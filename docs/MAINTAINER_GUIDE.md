# Maintainer Guide

This guide documents the expected maintenance workflow for Maintainer Signal Kit.

## Release Workflow

1. Update `CHANGELOG.md`.
2. Update the package version in `pyproject.toml` and
   `src/maintainer_signal_kit/__init__.py`.
3. Run:

   ```bash
   python -m unittest discover -s tests
   python -m maintainer_signal_kit pack . --output-dir maintainer-evidence-pack
   ```

4. Commit the release changes.
5. Create an annotated tag:

   ```bash
   git tag -a vX.Y.Z -m "vX.Y.Z"
   ```

6. Push `main` and tags.

## Review Principles

- Prefer evidence-backed behavior over optimistic claims.
- Keep generated application drafts conservative.
- Avoid collecting or transmitting private repository data.
- Treat repository metadata as public only after the maintainer confirms it is
  safe to share.

## Issue Triage

Use these labels when available:

- `bug`: broken behavior or incorrect report output
- `enhancement`: new signal, renderer, or workflow support
- `documentation`: docs-only changes
- `security`: vulnerability handling or sensitive-data concerns

## Security Review Checklist

- Does the change execute external commands?
- Does it read files outside the requested repository path?
- Does it transmit repository data over the network?
- Does it include secrets, tokens, emails, or private URLs in generated output?

Changes that affect any of those areas should get an extra maintainer review.
