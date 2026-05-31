# Example Evidence Pack Workflow

Generate a full pack:

```bash
python -m maintainer_signal_kit pack . --output-dir maintainer-evidence-pack
```

The generated directory contains:

- `maintenance-report.md`
- `maintenance-report.json`
- `maintenance-report.html`
- `application-draft.md`
- `evidence-checklist.md`

Before submitting any application, open `application-draft.md` and replace
remaining placeholders with verified data only.

Fetch public GitHub metadata when you need external repository evidence:

```bash
python -m maintainer_signal_kit github https://github.com/ismailskr12/maintainer-signal-kit
```
