from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from maintainer_signal_kit import audit_repository
from maintainer_signal_kit.pack import build_evidence_pack
from maintainer_signal_kit.profile import load_project_profile
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
            },
        )


if __name__ == "__main__":
    unittest.main()
