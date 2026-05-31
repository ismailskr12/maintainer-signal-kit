# Maintainer Signal Kit

Maintainer Signal Kit is a small CLI for open-source maintainers who need a clear,
honest view of a repository's maintenance signals before applying to grants,
credits programs, or security review initiatives.

It inspects a local repository and produces a concise report covering:

- documentation and governance files
- security and contribution policies
- CI workflow presence
- package manifests
- recent git activity, contributors, and tags when available
- practical next steps to improve maintainability

The tool is intentionally evidence-first. It does not invent usage, adoption, or
maintainer history.

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

## Development

Run tests:

```bash
python -m unittest discover -s tests
```

Run the CLI locally:

```bash
python -m maintainer_signal_kit audit .
```

## License

MIT
