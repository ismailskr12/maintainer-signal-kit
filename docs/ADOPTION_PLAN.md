# Adoption Plan

This plan focuses on earning real usage instead of manufacturing signals.

## First Maintainer Feedback Loop

- Share the repository with small open-source maintainers preparing support
  applications.
- Ask each reviewer to generate an evidence pack against one public repository.
- Collect issues for confusing wording, missing checks, and false positives.

## Example Reports

Publish example reports for public repositories where the generated output can
be verified independently. Example reports should avoid judgmental scoring and
focus on evidence quality.

## Package Distribution

- Prepare PyPI packaging after the CLI stabilizes.
- Add installation instructions for isolated environments.
- Add changelog entries for every user-facing command.

## Trust Building

- Keep network calls explicit.
- Keep redaction reports visible.
- Document weak signals honestly.
- Prefer smaller releases with clear test coverage.
