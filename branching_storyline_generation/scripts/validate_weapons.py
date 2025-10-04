#!/usr/bin/env python3
"""Validate weapons.json against balance distribution and style targets."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
WEAPONS_PATH = ROOT / "content" / "weapons.json"

ALLOWED_CATEGORIES = {"improvised", "drone", "cyber", "social", "support"}
ALLOWED_DAMAGE_TYPES = {"explosive", "incendiary", "cyber", "social", "sabotage"}


def load_weapons() -> Dict:
    if not WEAPONS_PATH.exists():
        print(f"ERROR: {WEAPONS_PATH} does not exist.")
        sys.exit(1)
    try:
        with WEAPONS_PATH.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Failed to parse {WEAPONS_PATH}: {exc}")
        sys.exit(1)


def ensure_style(data: Dict) -> None:
    style = data.get("style") or {}
    if style.get("year") != 2025:
        print("ERROR: style.year must be 2025.")
        sys.exit(1)
    template = style.get("imagePromptTemplate", "")
    for token in ("retro futurist", "light cyan", "persimmon", "2025"):
        if token not in template:
            print("ERROR: imagePromptTemplate missing required tokens for consistent art style.")
            sys.exit(1)


def extract_targets(data: Dict) -> Dict:
    targets = data.get("targets") or {}
    required_keys = ["totalWeapons", "categories", "damageTierMinimums", "stealthBands", "heatModifiers", "agiImpact", "publicSupportModifiers"]
    if any(key not in targets for key in required_keys):
        print("ERROR: targets section is incomplete in weapons.json.")
        sys.exit(1)
    return targets


def damage_tier(damage: float) -> str:
    if damage <= 15:
        return "light"
    if damage <= 35:
        return "medium"
    if damage <= 60:
        return "heavy"
    return "catastrophic"


def validate_weapon(weapon: Dict, index: int) -> Dict:
    required_fields = ["id", "name", "category", "damage", "damageType", "imagePrompt"]
    missing = [field for field in required_fields if weapon.get(field) in (None, "")]
    if missing:
        print(f"ERROR: weapon index {index} missing fields: {', '.join(missing)}")
        sys.exit(1)
    category = weapon.get("category")
    if category not in ALLOWED_CATEGORIES:
        print(f"ERROR: weapon {weapon['id']} has invalid category {category!r}.")
        sys.exit(1)
    damage_type = weapon.get("damageType")
    if damage_type not in ALLOWED_DAMAGE_TYPES:
        print(f"ERROR: weapon {weapon['id']} has invalid damageType {damage_type!r}.")
        sys.exit(1)
    try:
        damage_value = float(weapon.get("damage"))
    except (TypeError, ValueError):
        print(f"ERROR: weapon {weapon['id']} damage must be numeric.")
        sys.exit(1)
    stealth = weapon.get("stealth")
    if stealth is None:
        print(f"ERROR: weapon {weapon['id']} missing stealth value for band checks.")
        sys.exit(1)
    prompt = weapon.get("imagePrompt", "").lower()
    for token in ("retro futurist", "2025", "light", "persimmon"):
        if token not in prompt:
            print(f"ERROR: weapon {weapon['id']} imagePrompt missing token '{token}'.")
            sys.exit(1)
    effects = weapon.get("effects", [])
    return {
        "category": category,
        "damage": damage_value,
        "stealth": float(stealth),
        "effects": effects,
    }


def analyze_effects(effects: List[Dict]) -> Dict[str, bool]:
    result = {
        "heat_increase": False,
        "heat_decrease": False,
        "agi": False,
        "public_support": False,
    }
    for effect in effects or []:
        target = effect.get("target", {})
        if target.get("type") != "global":
            continue
        key = target.get("key")
        try:
            value = float(effect.get("value", 0))
        except (TypeError, ValueError):
            continue
        if key == "heat":
            if value > 0:
                result["heat_increase"] = True
            elif value < 0:
                result["heat_decrease"] = True
        elif key in {"agiRate", "agiProgress"}:
            if value < 0:
                result["agi"] = True
        elif key == "publicSupport":
            if value != 0:
                result["public_support"] = True
    return result


def main() -> None:
    data = load_weapons()
    ensure_style(data)
    targets = extract_targets(data)
    weapons = data.get("weapons") or []

    total_target = int(targets["totalWeapons"])
    if len(weapons) < total_target:
        print(f"ERROR: Only {len(weapons)} weapons defined; target is {total_target}.")
        sys.exit(1)

    category_counts: Dict[str, int] = {key: 0 for key in targets["categories"]}
    damage_counts: Dict[str, int] = {key: 0 for key in targets["damageTierMinimums"]}
    stealth_high = stealth_low = 0
    heat_increase = heat_decrease = 0
    agi_reducers = 0
    public_support_mods = 0

    for idx, weapon in enumerate(weapons):
        info = validate_weapon(weapon, idx)
        category_counts[info["category"]] = category_counts.get(info["category"], 0) + 1
        tier = damage_tier(info["damage"])
        if tier in damage_counts:
            damage_counts[tier] = damage_counts.get(tier, 0) + 1
        if info["stealth"] >= 0.5:
            stealth_high += 1
        if info["stealth"] <= 0.2:
            stealth_low += 1
        effect_flags = analyze_effects(info["effects"])
        if effect_flags["heat_increase"]:
            heat_increase += 1
        if effect_flags["heat_decrease"]:
            heat_decrease += 1
        if effect_flags["agi"]:
            agi_reducers += 1
        if effect_flags["public_support"]:
            public_support_mods += 1

    category_failures = [
        f"{cat}: {count}/{targets['categories'][cat]}"
        for cat, count in category_counts.items()
        if count < targets["categories"].get(cat, 0)
    ]
    if category_failures:
        print("ERROR: Category distribution incomplete -> " + ", ".join(category_failures))
        sys.exit(1)

    damage_failures = [
        f"{tier}: {count}/{targets['damageTierMinimums'][tier]}"
        for tier, count in damage_counts.items()
        if count < targets["damageTierMinimums"].get(tier, 0)
    ]
    if damage_failures:
        print("ERROR: Damage tier distribution incomplete -> " + ", ".join(damage_failures))
        sys.exit(1)

    if stealth_high < targets["stealthBands"].get("highStealth", 0):
        print(f"ERROR: Only {stealth_high} high-stealth weapons; need {targets['stealthBands']['highStealth']}.")
        sys.exit(1)
    if stealth_low < targets["stealthBands"].get("lowStealth", 0):
        print(f"ERROR: Only {stealth_low} low-stealth weapons; need {targets['stealthBands']['lowStealth']}.")
        sys.exit(1)

    if heat_increase < targets["heatModifiers"].get("increase", 0):
        print(f"ERROR: Only {heat_increase} weapons raise heat; need {targets['heatModifiers']['increase']}.")
        sys.exit(1)
    if heat_decrease < targets["heatModifiers"].get("decreaseOrRedistribute", 0):
        print(f"ERROR: Only {heat_decrease} weapons lower/redistribute heat; need {targets['heatModifiers']['decreaseOrRedistribute']}.")
        sys.exit(1)

    if agi_reducers < int(targets.get("agiImpact", 0)):
        print(f"ERROR: Only {agi_reducers} weapons slow AGI; need {targets['agiImpact']}.")
        sys.exit(1)

    if public_support_mods < int(targets.get("publicSupportModifiers", 0)):
        print(f"ERROR: Only {public_support_mods} weapons shift public support; need {targets['publicSupportModifiers']}.")
        sys.exit(1)

    print("OK: weapons.json meets 2025 style, count, and distribution targets.")


if __name__ == "__main__":
    main()
