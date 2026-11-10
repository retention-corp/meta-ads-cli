# meta-ads-mcp

Configuration assets for the **Meta Ads remote MCP server** — Meta's hosted
Model Context Protocol endpoint that lets any AI agent (Claude Desktop, Claude
Code, Cursor, ChatGPT, etc.) operate your Meta ad account in natural language.

- Help center (canonical):
  https://www.facebook.com/business/help/1456422242197840
- Endpoint: **`https://mcp.facebook.com/ads`** (single URL, all clients)
- Transport: HTTP (remote MCP)
- Auth: **OAuth via Meta** — the first tool call pops a Meta login + consent
  page in your browser. No API key, no system user token. Tokens are stored by
  the AI client and can be revoked from Meta Business Suite > Connected Apps.

This folder is config-only. Nothing here is "installed" — the server lives at
mcp.facebook.com. The files are templates you wire into the AI client of your
choice.

## What's here

```
meta-ads-mcp/
├── mcp.json                       # canonical Claude Code project-scope config
├── claude-desktop-snippet.json    # paste-target for Claude Desktop config
├── register-claude-code.sh        # one-liner to register with Claude Code
└── README.md
```

## Claude Code

Use the helper script (registers at user scope so the connector is available
in every project):

```bash
bash /Users/gyusupsim/Projects/tools/meta-ads-cli/meta-ads-mcp/register-claude-code.sh
```

Or run the underlying command directly:

```bash
claude mcp add --transport http --scope user meta-ads https://mcp.facebook.com/ads
```

Scope choices:

| Scope    | Stored in                                  | When to use                          |
|----------|--------------------------------------------|--------------------------------------|
| `user`   | `~/.claude.json` (or platform equivalent)  | Want the server in every project     |
| `local`  | project-local Claude state                 | Just this checkout                   |
| `project`| `./.mcp.json` (commits to git)             | Share with teammates via the repo    |

For project scope, copy `mcp.json` to the **repo root** as `.mcp.json` (Claude
Code only auto-discovers `.mcp.json` at the workspace root, not in subfolders).
After committing, teammates get a one-time prompt to approve the server.

Verify:

```bash
claude mcp get meta-ads
claude mcp list
```

Remove:

```bash
claude mcp remove meta-ads
```

## Claude Desktop

Paste the contents of `claude-desktop-snippet.json` into:

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

Merge under the existing top-level `mcpServers` key. Quit and relaunch Claude
Desktop. The connector appears in the tools list; first invocation triggers
the Meta OAuth flow.

Reference:
https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp

## OpenClaw

Register at user scope (lives in `~/.openclaw/openclaw.json`):

```bash
bash /Users/gyusupsim/Projects/tools/meta-ads-cli/meta-ads-mcp/register-openclaw.sh
```

Or directly:

```bash
openclaw mcp set meta-ads '{"type":"http","url":"https://mcp.facebook.com/ads"}'
```

OpenClaw normalizes `type: http` to `transport: streamable-http` in storage —
both forms accept the same OAuth flow on first tool call.

Verify:

```bash
openclaw mcp show meta-ads
openclaw mcp list
```

Remove:

```bash
openclaw mcp unset meta-ads
```

## Other clients

The Meta help page calls this URL "the remote MCP server URL for our ads MCP
server across all currently supported AI agents." Any MCP-capable client that
accepts an HTTP endpoint will work — point it at `https://mcp.facebook.com/ads`
and complete the OAuth flow when prompted.

| Client          | Where to add the URL                                  |
|-----------------|-------------------------------------------------------|
| Claude Code     | `claude mcp add --transport http meta-ads <URL>`      |
| Claude Desktop  | `claude_desktop_config.json` → `mcpServers.meta-ads`  |
| OpenClaw        | `openclaw mcp set meta-ads '{"type":"http","url":"<URL>"}'` |
| Cursor          | Settings → MCP → Add Server (HTTP)                    |
| ChatGPT (Apps)  | Connectors → Add custom MCP                           |

## OAuth scope

You'll grant the agent permission against your Meta user (not a system user).
Access mirrors what your Meta account can already do in Ads Manager — no
additional permissions are granted to anyone outside of you. Revoke any time
at https://business.facebook.com/settings/connected-apps .

## Capabilities (per Meta help page)

The MCP server enables the agent to:

- **Comprehensive reporting** — pull insights, breakdowns, performance trends
- **Ad creation & optimization** — draft and refine campaigns, ad sets, ads,
  creatives
- **Account hygiene** — review status, pause underperformers, rebalance budgets

For low-level scripting / CI use, prefer the CLI in `../meta-ads-official-cli/`
(deterministic, scriptable, system-user auth). Use this MCP when you want a
chat-driven interface.

## Troubleshooting

- **"Connector unavailable" / OAuth loop** — log out of unrelated Meta accounts
  in the same browser, retry. Meta's OAuth picks the active session.
- **No ad accounts visible** — your Meta user must already have access to the
  ad account in Business Manager. The MCP doesn't grant new asset access; it
  reflects what your account already sees.
- **Want a different account** — `claude mcp remove meta-ads`, then re-add
  while logged into the right Meta user.
