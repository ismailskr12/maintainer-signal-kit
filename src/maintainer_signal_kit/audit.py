from __future__ import annotations

import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path

from .models import AuditReport, GitActivity, Signal


def audit_repository(path: str | Path) -> AuditReport:
    root = Path(path).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Repository path does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Repository path is not a directory: {root}")

    signals = _file_signals(root)
    git_activity = _git_activity(root)
    score = sum(signal.points for signal in signals)
    max_score = sum(signal.max_points for signal in signals)
    next_steps = _next_steps(signals, git_activity)

    return AuditReport(
        repository_name=root.name,
        path=str(root),
        score=score,
        max_score=max_score,
        signals=tuple(signals),
        git_activity=git_activity,
        next_steps=tuple(next_steps),
    )


def _file_signals(root: Path) -> list[Signal]:
    checks = [
        ("README", ["README.md", "README.rst", "README.txt"], 12, "project overview and usage docs"),
        ("LICENSE", ["LICENSE", "LICENSE.md", "COPYING"], 10, "explicit open-source license"),
        ("CONTRIBUTING", ["CONTRIBUTING.md", ".github/CONTRIBUTING.md"], 8, "contribution workflow"),
        ("SECURITY", ["SECURITY.md", ".github/SECURITY.md"], 8, "vulnerability reporting policy"),
        ("CODE_OF_CONDUCT", ["CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.md"], 6, "community standards"),
        ("CI", [".github/workflows"], 12, "continuous integration workflow"),
        ("ISSUE_TEMPLATES", [".github/ISSUE_TEMPLATE"], 6, "structured issue reports"),
        ("PACKAGE_MANIFEST", ["pyproject.toml", "package.json", "Cargo.toml", "go.mod"], 10, "installable package metadata"),
        ("TESTS", ["tests", "test"], 10, "automated test directory"),
    ]

    signals: list[Signal] = []
    for name, candidates, max_points, detail in checks:
        found = _first_existing(root, candidates)
        signals.append(
            Signal(
                name=name,
                present=found is not None,
                detail=str(found.relative_to(root)) if found else detail,
                points=max_points if found else 0,
                max_points=max_points,
            )
        )
    return signals


def _first_existing(root: Path, candidates: list[str]) -> Path | None:
    for candidate in candidates:
        path = root / candidate
        if path.exists():
            return path
    return None


def _git_activity(root: Path) -> GitActivity:
    if not (root / ".git").exists():
        return GitActivity(available=False, detail="not a git repository")

    since = (datetime.now(UTC) - timedelta(days=90)).strftime("%Y-%m-%d")
    commits = _git(root, ["rev-list", "--count", f"--since={since}", "HEAD"])
    contributors = _git(root, ["shortlog", "-sne", "HEAD"])
    latest = _git(root, ["log", "-1", "--format=%cI"])
    tags = _git(root, ["tag", "--list"])

    if commits is None:
        return GitActivity(available=False, detail="git command failed")

    contributor_count = 0
    if contributors:
        contributor_count = len([line for line in contributors.splitlines() if line.strip()])

    tag_count = 0
    if tags:
        tag_count = len([line for line in tags.splitlines() if line.strip()])

    return GitActivity(
        available=True,
        commits_last_90_days=_parse_int(commits),
        contributor_count=contributor_count,
        latest_commit_date=latest.strip() if latest else None,
        tag_count=tag_count,
        detail="git metadata collected",
    )


def _git(root: Path, args: list[str]) -> str | None:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def _parse_int(value: str | None) -> int:
    try:
        return int((value or "0").strip())
    except ValueError:
        return 0


def _next_steps(signals: list[Signal], git_activity: GitActivity) -> list[str]:
    missing = [signal for signal in signals if not signal.present]
    steps = [f"Add {signal.name.lower().replace('_', ' ')}." for signal in missing[:5]]

    if not git_activity.available:
        steps.append("Initialize git history and publish the repository.")
    else:
        if git_activity.commits_last_90_days == 0:
            steps.append("Make recent maintenance commits visible in git history.")
        if git_activity.tag_count == 0:
            steps.append("Create release tags once the project has stable versions.")
        if git_activity.contributor_count < 2:
            steps.append("Document contributor onboarding and invite external review.")

    return steps
