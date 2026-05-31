from __future__ import annotations

import argparse
from pathlib import Path

from .audit import audit_repository
from .pack import build_evidence_pack
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

    parser.error(f"Unknown command: {args.command}")
    return 2
