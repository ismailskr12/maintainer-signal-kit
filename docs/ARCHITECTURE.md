# Architecture

Maintainer Signal Kit is intentionally small and dependency-light.

## Modules

- `audit.py`: collects repository file and git activity signals.
- `models.py`: stores immutable report, signal, git activity, and project
  profile data.
- `render.py`: renders reports and drafts as Markdown, JSON, and HTML.
- `profile.py`: reads optional `.maintainer-signal.json` project context.
- `github.py`: fetches public GitHub repository metrics for explicit
  user-selected repositories.
- `readiness.py`: renders a conservative readiness report from local audit
  evidence.
- `redact.py`: scans generated text for obvious sensitive values before public
  sharing.
- `pack.py`: writes the complete evidence pack.
- `cli.py`: exposes the command-line interface.

## Data Flow

1. The CLI receives a repository path.
2. `audit_repository` reads local files and git metadata.
3. Optional profile context is loaded from `.maintainer-signal.json`.
4. Renderers produce human-readable and machine-readable outputs.
5. The `pack` command writes the outputs to a local directory.
6. The optional `github` and `activity` commands fetch public repository metrics
   from GitHub's API for evidence gathering.
7. The pack command also writes readiness and redaction reports.

## Safety Model

The tool is designed for local, read-oriented repository inspection. The only
network feature is the explicit `github` command, which reads public repository
metadata from GitHub for a user-selected repository. It does not upload files or
make claims based on private data.
