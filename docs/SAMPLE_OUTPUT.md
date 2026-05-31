# Sample Output

Example command:

```bash
python -m maintainer_signal_kit audit .
```

Example report excerpt:

```text
# Maintenance Signal Report: maintainer-signal-kit

- Score: 82/82 (100%)

## Signals

| Signal | Status | Evidence | Points |
| --- | --- | --- | ---: |
| README | present | README.md | 12/12 |
| LICENSE | present | LICENSE | 10/10 |
| SECURITY | present | SECURITY.md | 8/8 |
| CI | present | .github/workflows | 12/12 |

## Git Activity

- Commits in last 90 days: 4
- Tags: 2
- Remote: https://github.com/ismailskr12/maintainer-signal-kit.git
```

Generated application drafts should be reviewed by a human before submission.

Example GitHub metrics command:

```bash
python -m maintainer_signal_kit github ismailskr12/maintainer-signal-kit
```
