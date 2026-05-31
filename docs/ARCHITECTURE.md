# Architecture

Maintainer Signal Kit is intentionally small and dependency-light.

## Modules

- `audit.py`: collects repository file and git activity signals.
- `models.py`: stores immutable report, signal, git activity, and project
  profile data.
- `render.py`: renders reports and drafts as Markdown, JSON, and HTML.
- `profile.py`: reads optional `.maintainer-signal.json` project context.
- `pack.py`: writes the complete evidence pack.
- `cli.py`: exposes the command-line interface.

## Data Flow

1. The CLI receives a repository path.
2. `audit_repository` reads local files and git metadata.
3. Optional profile context is loaded from `.maintainer-signal.json`.
4. Renderers produce human-readable and machine-readable outputs.
5. The `pack` command writes the outputs to a local directory.

## Safety Model

The tool is designed for local, read-oriented repository inspection. It does not
call external APIs, upload files, or make claims based on private data. Future
network integrations should be optional and explicit.
