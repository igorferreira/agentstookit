#!/usr/bin/env python3
"""CLF-C02 exam-readiness progress tracker.

Stdlib-only. All output is JSON for agent parsing.
Data file: $HERMES_HOME/skills/aws-ccp-tutor/data/progress.json
"""

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

_HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
DATA_DIR = _HERMES_HOME / "skills" / "aws-ccp-tutor" / "data"
PROGRESS_FILE = DATA_DIR / "progress.json"

# Official CLF-C02 domain weights (% of scored content)
DOMAIN_WEIGHTS = {
    "D1": 24,
    "D2": 30,
    "D3": 34,
    "D4": 12,
}
DOMAIN_NAMES = {
    "D1": "Cloud Concepts",
    "D2": "Security and Compliance",
    "D3": "Cloud Technology and Services",
    "D4": "Billing, Pricing, and Support",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _empty_store() -> dict:
    return {
        "version": 1,
        "domains": {
            d: {"correct": 0, "total": 0} for d in DOMAIN_WEIGHTS
        },
        "history": [],
    }


def _load() -> dict:
    if not PROGRESS_FILE.exists():
        return _empty_store()
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict) or "domains" not in data:
            return _empty_store()
        for d in DOMAIN_WEIGHTS:
            data["domains"].setdefault(d, {"correct": 0, "total": 0})
        data.setdefault("history", [])
        return data
    except (json.JSONDecodeError, OSError):
        return _empty_store()


def _save(data: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=DATA_DIR, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, PROGRESS_FILE)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _out(obj: object) -> None:
    json.dump(obj, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


def _accuracy(domain: dict) -> float:
    if domain["total"] == 0:
        return 0.0
    return domain["correct"] / domain["total"]


def _domain_stats(data: dict) -> dict:
    out = {}
    for d, weight in DOMAIN_WEIGHTS.items():
        dom = data["domains"][d]
        out[d] = {
            "name": DOMAIN_NAMES[d],
            "weight_pct": weight,
            "correct": dom["correct"],
            "total": dom["total"],
            "accuracy_pct": round(_accuracy(dom) * 100, 1),
        }
    return out


# ── Subcommands ──────────────────────────────────────────────────────────────

def cmd_record(args: argparse.Namespace) -> None:
    if args.correct > args.total:
        _out({"ok": False, "error": "--correct cannot exceed --total"})
        sys.exit(1)

    data = _load()
    dom = data["domains"][args.domain]
    dom["correct"] += args.correct
    dom["total"] += args.total

    data["history"].append({
        "at": _now_iso(),
        "domain": args.domain,
        "correct": args.correct,
        "total": args.total,
        "source": args.source,
    })

    _save(data)
    _out({"ok": True, "domain": args.domain, "updated": dom})


def cmd_stats(args: argparse.Namespace) -> None:
    data = _load()
    domains = _domain_stats(data)
    total_correct = sum(d["correct"] for d in domains.values())
    total_questions = sum(d["total"] for d in domains.values())
    overall_pct = round((total_correct / total_questions * 100), 1) if total_questions else 0.0

    _out({
        "ok": True,
        "domains": domains,
        "overall": {
            "correct": total_correct,
            "total": total_questions,
            "accuracy_pct": overall_pct,
        },
        "sessions_recorded": len(data["history"]),
    })


def cmd_weak(args: argparse.Namespace) -> None:
    data = _load()
    domains = _domain_stats(data)

    scored = []
    for d, info in domains.items():
        if info["total"] == 0:
            # Never practiced: treat as maximal need, weighted by exam weight.
            priority = info["weight_pct"] / 100.0
            status = "not_started"
        else:
            gap = 1 - (info["accuracy_pct"] / 100.0)
            priority = (info["weight_pct"] / 100.0) * gap
            status = "practiced"
        scored.append({
            "domain": d,
            "name": info["name"],
            "weight_pct": info["weight_pct"],
            "accuracy_pct": info["accuracy_pct"],
            "attempts": info["total"],
            "status": status,
            "priority_score": round(priority, 4),
        })

    scored.sort(key=lambda x: x["priority_score"], reverse=True)
    _out({"ok": True, "ranked": scored})


def cmd_reset(args: argparse.Namespace) -> None:
    _save(_empty_store())
    _out({"ok": True, "reset": True})


# ── CLI ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="CLF-C02 exam-readiness progress tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    p_record = sub.add_parser("record", help="Record quiz/lesson results for a domain")
    p_record.add_argument("--domain", required=True, choices=list(DOMAIN_WEIGHTS))
    p_record.add_argument("--correct", required=True, type=int)
    p_record.add_argument("--total", required=True, type=int)
    p_record.add_argument("--source", default="quiz", choices=["quiz", "lesson", "review"])

    sub.add_parser("stats", help="Show accuracy per domain and overall")
    sub.add_parser("weak", help="Rank domains by study priority (weight x gap)")
    sub.add_parser("reset", help="Wipe all recorded progress")

    args = parser.parse_args()
    cmd_map = {
        "record": cmd_record,
        "stats": cmd_stats,
        "weak": cmd_weak,
        "reset": cmd_reset,
    }
    cmd_map[args.command](args)


if __name__ == "__main__":
    main()
