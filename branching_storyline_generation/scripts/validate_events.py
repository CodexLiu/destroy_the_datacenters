#!/usr/bin/env python3
"""Validate events.json for completeness, 2025 timeline, and distribution targets."""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
EVENTS_PATH = ROOT / "content" / "events.json"


@dataclass
class Targets:
    total_events: int
    phases: Dict[str, int]
    stat_minimums: Dict[str, int]


def load_events() -> Dict:
    if not EVENTS_PATH.exists():
        print(f"ERROR: {EVENTS_PATH} does not exist.")
        sys.exit(1)
    try:
        with EVENTS_PATH.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Failed to parse {EVENTS_PATH}: {exc}")
        sys.exit(1)


def parse_targets(data: Dict) -> Targets:
    targets = data.get("targets") or {}
    phases = targets.get("phases") or {}
    stat_minimums = targets.get("statCoverageMinimums") or {}
    try:
        return Targets(
            total_events=int(targets.get("totalEvents")),
            phases={k: int(v) for k, v in phases.items()},
            stat_minimums={k: int(v) for k, v in stat_minimums.items()},
        )
    except (TypeError, ValueError):
        print("ERROR: targets section is missing or malformed; ensure integers are provided.")
        sys.exit(1)


def ensure_style(data: Dict) -> None:
    style = data.get("style") or {}
    year = style.get("year")
    template = style.get("imagePromptTemplate", "")
    if year != 2025:
        print(f"ERROR: style.year must be 2025, found {year!r}.")
        sys.exit(1)
    required_tokens = ["retro futurist", "light cyan", "persimmon", "2025"]
    if not all(token in template for token in required_tokens):
        print("ERROR: imagePromptTemplate missing required tokens (retro futurist, light cyan, persimmon, 2025).")
        sys.exit(1)


def collect_primary_stats(event: Dict) -> List[str]:
    stats = list(event.get("primaryStats") or [])
    # Infer from effects if not provided explicitly.
    for effect in event.get("effects", []) + [eff for choice in event.get("choices", []) for eff in choice.get("effects", [])]:
        target = effect.get("target", {})
        if target.get("type") == "global":
            stats.append(target.get("key"))
        elif target.get("type") == "datacenter":
            stats.append("defense")
        elif target.get("type") == "datacenters":
            stats.append(target.get("key"))
        elif target.get("type") == "inventory":
            stats.append("inventory")
    return [s for s in stats if s]


def validate_event(event: Dict, index: int) -> Dict[str, int]:
    required_fields = ["id", "title", "body", "year", "phase", "choices", "imagePrompt"]
    missing = [field for field in required_fields if not event.get(field)]
    if missing:
        print(f"ERROR: event index {index} ({event.get('id')}) missing fields: {', '.join(missing)}")
        sys.exit(1)
    if event.get("year") != 2025:
        print(f"ERROR: event {event['id']} year must be 2025, found {event.get('year')!r}.")
        sys.exit(1)
    phase = event.get("phase")
    if phase not in {"early", "mid", "late", "endgame"}:
        print(f"ERROR: event {event['id']} has invalid phase {phase!r}; expected early/mid/late/endgame.")
        sys.exit(1)
    prompt = event.get("imagePrompt", "").lower()
    for token in ("retro futurist", "2025", "light", "persimmon"):
        if token not in prompt:
            print(f"ERROR: event {event['id']} imagePrompt missing token '{token}'.")
            sys.exit(1)
    stats = collect_primary_stats(event)
    if not stats:
        print(f"ERROR: event {event['id']} does not declare any primary stat impacts.")
        sys.exit(1)
    return {
        "phase": phase,
        "stats": {stat for stat in stats}
    }


def main() -> None:
    data = load_events()
    ensure_style(data)
    events: List[Dict] = data.get("events") or []
    targets = parse_targets(data)

    if len(events) < targets.total_events:
        print(f"ERROR: Only {len(events)} events defined; target is {targets.total_events}.")
        sys.exit(1)

    phase_counts: Dict[str, int] = {phase: 0 for phase in targets.phases}
    stat_counts: Dict[str, int] = {stat: 0 for stat in targets.stat_minimums}

    for idx, event in enumerate(events):
        info = validate_event(event, idx)
        phase_counts[info["phase"]] = phase_counts.get(info["phase"], 0) + 1
        for stat in info["stats"]:
            if stat in stat_counts:
                stat_counts[stat] = stat_counts.get(stat, 0) + 1

    phase_failures = [f"{phase}: {count}/{targets.phases[phase]}" for phase, count in phase_counts.items() if count < targets.phases.get(phase, 0)]
    if phase_failures:
        print("ERROR: Phase distribution incomplete -> " + ", ".join(phase_failures))
        sys.exit(1)

    stat_failures = [f"{stat}: {count}/{targets.stat_minimums[stat]}" for stat, count in stat_counts.items() if count < targets.stat_minimums.get(stat, 0)]
    if stat_failures:
        print("ERROR: Stat coverage incomplete -> " + ", ".join(stat_failures))
        sys.exit(1)

    print("OK: events.json meets 2025 style, count, and distribution targets.")


if __name__ == "__main__":
    main()
