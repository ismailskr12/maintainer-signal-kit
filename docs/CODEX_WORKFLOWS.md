# Codex Workflows

Maintainer Signal Kit is designed to make Codex useful for routine open-source
maintenance without replacing maintainer judgment.

## Pull Request Review

Codex can run the audit and pack commands on a pull request branch, then point
reviewers to changes that affect public claims, repository safety, or generated
application drafts.

Suggested prompt:

```text
Review this PR for evidence quality. Verify that generated reports do not make
unverifiable usage or adoption claims, then run the test suite.
```

## Issue Triage

Codex can summarize incoming issues into maintenance categories:

- incorrect repository signal
- missing renderer
- packaging problem
- documentation gap
- security or privacy concern

## Release Prep

Codex can help maintainers:

- update the changelog
- run tests
- generate an evidence pack
- verify that public metrics and generated drafts are still accurate
- prepare a release note from commits

## Security Review

Codex should pay special attention to:

- new network calls
- file path handling
- generated output that might include private data
- command execution behavior
- accidental inclusion of credentials

The project intentionally keeps network behavior explicit. The `github` command
only calls GitHub's public repository API for a repository selected by the user.
