from __future__ import annotations

import argparse
from pathlib import Path

from .audit import audit_repository
from .github import (
    fetch_github_activity,
    fetch_github_metrics,
    github_activity_to_json,
    github_activity_to_markdown,
    github_metrics_to_json,
    github_metrics_to_markdown,
)
from .pack import build_evidence_pack
from .readiness import render_readiness_report
from .redact import redact_text, render_redaction_report, scan_file
from .render import render_html, render_json, render_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="maintainer-signal",
        description="Audit open-source repository maintenance signals.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser("audit", help="Audit a local repository.")
    audit.add_argument("path", nargs="?", default=".", help="Repository path to audit.")
    audit.add_argument(
        "--format",
        choices=("markdown", "json", "html"),
        default="markdown",
        help="Output format.",
    )
    audit.add_argument("--output", help="Write output to a file instead of stdout.")

    pack = subparsers.add_parser("pack", help="Build a maintainer evidence pack.")
    pack.add_argument("path", nargs="?", default=".", help="Repository path to audit.")
    pack.add_argument(
        "--output-dir",
        default="maintainer-evidence-pack",
        help="Directory for generated report and application draft files.",
    )

    github = subparsers.add_parser("github", help="Fetch public GitHub repository metrics.")
    github.add_argument("repository", help="GitHub repository URL or owner/name.")
    github.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    github.add_argument("--output", help="Write output to a file instead of stdout.")

    activity = subparsers.add_parser("activity", help="Fetch public GitHub activity signals.")
    activity.add_argument("repository", help="GitHub repository URL or owner/name.")
    activity.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    activity.add_argument("--output", help="Write output to a file instead of stdout.")

    readiness = subparsers.add_parser("readiness", help="Render selection readiness notes.")
    readiness.add_argument("path", nargs="?", default=".", help="Repository path to audit.")
    readiness.add_argument("--output", help="Write output to a file instead of stdout.")

    redact = subparsers.add_parser("redact", help="Scan or redact sensitive text in a file.")
    redact.add_argument("path", help="UTF-8 file to scan.")
    redact.add_argument("--apply", action="store_true", help="Print redacted file contents.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "audit":
        report = audit_repository(args.path)
        renderers = {
            "html": render_html,
            "json": render_json,
            "markdown": render_markdown,
        }
        rendered = renderers[args.format](report)
        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
        return 0

    if args.command == "pack":
        written = build_evidence_pack(args.path, args.output_dir)
        for path in written:
            print(path)
        return 0

    if args.command == "github":
        metrics = fetch_github_metrics(args.repository)
        rendered = (
            github_metrics_to_json(metrics)
            if args.format == "json"
            else github_metrics_to_markdown(metrics)
        )
        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
        return 0

    if args.command == "activity":
        activity = fetch_github_activity(args.repository)
        rendered = (
            github_activity_to_json(activity)
            if args.format == "json"
            else github_activity_to_markdown(activity)
        )
        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
        return 0

    if args.command == "readiness":
        rendered = render_readiness_report(audit_repository(args.path))
        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
        return 0

    if args.command == "redact":
        path = Path(args.path)
        text = path.read_text(encoding="utf-8")
        if args.apply:
            print(redact_text(text), end="")
        else:
            print(render_redaction_report(scan_file(path)), end="")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2
