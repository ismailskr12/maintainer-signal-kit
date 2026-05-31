from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Signal:
    name: str
    present: bool
    detail: str
    points: int
    max_points: int


@dataclass(frozen=True)
class GitActivity:
    available: bool
    commits_last_90_days: int = 0
    contributor_count: int = 0
    latest_commit_date: str | None = None
    tag_count: int = 0
    remote_url: str | None = None
    detail: str = "git metadata unavailable"


@dataclass(frozen=True)
class AuditReport:
    repository_name: str
    path: str
    score: int
    max_score: int
    signals: tuple[Signal, ...]
    git_activity: GitActivity
    next_steps: tuple[str, ...] = field(default_factory=tuple)

    @property
    def percentage(self) -> int:
        if self.max_score == 0:
            return 0
        return round((self.score / self.max_score) * 100)


@dataclass(frozen=True)
class ProjectProfile:
    project_name: str = ""
    repository_url: str = ""
    maintainer_role: str = ""
    project_mission: str = ""
    ecosystem_impact: str = ""
    credit_usage_plan: str = ""
    additional_context: str = ""
    public_evidence: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class GitHubMetrics:
    repository: str
    url: str
    description: str
    stars: int
    forks: int
    open_issues: int
    watchers: int
    default_branch: str
    license_name: str | None
    created_at: str | None
    updated_at: str | None
    pushed_at: str | None
    archived: bool
    disabled: bool
    topics: tuple[str, ...] = field(default_factory=tuple)
