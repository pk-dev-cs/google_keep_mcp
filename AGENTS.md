# Working on google-keep-mcp

## Project context

- This is a Python 3.11+ MCP server for Google Keep. It uses FastMCP, `gkeepapi`, and `uv`.
- MCP tools and server startup live in `src/google_keep_mcp/server.py`. The token setup helper is `scripts/get_master_token.py`.
- `pyproject.toml` defines the package and dependencies; `uv.lock` pins them. `Dockerfile` defines the image used by both `compose.yaml` and GitHub Actions. Keep setup instructions aligned with `README.md`.
- `gkeepapi` uses an unofficial Google Keep interface. Avoid assuming its behavior is stable across upstream changes.

## Branches

- Do not implement or publish changes directly on `main`.
- Create a session branch from the current `main` before making changes.
- Name session branches `Session-DD-MM-YY` (for example, `Session-01-11-26`).
- Keep the session branch after merging so the repository history retains the same structure.

## Commits

- Split work into small, logical commits. Each commit should represent one coherent concern.
- Use short English commit subjects written in lowercase (for example, `add local stdio setup`).
- Do not mix unrelated cleanup or formatting with a functional change.
- Review the diff and verify the project before committing or publishing.

## Publishing to main

- Publishing locally means committing on the session branch and merging it into local `main`.
- Merge session branches with `--no-ff`; do not squash or fast-forward them into `main`.
- Name merge commits `MERGE N: Description`, where `N` is the next merge number in the repository history.
- Verify that the working tree is clean and that `main` contains the merge commit after publishing.
- Do not push to `origin` unless the user explicitly requests a push.

## Verification

- For dependency changes, update both `pyproject.toml` and `uv.lock`.
- Run `uv sync --locked` when dependencies need to be installed, then use `uv run python -m compileall -q src scripts` for a basic syntax check. Run relevant tests if they exist.
- For container changes, run `docker compose config --quiet` and `docker compose build` when Docker is available.
- Run `git diff --check` to catch whitespace errors before committing or merging.
- Do not run live Google Keep operations as a routine check: some MCP tools create, modify, or delete notes and labels.

## Code style and Git safety

- Prefer clear names over comments. Use comments for complex logic or non-obvious decisions, and remove commented-out code.
- Do not overwrite unrelated work already in the working tree.
- Never use `git reset --hard` because it discards uncommitted changes.

## Credentials and data

- Never commit real values for `GOOGLE_KEEP_EMAIL`, `GOOGLE_KEEP_MASTER_TOKEN`, `GOOGLE_KEEP_DEVICE_ID`, or the EmbeddedSetup `oauth_token` cookie. Keep `.env.example` as placeholders only; `.env` is ignored by Git.
- Do not print, log, or include credentials or private Keep content in examples, tests, diffs, or responses.
- Treat cached Keep state as private. Avoid adding state files or volumes unless the task calls for them.

## Licensing

- This repository currently has no license file or license metadata. Do not assume permission to relicense upstream code; raise licensing questions with the user when relevant.
