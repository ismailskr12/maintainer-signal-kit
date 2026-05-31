from __future__ import annotations

import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from maintainer_signal_kit import audit_repository
from maintainer_signal_kit.cli import main
from maintainer_signal_kit.github import github_activity_to_markdown, github_metrics_to_markdown, parse_github_repository
from maintainer_signal_kit.models import GitHubActivitySummary, GitHubMetrics
from maintainer_signal_kit.pack import build_evidence_pack
from maintainer_signal_kit.profile import load_project_profile
from maintainer_signal_kit.readiness import render_readiness_report
from maintainer_signal_kit.redact import redact_text, scan_text
from maintainer_signal_kit.render import render_json, render_markdown


class AuditRepositoryTests(unittest.TestCase):
    def test_scores_present_repository_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "SECURITY.md").write_text("# Security\n", encoding="utf-8")
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
            (root / "tests").mkdir()

            report = audit_repository(root)

        present = {signal.name for signal in report.signals if signal.present}
        self.assertIn("README", present)
        self.assertIn("LICENSE", present)
        self.assertIn("SECURITY", present)
        self.assertIn("CI", present)
        self.assertGreater(report.score, 0)
        self.assertFalse(report.git_activity.available)

    def test_markdown_renderer_contains_score_and_next_steps(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            report = audit_repository(root)

        markdown = render_markdown(report)

        self.assertIn("Maintenance Signal Report", markdown)
        self.assertIn("Score:", markdown)
        self.assertIn("Suggested Next Steps", markdown)

    def test_json_renderer_is_machine_readable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = audit_repository(root)

        rendered = render_json(report)

        self.assertIn('"repository_name"', rendered)
        self.assertIn('"signals"', rendered)

    def test_profile_loader_reads_project_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".maintainer-signal.json").write_text(
                '{"project_name":"Demo","public_evidence":["README present"]}',
                encoding="utf-8",
            )

            profile = load_project_profile(root)

        self.assertEqual(profile.project_name, "Demo")
        self.assertEqual(profile.public_evidence, ("README present",))

    def test_evidence_pack_writes_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            output = Path(directory) / "pack"
            root.mkdir()
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / ".maintainer-signal.json").write_text(
                '{"project_name":"Demo","maintainer_role":"Primary maintainer"}',
                encoding="utf-8",
            )

            written = build_evidence_pack(root, output)

        names = {path.name for path in written}
        self.assertEqual(
            names,
            {
                "application-draft.md",
                "evidence-checklist.md",
                "maintenance-report.html",
                "maintenance-report.json",
                "maintenance-report.md",
                "readiness-report.md",
                "redaction-report.md",
            },
        )

    def test_parse_github_repository_accepts_url_and_slug(self) -> None:
        self.assertEqual(
            parse_github_repository("https://github.com/ismailskr12/maintainer-signal-kit"),
            "ismailskr12/maintainer-signal-kit",
        )
        self.assertEqual(
            parse_github_repository("ismailskr12/maintainer-signal-kit.git"),
            "ismailskr12/maintainer-signal-kit",
        )

    def test_github_metrics_markdown_includes_public_counts(self) -> None:
        metrics = GitHubMetrics(
            repository="owner/repo",
            url="https://github.com/owner/repo",
            description="Demo",
            stars=3,
            forks=2,
            open_issues=1,
            watchers=4,
            default_branch="main",
            license_name="MIT",
            created_at="2026-01-01T00:00:00Z",
            updated_at="2026-01-02T00:00:00Z",
            pushed_at="2026-01-03T00:00:00Z",
            archived=False,
            disabled=False,
            topics=("oss", "maintenance"),
        )

        rendered = github_metrics_to_markdown(metrics)

        self.assertIn("Stars: 3", rendered)
        self.assertIn("Topics: oss, maintenance", rendered)

    def test_github_activity_markdown_includes_workflow_counts(self) -> None:
        activity = GitHubActivitySummary(
            repository="owner/repo",
            contributors_observed=2,
            open_pull_requests=1,
            recent_closed_pull_requests=4,
            open_issues_only=3,
            recent_closed_issues_only=5,
            release_count_observed=2,
            languages=("Python", "Shell"),
        )

        rendered = github_activity_to_markdown(activity)

        self.assertIn("Contributors observed: 2", rendered)
        self.assertIn("Languages: Python, Shell", rendered)

    def test_redaction_finds_and_masks_sensitive_text(self) -> None:
        text = "contact me@example.com with API_KEY=secret"

        findings = scan_text(text, "demo.txt")
        redacted = redact_text(text)

        self.assertEqual(len(findings), 2)
        self.assertIn("[REDACTED:email]", redacted)
        self.assertIn("[REDACTED:api-key]", redacted)

    def test_readiness_report_states_caveat(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            report = audit_repository(root)

        rendered = render_readiness_report(report)

        self.assertIn("Selection Readiness", rendered)
        self.assertIn("does not guarantee acceptance", rendered)

    def test_cli_audit_writes_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            output = StringIO()

            with redirect_stdout(output):
                exit_code = main(["audit", str(root)])

        self.assertEqual(exit_code, 0)
        self.assertIn("Maintenance Signal Report", output.getvalue())


if __name__ == "__main__":
    unittest.main()
