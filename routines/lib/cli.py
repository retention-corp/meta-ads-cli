"""Subprocess wrapper around the official `meta` CLI.

Hard dependency on the venv at meta-ads-official-cli/.venv. We do NOT call the
Marketing API directly — every Meta interaction goes through the CLI so the
auth, pagination, retry, and version handling is delegated to Meta's own tool.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
META_BIN = ROOT / "meta-ads-official-cli" / ".venv" / "bin" / "meta"


class CliError(RuntimeError):
    pass


def _run(args: list[str], timeout: int = 60) -> str:
    if not META_BIN.exists():
        raise CliError(f"meta CLI not found at {META_BIN}. Run install first.")
    proc = subprocess.run(
        [str(META_BIN), *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(ROOT / "meta-ads-official-cli"),
    )
    if proc.returncode != 0:
        raise CliError(f"meta {' '.join(args)} failed (exit {proc.returncode}): {proc.stderr.strip()}")
    return proc.stdout


def json_call(*args: str, timeout: int = 60) -> Any:
    """Run `meta --output json <args>` and parse stdout as JSON."""
    out = _run(["--output", "json", *args], timeout=timeout)
    try:
        return json.loads(out)
    except json.JSONDecodeError as e:
        raise CliError(f"meta returned non-JSON output: {out[:500]}") from e


def insights(
    *,
    ad_id: str | None = None,
    adset_id: str | None = None,
    campaign_id: str | None = None,
    date_preset: str = "last_7d",
    since: str | None = None,
    until: str | None = None,
    time_increment: str | None = None,
    breakdown: str | None = None,
    fields: list[str] | None = None,
    limit: int = 500,
) -> list[dict]:
    """Thin wrapper around `meta ads insights get` with sane defaults."""
    args: list[str] = ["ads", "insights", "get"]
    if since and until:
        args += ["--since", since, "--until", until]
    else:
        args += ["--date-preset", date_preset]
    if time_increment:
        args += ["--time-increment", time_increment]
    if breakdown:
        args += ["--breakdown", breakdown]
    if fields:
        args += ["--fields", ",".join(fields)]
    if ad_id:
        args += ["--ad-id", ad_id]
    if adset_id:
        args += ["--adset-id", adset_id]
    if campaign_id:
        args += ["--campaign-id", campaign_id]
    args += ["-l", str(limit)]
    payload = json_call(*args)
    return payload.get("data", []) if isinstance(payload, dict) else (payload or [])


def list_ads(limit: int = 200) -> list[dict]:
    return json_call("ads", "ad", "list", "--limit", str(limit)) or []


def list_adsets(limit: int = 200) -> list[dict]:
    return json_call("ads", "adset", "list", "--limit", str(limit)) or []


def list_campaigns(limit: int = 200) -> list[dict]:
    return json_call("ads", "campaign", "list", "--limit", str(limit)) or []


def get_ad(ad_id: str) -> dict:
    return json_call("ads", "ad", "get", ad_id)


def get_adset(adset_id: str) -> dict:
    return json_call("ads", "adset", "get", adset_id)


def get_campaign(campaign_id: str) -> dict:
    return json_call("ads", "campaign", "get", campaign_id)


def update_ad(ad_id: str, **fields: str) -> dict:
    args = ["ads", "ad", "update", ad_id]
    for k, v in fields.items():
        args += [f"--{k.replace('_', '-')}", str(v)]
    return json_call(*args)


def pause_ad(ad_id: str, dry_run: bool = True) -> dict | None:
    if dry_run:
        return {"dry_run": True, "would_run": f"meta ads ad update {ad_id} --status PAUSED"}
    return update_ad(ad_id, status="PAUSED")


def sum_action(actions: list[dict] | None, action_type: str) -> float:
    if not actions:
        return 0.0
    return sum(float(a.get("value", 0) or 0) for a in actions if a.get("action_type") == action_type)
