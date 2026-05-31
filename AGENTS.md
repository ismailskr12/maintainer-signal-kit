# Agent Instructions

Maintainer Signal Kit is an evidence-first CLI. Keep generated claims truthful
and conservative.

## Development Commands

```bash
python -m pip install -e .
python -m unittest discover -s tests
python -m maintainer_signal_kit audit .
python -m maintainer_signal_kit pack . --output-dir maintainer-evidence-pack
python -m maintainer_signal_kit github ismailskr12/maintainer-signal-kit
```

## Rules For Agent Changes

- Do not invent adoption, stars, downloads, users, or maintainer history.
- Prefer standard library code unless a dependency clearly earns its weight.
- Add tests for every behavior change.
- Keep public reports free of secrets and private repository data.
- Update docs when CLI behavior changes.
