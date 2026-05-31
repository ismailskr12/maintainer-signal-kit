from __future__ import annotations

from pathlib import Path

from .audit import audit_repository
from .profile import load_project_profile
from .render import (
    render_application_draft,
    render_evidence_checklist,
    render_html,
    render_json,
    render_markdown,
)


def build_evidence_pack(repo_path: str | Path, output_dir: str | Path) -> tuple[Path, ...]:
    root = Path(repo_path).expanduser().resolve()
    destination = Path(output_dir).expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)

    report = audit_repository(root)
    profile = load_project_profile(root)
    files = {
        "maintenance-report.md": render_markdown(report),
        "maintenance-report.json": render_json(report),
        "maintenance-report.html": render_html(report),
        "application-draft.md": render_application_draft(report, profile),
        "evidence-checklist.md": render_evidence_checklist(report),
    }

    written: list[Path] = []
    for name, content in files.items():
        path = destination / name
        path.write_text(content, encoding="utf-8")
        written.append(path)
    return tuple(written)
