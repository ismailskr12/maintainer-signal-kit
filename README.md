# Maintainer Signal Kit

Maintainer Signal Kit is an evidence-pack generator for open-source maintainers.
It helps a maintainer turn a local repository into a clear, honest dossier for
support programs, credit programs, security reviews, and internal maintenance
planning.

It inspects a local repository and produces reports covering:

- documentation and governance files
- security and contribution policies
- CI workflow presence
- package manifests
- recent git activity, contributors, and tags when available
- practical next steps to improve maintainability
- a human-reviewable support application draft
- a checklist that separates verified facts from claims requiring evidence

The tool is intentionally evidence-first. It does not invent usage, adoption, or
maintainer history.

## Core Idea

Most grant, credit, and open-source support applications ask maintainers for the
same facts: What do you maintain? Why does it matter? Are there signs of active
maintenance? How will support be used?

Maintainer Signal Kit makes that preparation repeatable. It generates a public
maintenance report and an application draft, but leaves unverifiable claims as
placeholders. That makes it useful without encouraging fake adoption metrics.

## Install

```bash
python -m pip install -e .
```

## Usage

Audit the current repository and print Markdown:

```bash
python -m maintainer_signal_kit audit .
```

Write JSON:

```bash
python -m maintainer_signal_kit audit . --format json --output report.json
```

Generate a full evidence pack:

```bash
python -m maintainer_signal_kit pack . --output-dir maintainer-evidence-pack
```

The pack includes Markdown, JSON, HTML, an application draft, and an evidence
checklist.

## Example

```text
Repository: maintainer-signal-kit
Score: 76/100

Strong signals:
- README present
- LICENSE present
- SECURITY.md present
- CI workflows present

Suggested next steps:
- Add issue templates
- Add release tags
```

## Why This Exists

Open-source support programs often ask maintainers to describe their role,
project importance, active maintenance work, and how credits or tooling will be
used. This project helps maintainers prepare that evidence without exaggerating
claims.

## Project Profile

Add `.maintainer-signal.json` to describe verified project context:

```json
{
  "project_name": "Maintainer Signal Kit",
  "maintainer_role": "Primary maintainer responsible for releases and security response.",
  "project_mission": "Help maintainers prepare honest support applications.",
  "ecosystem_impact": "Add verified stars, downloads, dependents, or users here.",
  "credit_usage_plan": "Use credits for pull request review and release automation."
}
```

Fields that cannot be verified should stay empty until evidence exists.

## Development

Run tests:

```bash
python -m unittest discover -s tests
```

Run the CLI locally:

```bash
python -m maintainer_signal_kit audit .
python -m maintainer_signal_kit pack .
```

## License

MIT
