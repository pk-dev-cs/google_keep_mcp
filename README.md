# google-keep-mcp

An MCP server for Google Keep, built on [gkeepapi](https://github.com/kiwiz/gkeepapi) (an unofficial, reverse-engineered client — there is no official Google Keep API for consumer accounts).

## Tools

16 tools across three groups:

**Notes & lists** — `search_notes`, `get_note`, `create_note`, `create_list`, `update_note`, `trash_note`, `restore_note`, `delete_note`

**Checklist items** — `add_list_item`, `update_list_item`, `delete_list_item`

**Labels** — `list_labels`, `create_label`, `delete_label`, `add_label_to_note`, `remove_label_from_note`

## Auth

`gkeepapi` authenticates with an email and master token. To obtain one, sign in
at [Google EmbeddedSetup](https://accounts.google.com/EmbeddedSetup), click
"I agree", and copy the `oauth_token` cookie value from your browser's
Developer Tools (Application/Storage → Cookies → `accounts.google.com`). The
page may keep loading after you agree. Then run:

```bash
uv run python scripts/get_master_token.py
```

The script prompts for the cookie with hidden input and exchanges it through
`gpsoauth` for a master token. It does not use your Google password or an app
password. Never share the cookie or master token; the master token grants full
account access. It also pins a random device ID so the server doesn't rely on
the host machine's MAC address for its device identity.

Required env vars:

```bash
GOOGLE_KEEP_EMAIL=you@gmail.com
GOOGLE_KEEP_MASTER_TOKEN=...
GOOGLE_KEEP_DEVICE_ID=...

# optional: cache Keep state to disk for faster startup
GOOGLE_KEEP_STATE_PATH=./.keep_state.json
```

See `.env.example`.

## Quick Start

```bash
uv sync --locked

# Run locally (stdio)
uv run python -m google_keep_mcp.server

```

## Docker

Build the image from this checkout. The `Dockerfile` installs
dependencies from `uv.lock` and runs the server as an unprivileged user:

```bash
docker compose build
```

To generate the Google master token without installing Python/uv on the host,
complete the EmbeddedSetup browser steps above and run the setup script
interactively in the locally built image:

```bash
docker compose run --rm --pull never google-keep-mcp python scripts/get_master_token.py
```

The setup command uses a terminal so the cookie input is hidden. The
Codex MCP command below uses `-T` to disable the terminal for STDIO.

Create a local `.env` containing the printed `GOOGLE_KEEP_EMAIL`,
`GOOGLE_KEEP_MASTER_TOKEN`, and `GOOGLE_KEEP_DEVICE_ID` before connecting the
server. Do not commit or share this file. The script prints the token to your
terminal; avoid saving its output in logs or shell history.

Connect Codex to the container through STDIO, without publishing an HTTP port.
Add this to your Codex `config.toml` and restart Codex:

```toml
[mcp_servers.google_keep]
command = "docker"
args = ["compose", "run", "--rm", "-T", "--pull", "never", "google-keep-mcp"]
cwd = "<absolute path to this checkout>"
enabled_tools = ["search_notes", "get_note", "list_labels"]
```

Replace `cwd` with the location of your checkout. Use `docker compose run`
rather than `docker compose up`: the STDIO server
needs its input and output connected to an MCP client. The service creates no
port or Keep state volume. The read-only tool allowlist limits Codex's
actions, but the Google token still grants the server broader access.

## Upstream deployment (separate from this local setup)

The upstream author describes a separate deployment on `ampere` via Komodo
(stack: `google-keep-mcp-ampere`), registered in MetaMCP's `main-namespace` as
`google-keep-mcp` (port 8082). The local Compose setup above does not use it.

In the upstream repository, pushing to `main` rebuilds its image; the author
then redeploys the stack via Komodo. This fork's local Compose setup is separate.

## A note on stability

`gkeepapi` is unofficial and periodically breaks when Google changes its login flow or adds new Keep content types — see its [CHANGELOG](https://github.com/kiwiz/gkeepapi/blob/master/CHANGELOG.md) and issue tracker. If this server suddenly starts failing with `LoginException` or similar, it's very likely a `gkeepapi` compatibility issue, not something wrong in this repo. Check upstream before debugging locally.

## Tech Stack

| Component | Choice |
|-----------|--------|
| MCP framework | [FastMCP](https://gofastmcp.com) 2.x |
| Keep client | [gkeepapi](https://github.com/kiwiz/gkeepapi) |
| Package management | [uv](https://github.com/astral-sh/uv) |
