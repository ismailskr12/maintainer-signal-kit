from __future__ import annotations

import json
from dataclasses import asdict

from html import escape

from .models import AuditReport, ProjectProfile


def render_markdown(report: AuditReport) -> str:
    lines = [
        f"# Maintenance Signal Report: {report.repository_name}",
        "",
        f"- Path: `{report.path}`",
        f"- Score: **{report.score}/{report.max_score}** ({report.percentage}%)",
        "",
        "## Signals",
        "",
        "| Signal | Status | Evidence | Points |",
        "| --- | --- | --- | ---: |",
    ]
    for signal in report.signals:
        status = "present" if signal.present else "missing"
        lines.append(f"| {signal.name} | {status} | {signal.detail} | {signal.points}/{signal.max_points} |")

    lines.extend(
        [
            "",
            "## Git Activity",
            "",
            f"- Available: {report.git_activity.available}",
            f"- Commits in last 90 days: {report.git_activity.commits_last_90_days}",
            f"- Contributors: {report.git_activity.contributor_count}",
            f"- Latest commit: {report.git_activity.latest_commit_date or 'unknown'}",
            f"- Tags: {report.git_activity.tag_count}",
            f"- Remote: {report.git_activity.remote_url or 'unknown'}",
            "",
            "## Suggested Next Steps",
            "",
        ]
    )

    if report.next_steps:
        lines.extend(f"- {step}" for step in report.next_steps)
    else:
        lines.append("- No immediate repository hygiene gaps found.")

    return "\n".join(lines) + "\n"


def render_json(report: AuditReport) -> str:
    return json.dumps(asdict(report), indent=2, sort_keys=True) + "\n"


def render_html(report: AuditReport) -> str:
    rows = "\n".join(
        "<tr>"
        f"<td>{escape(signal.name)}</td>"
        f"<td>{'present' if signal.present else 'missing'}</td>"
        f"<td>{escape(signal.detail)}</td>"
        f"<td>{signal.points}/{signal.max_points}</td>"
        "</tr>"
        for signal in report.signals
    )
    steps = "\n".join(f"<li>{escape(step)}</li>" for step in report.next_steps)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Maintenance Signal Report - {escape(report.repository_name)}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; line-height: 1.5; color: #172026; }}
    main {{ max-width: 980px; margin: 0 auto; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #d0d7de; padding: 0.6rem; text-align: left; }}
    th {{ background: #f6f8fa; }}
    .score {{ font-size: 2rem; font-weight: 700; }}
  </style>
</head>
<body>
<main>
  <h1>Maintenance Signal Report</h1>
  <p><strong>Repository:</strong> {escape(report.repository_name)}</p>
  <p class="score">{report.score}/{report.max_score} ({report.percentage}%)</p>
  <h2>Signals</h2>
  <table>
    <thead><tr><th>Signal</th><th>Status</th><th>Evidence</th><th>Points</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <h2>Git Activity</h2>
  <ul>
    <li>Commits in last 90 days: {report.git_activity.commits_last_90_days}</li>
    <li>Contributors: {report.git_activity.contributor_count}</li>
    <li>Latest commit: {escape(report.git_activity.latest_commit_date or 'unknown')}</li>
    <li>Tags: {report.git_activity.tag_count}</li>
    <li>Remote: {escape(report.git_activity.remote_url or 'unknown')}</li>
  </ul>
  <h2>Suggested Next Steps</h2>
  <ul>{steps or '<li>No immediate repository hygiene gaps found.</li>'}</ul>
</main>
</body>
</html>
"""


def render_application_draft(report: AuditReport, profile: ProjectProfile) -> str:
    repository_url = profile.repository_url or report.git_activity.remote_url or "[public repository URL]"
    project_name = profile.project_name or report.repository_name
    evidence_lines = profile.public_evidence or (
        f"Maintenance score: {report.score}/{report.max_score} ({report.percentage}%).",
        f"Recent commits: {report.git_activity.commits_last_90_days}.",
        f"Release tags: {report.git_activity.tag_count}.",
    )
    return "\n".join(
        [
            "# Open Source Support Application Draft",
            "",
            "This draft is generated from local repository evidence and project profile data.",
            "Review every line before submitting it to any program.",
            "",
            "## Project",
            "",
            f"- Name: {project_name}",
            f"- Repository: {repository_url}",
            "",
            "## Maintainer Role",
            "",
            profile.maintainer_role or "[Describe your real role: primary maintainer, core maintainer, reviewer, release manager, or security contact.]",
            "",
            "## Project Mission",
            "",
            profile.project_mission or "[Explain the concrete problem this project solves for open-source maintainers or users.]",
            "",
            "## Ecosystem Impact",
            "",
            profile.ecosystem_impact or "[Add verified usage, users, stars, downloads, dependencies, organizations, or ecosystem importance.]",
            "",
            "## Public Evidence",
            "",
            *(f"- {line}" for line in evidence_lines),
            "",
            "## How Credits Or Tooling Would Be Used",
            "",
            profile.credit_usage_plan or "[Describe real maintainer workflows: issue triage, pull request review, release automation, tests, documentation, or security review.]",
            "",
            "## Additional Context",
            "",
            profile.additional_context or "[Optional context. Do not include unverifiable adoption claims.]",
            "",
        ]
    )


def render_evidence_checklist(report: AuditReport) -> str:
    missing = [signal for signal in report.signals if not signal.present]
    lines = [
        "# Evidence Checklist",
        "",
        "Use this checklist before submitting a public support, grant, or credits application.",
        "",
        "## Repository Evidence",
        "",
    ]
    lines.extend(
        f"- [{'x' if signal.present else ' '}] {signal.name}: {signal.detail}"
        for signal in report.signals
    )
    lines.extend(
        [
            "",
            "## Activity Evidence",
            "",
            f"- [{'x' if report.git_activity.available else ' '}] Git history is available.",
            f"- [{'x' if report.git_activity.commits_last_90_days > 0 else ' '}] Recent commits exist.",
            f"- [{'x' if report.git_activity.tag_count > 0 else ' '}] Release tags exist.",
            f"- [{'x' if report.git_activity.remote_url else ' '}] Public remote URL is configured.",
            "",
            "## Claims To Verify Manually",
            "",
            "- [ ] Stars, forks, downloads, dependents, users, or organization usage.",
            "- [ ] Your exact maintainer role and responsibilities.",
            "- [ ] How requested credits/tooling will support public open-source work.",
            "- [ ] No private data, secrets, or exaggerated adoption claims are included.",
            "",
        ]
    )
    if missing:
        lines.extend(["## Highest Priority Gaps", ""])
        lines.extend(f"- Add {signal.name.lower().replace('_', ' ')}." for signal in missing)
        lines.append("")
    return "\n".join(lines)
