from __future__ import annotations

import json
from dataclasses import asdict

from .models import AuditReport


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
