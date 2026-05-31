# Product Brief

Maintainer Signal Kit turns a local open-source repository into a shareable
maintenance evidence pack.

## Problem

Maintainers are often asked to prove that a project is active, safe to
contribute to, important enough to support, and ready for credits, grants, or
security tooling. That work is usually manual and error-prone. It is also easy
to accidentally overstate adoption when a form asks for a short justification.

## Approach

The project favors verifiable evidence over persuasion. It inspects repository
files and git metadata, then generates reports and draft application material
that clearly separates known facts from placeholders requiring human review.
It can also fetch public GitHub repository metrics for repositories selected by
the maintainer.

## Primary Users

- solo maintainers preparing support program applications
- small maintainer teams documenting project health
- reviewers who need a quick repository hygiene snapshot
- open-source programs that want applicants to submit structured evidence

## Non-Goals

- It does not claim eligibility for any third-party program.
- It does not scrape private data or transmit repository contents.
- It does not invent usage, downloads, stars, contributors, or maintainer roles.
- It does not hide weak signals; new projects should state that they are new.
