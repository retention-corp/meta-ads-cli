"""Slack incoming-webhook poster. Read-only (no interactive callbacks).

Set SLACK_WEBHOOK_URL in your env or .env. If unset, falls back to stdout
so routines remain runnable for the video shoot without Slack configured.
"""
from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

ROUTINES = Path(__file__).resolve().parent.parent


def _load_env():
    env_path = ROUTINES / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            v = v.strip().strip("'").strip('"')
            os.environ.setdefault(k.strip(), v)


_load_env()


def post(text: str, *, channel: str | None = None, blocks: list | None = None) -> bool:
    """Post a message. Returns True on success, False if no webhook (still prints)."""
    webhook = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook:
        print(f"\n[slack:stdout {channel or 'default'}]\n{text}\n")
        return False
    payload: dict = {"text": text}
    if channel:
        payload["channel"] = channel
    if blocks:
        payload["blocks"] = blocks
    req = urllib.request.Request(
        webhook,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status == 200
    except Exception as e:
        print(f"[slack:error] {e}\nFell back to stdout:\n{text}\n")
        return False


def kv_block(items: list[tuple[str, str]]) -> str:
    width = max(len(k) for k, _ in items) + 2
    return "\n".join(f"{k.ljust(width)} {v}" for k, v in items)
