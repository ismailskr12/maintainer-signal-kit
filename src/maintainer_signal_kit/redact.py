from __future__ import annotations

import re
from pathlib import Path

from .models import SensitiveFinding


SENSITIVE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("api-key", re.compile(r"\b(sk-[A-Za-z0-9_-]{20,}|[A-Za-z0-9_]*API[_-]?KEY[A-Za-z0-9_]*\s*[=:])")),
    ("email", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
)


def scan_text(text: str, path: str = "<text>") -> tuple[SensitiveFinding, ...]:
    findings: list[SensitiveFinding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for category, pattern in SENSITIVE_PATTERNS:
            if pattern.search(line):
                findings.append(
                    SensitiveFinding(
                        category=category,
                        path=path,
                        line=line_number,
                        preview=_preview(line),
                    )
                )
    return tuple(findings)


def redact_text(text: str) -> str:
    redacted = text
    for category, pattern in SENSITIVE_PATTERNS:
        redacted = pattern.sub(f"[REDACTED:{category}]", redacted)
    return redacted


def scan_file(path: str | Path) -> tuple[SensitiveFinding, ...]:
    file_path = Path(path)
    try:
        text = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ()
    return scan_text(text, str(file_path))


def render_redaction_report(findings: tuple[SensitiveFinding, ...]) -> str:
    lines = [
        "# Redaction Report",
        "",
        "This report flags text that should be reviewed before public sharing.",
        "",
    ]
    if not findings:
        lines.append("No obvious sensitive values found.")
        return "\n".join(lines) + "\n"

    lines.extend(["| Category | Path | Line | Preview |", "| --- | --- | ---: | --- |"])
    for finding in findings:
        lines.append(
            f"| {finding.category} | `{finding.path}` | {finding.line} | `{finding.preview}` |"
        )
    return "\n".join(lines) + "\n"


def _preview(line: str) -> str:
    clean = " ".join(line.strip().split())
    return redact_text(clean[:160])
