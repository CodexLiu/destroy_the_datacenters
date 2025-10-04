#!/usr/bin/env python3
"""Validate agents.json roster size, role split, and 2025 style."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
AGENTS_PATH = ROOT / "content" / "agents.json"

ALLOWED_ROLES = {"operative", "logistics", "tech"}


def load_agents() -> Dict:
    if not AGENTS_PATH.exists():
        print(f"ERROR: {AGENTS_PATH} does not exist.")
        sys.exit(1)
    try:
        with AGENTS_PATH.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Failed to parse {AGENTS_PATH}: {exc}")
        sys.exit(1)


def ensure_style(data: Dict) -> Dict:
    style = data.get("style") or {}
    if style.get("year") != 2025:
        print("ERROR: style.year must be 2025.")
        sys.exit(1)
    return data.get("targets") or {}


def validate_agent(agent: Dict, index: int) -> str:
    required_fields = ["id", "name", "role", "description", "imagePrompt", "successRate", "risk"]
    missing = [field for field in required_fields if agent.get(field) in (None, "")]
    if missing:
        print(f"ERROR: agent index {index} missing fields: {', '.join(missing)}")
        sys.exit(1)
    role = agent.get("role")
    if role not in ALLOWED_ROLES:
        print(f"ERROR: agent {agent['id']} has invalid role {role!r}.")
        sys.exit(1)
    prompt = (agent.get("imagePrompt") or "").lower()
    for token in ("retro futurist", "2025", "light", "persimmon"):
        if token not in prompt:
            print(f"ERROR: agent {agent['id']} imagePrompt missing token '{token}'.")
            sys.exit(1)
    primary = agent.get("primaryEffects") or []
    if not primary:
        print(f"ERROR: agent {agent['id']} missing primaryEffects for balancing.")
        sys.exit(1)
    try:
        float(agent.get("successRate"))
        float(agent.get("risk"))
    except (TypeError, ValueError):
        print(f"ERROR: agent {agent['id']} successRate/risk must be numeric.")
        sys.exit(1)
    return role


def main() -> None:
    data = load_agents()
    targets = ensure_style(data)

    agents = data.get("agents") or []
    total_target = int(targets.get("totalAgents", 0) or 0)
    if len(agents) < total_target:
        print(f"ERROR: Only {len(agents)} agents defined; target is {total_target}.")
        sys.exit(1)

    role_targets = targets.get("roles", {})
    role_counts: Dict[str, int] = {role: 0 for role in role_targets}

    for idx, agent in enumerate(agents):
        role = validate_agent(agent, idx)
        role_counts[role] = role_counts.get(role, 0) + 1

    role_failures = [
        f"{role}: {count}/{role_targets[role]}"
        for role, count in role_counts.items()
        if count < role_targets.get(role, 0)
    ]
    if role_failures:
        print("ERROR: Role distribution incomplete -> " + ", ".join(role_failures))
        sys.exit(1)

    print("OK: agents.json meets 2025 style, count, and role targets.")


if __name__ == "__main__":
    main()
