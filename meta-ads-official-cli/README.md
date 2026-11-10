# meta-ads-official-cli

Standalone install of Meta's official **Ads CLI** (`meta-ads` on PyPI), kept in
its own venv to avoid colliding with the parent `meta-ads-cli` (YAML deployer)
project.

- Docs: https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/ads-cli-overview
- PyPI: https://pypi.org/project/meta-ads/
- Installed version: `1.0.1`
- Entrypoint: `meta` (with subcommands `meta ads ...` and `meta auth ...`)

## What's here

```
meta-ads-official-cli/
├── .venv/        # Python 3.13 venv with meta-ads installed (gitignored)
└── README.md
```

## Activate

bash/zsh:

```bash
source /Users/gyusupsim/Projects/tools/meta-ads-cli/meta-ads-official-cli/.venv/bin/activate
```

fish:

```fish
source /Users/gyusupsim/Projects/tools/meta-ads-cli/meta-ads-official-cli/.venv/bin/activate.fish
```

Verify:

```
meta --version       # meta, version 1.0.1
meta --help
meta ads --help
```

## Configure

Auth is via a Meta system user access token. Set environment variables (in
`.env` or your shell):

| Variable        | Required                | Purpose                                            |
|-----------------|-------------------------|----------------------------------------------------|
| `ACCESS_TOKEN`  | Yes                     | System user access token                           |
| `AD_ACCOUNT_ID` | Yes (most commands)     | Ad account ID, e.g. `act_123456`                   |
| `BUSINESS_ID`   | No                      | Default business ID (catalog/dataset commands)     |

Resolution precedence (highest first):
CLI flag (e.g. `--ad-account-id`) → shell env → project `.env` → user-level `~/.config/meta/`

Check status:

```
meta auth status
```

## Usage examples

```
meta ads campaign list
meta ads adset get 123456 --output json
meta ads insights get --date-preset last_7d
meta ads creative create --name "My Ad" --page-id <PAGE_ID> --image ./banner.jpg
```

Top-level command groups: `ad`, `adaccount`, `adset`, `campaign`, `catalog`,
`creative`, `dataset`, `insights`, `page`, `product-feed`, `product-item`,
`product-set`.

## Reinstall / upgrade

```bash
cd /Users/gyusupsim/Projects/tools/meta-ads-cli/meta-ads-official-cli
source .venv/bin/activate
uv pip install --upgrade meta-ads
```

## Recreate venv from scratch

```bash
cd /Users/gyusupsim/Projects/tools/meta-ads-cli/meta-ads-official-cli
rm -rf .venv
uv venv --python 3.13 .venv
source .venv/bin/activate
uv pip install meta-ads
```
