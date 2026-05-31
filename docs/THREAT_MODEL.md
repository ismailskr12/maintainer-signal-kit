# Threat Model

Maintainer Signal Kit handles repository metadata and generated application
drafts. The main risks are accidental disclosure and unsupported public claims.

## Assets

- repository paths and file names
- generated application drafts
- public GitHub metrics
- maintainer profile data

## Risks

- private emails or tokens in generated drafts
- private repository paths shared publicly
- unsupported claims about adoption or impact
- unexpected network access

## Mitigations

- redaction scan in generated evidence packs
- explicit `github` and `activity` commands for network access
- conservative application draft templates
- documentation that tells maintainers not to invent metrics

## Out Of Scope

- scanning entire private codebases for secrets
- authenticating to GitHub or package registries
- guaranteeing third-party program acceptance
