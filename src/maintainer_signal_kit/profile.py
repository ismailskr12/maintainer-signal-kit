from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import ProjectProfile


DEFAULT_PROFILE_NAME = ".maintainer-signal.json"


def load_project_profile(path: str | Path) -> ProjectProfile:
    profile_path = Path(path)
    if profile_path.is_dir():
        profile_path = profile_path / DEFAULT_PROFILE_NAME
    if not profile_path.exists():
        return ProjectProfile()

    data = json.loads(profile_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Project profile must be a JSON object.")

    evidence = data.get("public_evidence", ())
    if isinstance(evidence, str):
        evidence = (evidence,)
    if not isinstance(evidence, list | tuple):
        raise ValueError("public_evidence must be a string or list of strings.")

    return ProjectProfile(
        project_name=_string(data, "project_name"),
        repository_url=_string(data, "repository_url"),
        maintainer_role=_string(data, "maintainer_role"),
        project_mission=_string(data, "project_mission"),
        ecosystem_impact=_string(data, "ecosystem_impact"),
        credit_usage_plan=_string(data, "credit_usage_plan"),
        additional_context=_string(data, "additional_context"),
        public_evidence=tuple(str(item) for item in evidence),
    )


def _string(data: dict[str, Any], key: str) -> str:
    value = data.get(key, "")
    return value if isinstance(value, str) else str(value)
