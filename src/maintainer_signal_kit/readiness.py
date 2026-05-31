from __future__ import annotations

from .models import AuditReport


def readiness_level(report: AuditReport) -> str:
    if report.percentage >= 90 and report.git_activity.tag_count > 0:
        return "strong"
    if report.percentage >= 70:
        return "developing"
    return "early"


def render_readiness_report(report: AuditReport) -> str:
    level = readiness_level(report)
    missing = [signal.name for signal in report.signals if not signal.present]
    lines = [
        f"# Selection Readiness: {report.repository_name}",
        "",
        f"- Repository hygiene score: {report.score}/{report.max_score} ({report.percentage}%)",
        f"- Readiness level: {level}",
        f"- Recent commits: {report.git_activity.commits_last_90_days}",
        f"- Contributors observed locally: {report.git_activity.contributor_count}",
        f"- Release tags: {report.git_activity.tag_count}",
        f"- Remote configured: {'yes' if report.git_activity.remote_url else 'no'}",
        "",
        "## Strong Signals",
        "",
    ]
    lines.extend(f"- {signal.name}: {signal.detail}" for signal in report.signals if signal.present)
    lines.extend(["", "## Weak Or Missing Signals", ""])
    if missing:
        lines.extend(f"- {name}" for name in missing)
    else:
        lines.append("- No core repository hygiene signals are missing.")

    lines.extend(
        [
            "",
            "## Important Caveat",
            "",
            "Repository hygiene does not guarantee acceptance into any support program. "
            "External adoption, ecosystem importance, and real maintainer activity must be verified separately.",
            "",
        ]
    )
    return "\n".join(lines)
