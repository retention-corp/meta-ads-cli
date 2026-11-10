"""Routine 4: Creative Testing Pipeline.

Reads hooks / bodies / CTAs from the vault folder, generates combinations,
optionally creates ads via the CLI. **Default mode = dry-run** — prints what
would be created without touching the account. Pass `--execute` to actually
create ads (all PAUSED, never auto-active — second human gate before launch).

Folder layout expected:
  routines/vault/hooks/<image_or_video_files>
  routines/vault/bodies/<text files, one per body>
  routines/vault/ctas/<one of LEARN_MORE | SIGN_UP | SHOP_NOW | …>

Empty vault = empty plan. The script does not invent assets; it only
combines what's actually staged.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import dataclass, asdict
from itertools import product
from pathlib import Path

import cli  # type: ignore[import-not-found]

ROUTINES = Path(__file__).resolve().parent.parent
VAULT = ROUTINES / "vault"


@dataclass
class Combo:
    hash: str
    hook_path: str
    body_text: str
    cta: str
    name: str


def discover() -> tuple[list[Path], list[str], list[str]]:
    hook_files = sorted(p for p in (VAULT / "hooks").glob("*") if p.is_file() and not p.name.startswith("."))
    bodies: list[str] = []
    for f in sorted((VAULT / "bodies").glob("*.txt")):
        bodies.append(f.read_text().strip())
    ctas = []
    for f in sorted((VAULT / "ctas").glob("*")):
        if f.is_file() and not f.name.startswith("."):
            ctas.append(f.stem.upper())
    return hook_files, bodies, ctas


def build_combos(hooks: list[Path], bodies: list[str], ctas: list[str], prefix: str) -> list[Combo]:
    combos: list[Combo] = []
    for hook, body, cta in product(hooks, bodies, ctas):
        h = hashlib.sha1(f"{hook.name}|{body[:30]}|{cta}".encode()).hexdigest()[:8]
        combos.append(
            Combo(
                hash=h,
                hook_path=str(hook),
                body_text=body,
                cta=cta,
                name=f"{prefix}_{h}",
            )
        )
    return combos


def plan(prefix: str = "test") -> dict:
    hooks, bodies, ctas = discover()
    combos = build_combos(hooks, bodies, ctas, prefix)
    return {
        "prefix": prefix,
        "vault": {"hooks": [str(h) for h in hooks], "bodies": len(bodies), "ctas": ctas},
        "combinations": len(combos),
        "combos": [asdict(c) for c in combos],
    }


def execute(plan_dict: dict, adset_id: str, page_id: str, link: str, headline: str) -> list[dict]:
    """Real create. All ads land as PAUSED."""
    results = []
    for combo in plan_dict["combos"]:
        # 1. upload image
        img = cli.json_call("ads", "upload-ad-image", "--image", combo["hook_path"])
        image_hash = (img or {}).get("hash") or (img or {}).get("image_hash")
        if not image_hash:
            results.append({"combo": combo["hash"], "status": "image_upload_failed", "raw": img})
            continue
        # 2. create creative
        creative_args = [
            "ads", "creative", "create",
            "--name", f"creative_{combo['name']}",
            "--page-id", page_id,
            "--image-hash", image_hash,
            "--message", combo["body_text"],
            "--headline", headline,
            "--cta", combo["cta"],
            "--link", link,
        ]
        cr = cli.json_call(*creative_args)
        creative_id = (cr or {}).get("id")
        if not creative_id:
            results.append({"combo": combo["hash"], "status": "creative_failed", "raw": cr})
            continue
        # 3. create ad PAUSED
        ad = cli.json_call(
            "ads", "ad", "create",
            "--name", combo["name"],
            "--adset-id", adset_id,
            "--creative-id", creative_id,
            "--status", "PAUSED",
        )
        results.append({"combo": combo["hash"], "ad_id": ad.get("id"), "status": "created_paused"})
    return results


def to_slack_text(plan_dict: dict, executed: list[dict] | None = None) -> str:
    head = f":art: *크리에이티브 테스트 배치 — {plan_dict['prefix']}*"
    body = (
        f"vault: hooks {len(plan_dict['vault']['hooks'])}개 × "
        f"bodies {plan_dict['vault']['bodies']}개 × CTAs {len(plan_dict['vault']['ctas'])}개 "
        f"= {plan_dict['combinations']} 조합"
    )
    if executed is None:
        return f"{head}\n{body}\n_dry-run — 광고 생성 없음. 실 생성하려면 --execute (전부 PAUSED 상태로 생성됨)._"
    ok = sum(1 for r in executed if r["status"] == "created_paused")
    bad = len(executed) - ok
    return f"{head}\n{body}\n:white_check_mark: PAUSED 광고 {ok}개 생성. :x: {bad}개 실패.\n_전부 PAUSED 상태. 검토 후 활성화하세요._"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", default="test")
    parser.add_argument("--execute", action="store_true", help="actually create ads (default: dry-run)")
    parser.add_argument("--adset-id", default=os.environ.get("CREATIVE_TEST_ADSET_ID"))
    parser.add_argument("--page-id", default=os.environ.get("META_PAGE_ID", "1534124060211977"))
    parser.add_argument("--link", default=os.environ.get("CREATIVE_LINK", "https://example.com"))
    parser.add_argument("--headline", default=os.environ.get("CREATIVE_HEADLINE", "Test"))
    args = parser.parse_args()

    plan_dict = plan(prefix=args.prefix)
    out = ROUTINES / "reports" / f"creative_plan_{args.prefix}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(plan_dict, ensure_ascii=False, indent=2))
    print(f"plan written → {out} ({plan_dict['combinations']} combinations)")

    executed = None
    if args.execute:
        if not args.adset_id:
            print("ERROR: --adset-id required when --execute is set")
            raise SystemExit(2)
        executed = execute(plan_dict, args.adset_id, args.page_id, args.link, args.headline)
        out_x = ROUTINES / "reports" / f"creative_executed_{args.prefix}.json"
        out_x.write_text(json.dumps(executed, ensure_ascii=False, indent=2))
        print(f"executed log → {out_x}")

    from slack import post  # type: ignore[import-not-found]

    post(to_slack_text(plan_dict, executed), channel="#creative-review")
