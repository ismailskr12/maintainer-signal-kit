from __future__ import annotations

import json
from dataclasses import asdict
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from .models import GitHubMetrics


def parse_github_repository(value: str) -> str:
    candidate = value.strip()
    if not candidate:
        raise ValueError("GitHub repository cannot be empty.")

    if candidate.startswith("http://") or candidate.startswith("https://"):
        parsed = urlparse(candidate)
        if parsed.netloc.lower() != "github.com":
            raise ValueError("Only github.com repository URLs are supported.")
        parts = [part for part in parsed.path.strip("/").split("/") if part]
    else:
        parts = [part for part in candidate.strip("/").split("/") if part]

    if len(parts) < 2:
        raise ValueError("Expected GitHub repository in owner/name form.")

    owner, name = parts[0], parts[1]
    if name.endswith(".git"):
        name = name[:-4]
    return f"{owner}/{name}"


def fetch_github_metrics(repository: str, timeout: float = 10.0) -> GitHubMetrics:
    full_name = parse_github_repository(repository)
    request = Request(
        f"https://api.github.com/repos/{full_name}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "maintainer-signal-kit",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise RuntimeError(f"GitHub API returned HTTP {error.code} for {full_name}.") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach GitHub API for {full_name}: {error.reason}") from error

    return GitHubMetrics(
        repository=payload["full_name"],
        url=payload["html_url"],
        description=payload.get("description") or "",
        stars=int(payload.get("stargazers_count") or 0),
        forks=int(payload.get("forks_count") or 0),
        open_issues=int(payload.get("open_issues_count") or 0),
        watchers=int(payload.get("subscribers_count") or payload.get("watchers_count") or 0),
        default_branch=payload.get("default_branch") or "",
        license_name=(payload.get("license") or {}).get("spdx_id"),
        created_at=payload.get("created_at"),
        updated_at=payload.get("updated_at"),
        pushed_at=payload.get("pushed_at"),
        archived=bool(payload.get("archived")),
        disabled=bool(payload.get("disabled")),
        topics=tuple(payload.get("topics") or ()),
    )


def github_metrics_to_json(metrics: GitHubMetrics) -> str:
    return json.dumps(asdict(metrics), indent=2, sort_keys=True) + "\n"


def github_metrics_to_markdown(metrics: GitHubMetrics) -> str:
    topics = ", ".join(metrics.topics) if metrics.topics else "none"
    return "\n".join(
        [
            f"# GitHub Metrics: {metrics.repository}",
            "",
            f"- URL: {metrics.url}",
            f"- Description: {metrics.description or 'none'}",
            f"- Stars: {metrics.stars}",
            f"- Forks: {metrics.forks}",
            f"- Watchers: {metrics.watchers}",
            f"- Open issues: {metrics.open_issues}",
            f"- Default branch: {metrics.default_branch}",
            f"- License: {metrics.license_name or 'unknown'}",
            f"- Created: {metrics.created_at or 'unknown'}",
            f"- Updated: {metrics.updated_at or 'unknown'}",
            f"- Last push: {metrics.pushed_at or 'unknown'}",
            f"- Archived: {metrics.archived}",
            f"- Disabled: {metrics.disabled}",
            f"- Topics: {topics}",
            "",
        ]
    )
