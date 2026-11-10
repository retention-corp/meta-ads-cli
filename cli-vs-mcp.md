# Meta Ads — CLI vs MCP: when to use which

Two official tools from Meta. Same Marketing API underneath. Different
interfaces, different auth models, different risk profiles. Pick the one that
matches the **shape of the work**, not the one that's "newer."

- **CLI** (`meta-ads-official-cli/`) — `meta ads <resource> <action>` with a
  long-lived system user token.
- **MCP** (`meta-ads-mcp/`) — `https://mcp.facebook.com/ads` over HTTP, OAuth
  bound to your Meta user, called by an AI agent in conversation.

## TL;DR — pick by shape of work

| Shape of work                          | Tool        |
|----------------------------------------|-------------|
| Determinism, scripts, cron, CI/CD      | **CLI**     |
| Bulk / loop / pipeline (`xargs`, `jq`) | **CLI**     |
| Audit trail, version-control of intent | **CLI**     |
| Reproducibility (same input = output)  | **CLI**     |
| Exploration, "what's going on?"        | **MCP**     |
| Cross-domain reasoning + ad action     | **MCP**     |
| Slack-style "pause this and rebudget"  | **MCP**     |
| Anything you'd ask an analyst to do    | **MCP**     |
| Onboarding a new ad account quickly    | **MCP**     |
| Anything destructive (delete, archive) | **CLI** (with `--dry-run`-style review) |

If you'd say it in Korean to a junior marketer at the next desk → **MCP**.
If you'd write it in a Slack DM to a backend engineer → **CLI**.

## Decision matrix

| Use case                                                      | CLI | MCP | Notes                                                          |
|---------------------------------------------------------------|:---:|:---:|----------------------------------------------------------------|
| Daily / weekly insights pull → CSV / dashboard                | ✅  | ⛔  | Loop `meta ads insights get` per ad, store JSON, render HTML   |
| Generate a perf dashboard *right now*                         | ✅  | ✅  | CLI for the data, MCP if you also want narrative analysis     |
| "Why did spend drop yesterday?" diagnostic                    | ⛔  | ✅  | MCP can pull insights *and* explain; CLI just returns rows     |
| Pause every ad with ROAS < 1.0 across last 7d                 | ✅  | ⚠️  | CLI for safety: list, filter, batch update with explicit flags. MCP fine if you review each step. |
| Bulk creative upload (50 images → 50 ads)                     | ✅  | ⛔  | Loop with `meta ads creative create --image …` in a shell      |
| Prototype a new campaign with copy + targeting iteration      | ⚠️  | ✅  | MCP shines: agent edits, you respond, agent re-edits           |
| One-off SQL-like question ("top 5 ads by CPA last 30d")       | ⚠️  | ✅  | MCP: ask in plain language. CLI works but you'll write a script. |
| CI step that creates an ad after a marketing site deploy      | ✅  | ⛔  | Deterministic execution, no human in the loop                  |
| Backfill historical insights into a warehouse                 | ✅  | ⛔  | Long-running, deterministic, paged                             |
| Onboarding: explain my ad account to me                       | ⛔  | ✅  | Conversational walkthrough beats reading raw JSON              |
| Catalog management: bulk import 10k SKUs                      | ✅  | ⛔  | CLI + product-feed                                             |
| Moving budget between adsets at 9am every weekday             | ✅  | ⛔  | Cron + CLI, no agent needed                                    |
| Handing off to a teammate (write a runbook)                   | ✅  | ⛔  | Commands paste; conversations don't                            |
| You don't yet know what you want                              | ⛔  | ✅  | MCP is exploration mode; CLI is execution mode                 |

⚠️ = works but you should think about whether the other tool is safer.

## Side-by-side properties

| Property                | CLI                                       | MCP                                       |
|-------------------------|-------------------------------------------|-------------------------------------------|
| Identity                | System user (long-lived token)            | Your Meta user (OAuth, browser-bound)     |
| Token lifetime          | Effectively forever (no expiry)           | Browser session + refresh                 |
| Where token lives       | `.env` file you control                   | Inside the AI client's config             |
| Permissions             | Whatever scopes you minted on the token   | `ads_management ads_read catalog_management business_management` |
| Rate limit attribution  | App + system user                         | Per Meta user                             |
| Audit                   | Shell history + JSON output               | Agent transcript                          |
| Deterministic?          | Yes (same args → same call)               | No (LLM may rephrase, retry, branch)      |
| Best for non-tech user  | No                                        | Yes                                       |
| Composes with `jq`/`xargs`? | Yes                                  | No                                         |
| Side-effect safety      | High (you literally type the verb)        | Medium (agent may chain unexpectedly)     |
| Latency                 | One HTTP call                             | One LLM round trip + one MCP call         |
| Cost                    | Free (CLI) + Marketing API quota          | LLM tokens + Marketing API quota          |
| Resumes after laptop reboot? | Yes                                  | OAuth re-auth may be needed              |
| Works in CI / a Docker container? | Yes (token in env)              | No (OAuth needs a browser)                |
| Works on a phone?       | No                                        | Yes (any MCP-aware app)                   |

## Hybrid patterns

These are the patterns that work best in practice — pick one.

### 1. CLI for action, MCP for exploration

Use the MCP-driven chat to figure out *what* to do — "show me the ads with
spend > $50 and zero purchases last 7d." Once you've decided, ask the agent to
emit the equivalent CLI commands and run them yourself. The CLI invocation is
the audit trail; the chat is the scratchpad.

### 2. MCP-supervised CLI loops

The agent monitors a dashboard generated from CLI data on a cadence, and when
it spots a regression, it proposes the CLI command to fix it. Human approves,
the CLI runs in a shell. The MCP is the watcher; the CLI is the hand.

### 3. CLI in CI, MCP at the desk

CI does the boring stuff — daily dashboard, weekly creative wear-out report,
budget pacing checks — all with the CLI. The MCP only shows up for the human
ad-hoc work in front of a chat window. Two tools, two halves of the workflow,
no overlap.

## Anti-patterns

- **MCP for cron-like recurring jobs.** OAuth tokens silently expire, browsers
  go to sleep, the agent context resets. Use the CLI.
- **CLI for "explore my account."** You'll spend more time writing `--fields`
  and parsing JSON than thinking. Use the MCP.
- **Letting the agent run destructive commands without review.** The MCP can
  pause campaigns. That's fine for "pause this one ad we're discussing."
  Don't let it `delete` based on inferred intent.
- **Mixing token sources in the same script.** Pick one identity. CLI scripts
  use the system user token; chat actions use your OAuth. Don't blur the line.
- **Treating MCP output as authoritative numbers.** The agent may summarize
  rounded values. For the actual board report, pull the same query via CLI.

## Auth model — the part that bites you

| Failure mode                            | CLI symptom                              | MCP symptom                              |
|-----------------------------------------|------------------------------------------|------------------------------------------|
| Token revoked in Business Suite          | `Not authenticated`                       | `Failed to connect`                       |
| Permissions on ad account changed       | `OAuthException` 200 / 100                | OAuth re-prompt                           |
| Wrong account selected                  | `act_X does not exist` (wrong env var)    | Browser logged into wrong Meta user       |
| Token leaked                            | Anyone with the token can do anything    | Browser session, harder to exfiltrate     |

The CLI's token is **portable, long-lived, and high-blast-radius** — store it
the same way you'd store an AWS root key. The MCP's OAuth is bound to your
browser session and easier to revoke (`business.facebook.com/settings/connected-apps`).

## When to actually use both

You will end up using both. The split:

```
        ┌─────────────────────────────────────────────────────┐
        │                                                     │
        │   exploration / one-off question / chat-shaped      │
        │                                                     │
        │                       MCP                           │
        │                                                     │
        ├─────────────────────────────────────────────────────┤
        │                                                     │
        │   recurring / scripted / CI / batch / scheduled     │
        │                                                     │
        │                       CLI                           │
        │                                                     │
        └─────────────────────────────────────────────────────┘
```

The mistake is using MCP because it's novel, or CLI because it's safer-feeling.
Match the tool to the work.

## Pointers

- CLI install + setup: `meta-ads-official-cli/README.md`
- MCP install + setup: `meta-ads-mcp/README.md`
- Help center (canonical): https://www.facebook.com/business/help/1456422242197840
- CLI docs: https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/ads-cli-overview
