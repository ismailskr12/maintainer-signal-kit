from __future__ import annotations

import json
from dataclasses import asdict
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from .models import GitHubActivitySummary, GitHubMetrics


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
    payload = _get_json(f"https://api.github.com/repos/{full_name}", timeout)
    if not isinstance(payload, dict):
        raise RuntimeError("Unexpected GitHub repository response.")

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


def fetch_github_activity(repository: str, timeout: float = 10.0) -> GitHubActivitySummary:
    full_name = parse_github_repository(repository)
    contributors = _expect_list(_get_json(f"https://api.github.com/repos/{full_name}/contributors?per_page=100", timeout))
    open_prs = _expect_list(_get_json(f"https://api.github.com/repos/{full_name}/pulls?state=open&per_page=100", timeout))
    closed_prs = _expect_list(_get_json(f"https://api.github.com/repos/{full_name}/pulls?state=closed&per_page=100", timeout))
    open_issues = _expect_list(_get_json(f"https://api.github.com/repos/{full_name}/issues?state=open&per_page=100", timeout))
    closed_issues = _expect_list(_get_json(f"https://api.github.com/repos/{full_name}/issues?state=closed&per_page=100", timeout))
    releases = _expect_list(_get_json(f"https://api.github.com/repos/{full_name}/releases?per_page=100", timeout))
    languages = _get_json(f"https://api.github.com/repos/{full_name}/languages", timeout)
    if not isinstance(languages, dict):
        languages = {}

    return GitHubActivitySummary(
        repository=full_name,
        contributors_observed=len(contributors),
        open_pull_requests=len(open_prs),
        recent_closed_pull_requests=len(closed_prs),
        open_issues_only=len([issue for issue in open_issues if "pull_request" not in issue]),
        recent_closed_issues_only=len([issue for issue in closed_issues if "pull_request" not in issue]),
        release_count_observed=len(releases),
        languages=tuple(str(language) for language in languages.keys()),
    )


def github_metrics_to_json(metrics: GitHubMetrics) -> str:
    return json.dumps(asdict(metrics), indent=2, sort_keys=True) + "\n"


def github_activity_to_json(activity: GitHubActivitySummary) -> str:
    return json.dumps(asdict(activity), indent=2, sort_keys=True) + "\n"


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


def github_activity_to_markdown(activity: GitHubActivitySummary) -> str:
    languages = ", ".join(activity.languages) if activity.languages else "none"
    return "\n".join(
        [
            f"# GitHub Activity: {activity.repository}",
            "",
            f"- Contributors observed: {activity.contributors_observed}",
            f"- Open pull requests: {activity.open_pull_requests}",
            f"- Recent closed pull requests: {activity.recent_closed_pull_requests}",
            f"- Open issues: {activity.open_issues_only}",
            f"- Recent closed issues: {activity.recent_closed_issues_only}",
            f"- Releases observed: {activity.release_count_observed}",
            f"- Languages: {languages}",
            "",
        ]
    )


def _get_json(url: str, timeout: float) -> object:
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "maintainer-signal-kit",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise RuntimeError(f"GitHub API returned HTTP {error.code} for {url}.") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach GitHub API for {url}: {error.reason}") from error


def _expect_list(value: object) -> list[object]:
    if not isinstance(value, list):
        raise RuntimeError("Unexpected GitHub list response.")
    return value
