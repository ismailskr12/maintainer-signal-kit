from __future__ import annotations

import argparse
from pathlib import Path

from .audit import audit_repository
from .render import render_json, render_markdown


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
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    audit.add_argument("--output", help="Write output to a file instead of stdout.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "audit":
        report = audit_repository(args.path)
        rendered = render_json(report) if args.format == "json" else render_markdown(report)
        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8")
        else:
            print(rendered, end="")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2
