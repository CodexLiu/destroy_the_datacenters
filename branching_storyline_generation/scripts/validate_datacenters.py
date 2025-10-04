#!/usr/bin/env python3
"""Validate datacenters.geojson for coverage, tiers, and style requirements."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
DC_PATH = ROOT / "content" / "datacenters.geojson"
REGISTRY_PATH = ROOT / "creative_registry.json"

ALLOWED_REGIONS = {"northeast", "southeast", "midwest", "mountain", "west", "swSpecial"}
ALLOWED_POWER_TIERS = {"low", "medium", "high", "mega"}

STATE_BOUNDS = {
    "AL": {"lat": (30.1, 35.0), "lon": (-88.6, -84.9)},
    "AZ": {"lat": (31.3, 37.0), "lon": (-114.8, -109.0)},
    "AR": {"lat": (33.0, 36.5), "lon": (-94.6, -89.6)},
    "CA": {"lat": (32.5, 42.0), "lon": (-124.4, -114.1)},
    "CO": {"lat": (37.0, 41.0), "lon": (-109.1, -102.0)},
    "CT": {"lat": (41.0, 42.1), "lon": (-73.7, -71.8)},
    "DE": {"lat": (38.4, 39.9), "lon": (-75.8, -75.0)},
    "FL": {"lat": (24.5, 31.0), "lon": (-87.6, -80.0)},
    "GA": {"lat": (30.4, 35.0), "lon": (-85.6, -80.8)},
    "ID": {"lat": (42.0, 49.0), "lon": (-117.2, -111.0)},
    "IL": {"lat": (36.9, 42.5), "lon": (-91.5, -87.0)},
    "IN": {"lat": (37.8, 41.8), "lon": (-88.1, -84.8)},
    "IA": {"lat": (40.4, 43.5), "lon": (-96.6, -90.1)},
    "KS": {"lat": (37.0, 40.0), "lon": (-102.1, -94.6)},
    "KY": {"lat": (36.5, 39.1), "lon": (-89.6, -82.3)},
    "LA": {"lat": (28.9, 33.0), "lon": (-94.0, -88.8)},
    "ME": {"lat": (43.0, 47.5), "lon": (-71.1, -66.9)},
    "MD": {"lat": (37.9, 39.7), "lon": (-79.5, -75.0)},
    "MA": {"lat": (41.2, 42.9), "lon": (-73.5, -69.9)},
    "MI": {"lat": (41.7, 48.3), "lon": (-90.4, -82.4)},
    "MN": {"lat": (43.5, 49.4), "lon": (-97.2, -89.5)},
    "MS": {"lat": (30.2, 35.0), "lon": (-91.7, -88.1)},
    "MO": {"lat": (35.9, 40.6), "lon": (-95.8, -89.1)},
    "MT": {"lat": (44.4, 49.0), "lon": (-116.1, -104.0)},
    "NE": {"lat": (40.0, 43.0), "lon": (-104.1, -95.3)},
    "NV": {"lat": (35.0, 42.0), "lon": (-120.0, -114.0)},
    "NH": {"lat": (42.7, 45.3), "lon": (-72.6, -70.6)},
    "NJ": {"lat": (38.9, 41.4), "lon": (-75.6, -73.8)},
    "NM": {"lat": (31.3, 37.0), "lon": (-109.1, -103.0)},
    "NY": {"lat": (40.5, 45.0), "lon": (-79.8, -71.8)},
    "NC": {"lat": (33.8, 36.6), "lon": (-84.3, -75.4)},
    "ND": {"lat": (45.9, 49.0), "lon": (-104.1, -96.6)},
    "OH": {"lat": (38.4, 42.3), "lon": (-84.9, -80.5)},
    "OK": {"lat": (33.6, 37.0), "lon": (-103.0, -94.4)},
    "OR": {"lat": (41.9, 46.3), "lon": (-124.8, -116.5)},
    "PA": {"lat": (39.7, 42.3), "lon": (-80.6, -74.7)},
    "RI": {"lat": (41.1, 42.0), "lon": (-71.9, -71.1)},
    "SC": {"lat": (32.0, 35.2), "lon": (-83.4, -78.5)},
    "SD": {"lat": (42.5, 45.9), "lon": (-104.1, -96.4)},
    "TN": {"lat": (34.9, 36.7), "lon": (-90.3, -81.6)},
    "TX": {"lat": (25.8, 36.5), "lon": (-106.6, -93.5)},
    "UT": {"lat": (37.0, 42.0), "lon": (-114.1, -109.0)},
    "VT": {"lat": (42.7, 45.1), "lon": (-73.4, -71.5)},
    "VA": {"lat": (36.5, 39.5), "lon": (-83.7, -75.2)},
    "WA": {"lat": (45.5, 49.0), "lon": (-124.8, -116.9)},
    "WV": {"lat": (37.2, 40.7), "lon": (-82.7, -77.7)},
    "WI": {"lat": (42.5, 47.3), "lon": (-92.9, -86.2)},
    "WY": {"lat": (41.0, 45.0), "lon": (-111.1, -104.0)}
}


def load_geojson() -> Dict:
    if not DC_PATH.exists():
        print(f"ERROR: {DC_PATH} does not exist.")
        sys.exit(1)
    try:
        with DC_PATH.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Failed to parse {DC_PATH}: {exc}")
        sys.exit(1)


def load_registry() -> Dict:
    if not REGISTRY_PATH.exists():
        print(f"ERROR: {REGISTRY_PATH} does not exist.")
        sys.exit(1)
    try:
        with REGISTRY_PATH.open("r", encoding="utf-8") as fp:
            return json.load(fp)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Failed to parse {REGISTRY_PATH}: {exc}")
        sys.exit(1)


def ensure_metadata(data: Dict) -> Dict:
    metadata = data.get("metadata") or {}
    style = metadata.get("style") or {}
    targets = metadata.get("targets") or {}
    if style.get("year") != 2025:
        print("ERROR: metadata.style.year must be 2025.")
        sys.exit(1)
    template = style.get("imagePromptTemplate", "")
    for token in ("retro futurist", "light cyan", "persimmon", "2025"):
        if token not in template:
            print("ERROR: metadata.style.imagePromptTemplate missing required tokens.")
            sys.exit(1)
    required_target_keys = ["totalDatacenters", "regions", "powerTiers"]
    if any(key not in targets for key in required_target_keys):
        print("ERROR: metadata.targets incomplete.")
        sys.exit(1)
    return targets


def validate_feature(feature: Dict, index: int) -> Dict[str, str]:
    if feature.get("type") != "Feature":
        print(f"ERROR: feature index {index} missing type Feature.")
        sys.exit(1)
    geometry = feature.get("geometry") or {}
    if geometry.get("type") != "Point":
        print(f"ERROR: feature {feature.get('id')} geometry must be Point.")
        sys.exit(1)
    coords = geometry.get("coordinates")
    if not (isinstance(coords, list) and len(coords) == 2):
        print(f"ERROR: feature {feature.get('id')} coordinates must be [lon, lat].")
        sys.exit(1)
    props = feature.get("properties") or {}
    required_props = [
        "id",
        "name",
        "operator",
        "regionGroup",
        "state",
        "powerMW",
        "powerTier",
        "computeUnits",
        "healthMax",
        "defense",
        "agiImpact",
        "status",
        "imagePrompt",
    ]
    missing = [key for key in required_props if props.get(key) in (None, "")]
    if missing:
        print(f"ERROR: feature {feature.get('id')} missing properties: {', '.join(missing)}")
        sys.exit(1)
    region = props.get("regionGroup")
    if region not in ALLOWED_REGIONS:
        print(f"ERROR: feature {feature['id']} regionGroup {region!r} invalid.")
        sys.exit(1)
    power_tier = props.get("powerTier")
    if power_tier not in ALLOWED_POWER_TIERS:
        print(f"ERROR: feature {feature['id']} powerTier {power_tier!r} invalid.")
        sys.exit(1)
    state = (props.get("state") or "").upper()
    if state not in STATE_BOUNDS:
        print(f"ERROR: feature {feature['id']} has unknown state {state!r}.")
        sys.exit(1)
    try:
        float(props.get("powerMW"))
        float(props.get("computeUnits"))
        float(props.get("healthMax"))
        float(props.get("defense"))
        float(props.get("agiImpact"))
    except (TypeError, ValueError):
        print(f"ERROR: feature {feature['id']} numeric fields must be numbers.")
        sys.exit(1)
    lon, lat = coords
    bounds = STATE_BOUNDS[state]
    lat_min, lat_max = bounds["lat"]
    lon_min, lon_max = bounds["lon"]
    if not (lat_min <= lat <= lat_max and lon_min <= lon <= lon_max):
        print(
            f"ERROR: feature {feature['id']} coordinates ({lat:.4f}, {lon:.4f}) fall outside {state} bounds."
        )
        sys.exit(1)
    prompt = (props.get("imagePrompt") or "").lower()
    for token in ("retro futurist", "2025", "light", "persimmon"):
        if token not in prompt:
            print(f"ERROR: feature {feature['id']} imagePrompt missing token '{token}'.")
            sys.exit(1)
    status = props.get("status")
    if status not in {"intact", "damaged", "destroyed"}:
        print(f"ERROR: feature {feature['id']} status {status!r} invalid.")
        sys.exit(1)
    return {"region": region, "powerTier": power_tier}


def main() -> None:
    data = load_geojson()
    targets = ensure_metadata(data)
    features = data.get("features") or []

    total_target = int(targets.get("totalDatacenters", 0))
    if len(features) < total_target:
        print(f"ERROR: Only {len(features)} datacenters defined; target is {total_target}.")
        sys.exit(1)

    region_counts: Dict[str, int] = {key: 0 for key in targets.get("regions", {})}
    tier_counts: Dict[str, int] = {key: 0 for key in targets.get("powerTiers", {})}

    feature_props: Dict[str, Dict[str, str]] = {}
    for idx, feature in enumerate(features):
        info = validate_feature(feature, idx)
        region_counts[info["region"]] = region_counts.get(info["region"], 0) + 1
        tier_counts[info["powerTier"]] = tier_counts.get(info["powerTier"], 0) + 1
        props = feature["properties"]
        feature_props[props["id"]] = {
            "name": props["name"],
            "state": props["state"],
            "regionGroup": props["regionGroup"],
            "powerTier": props["powerTier"],
        }

    region_failures = [
        f"{region}: {count}/{targets['regions'][region]}"
        for region, count in region_counts.items()
        if count < targets["regions"].get(region, 0)
    ]
    if region_failures:
        print("ERROR: Region distribution incomplete -> " + ", ".join(region_failures))
        sys.exit(1)

    tier_failures = [
        f"{tier}: {count}/{targets['powerTiers'][tier]}"
        for tier, count in tier_counts.items()
        if count < targets["powerTiers"].get(tier, 0)
    ]
    if tier_failures:
        print("ERROR: Power-tier distribution incomplete -> " + ", ".join(tier_failures))
        sys.exit(1)

    registry = load_registry()
    datacenter_items: List[Dict] = registry.get("categories", {}).get("datacenters", {}).get("items", [])
    if len(datacenter_items) != len(features):
        print(
            "ERROR: creative_registry.datacenters.items has"
            f" {len(datacenter_items)} entries but {len(features)} datacenters exist."
        )
        sys.exit(1)

    registry_ids = {item.get("id") for item in datacenter_items}

    missing_in_registry = [dc_id for dc_id in feature_props if dc_id not in registry_ids]
    if missing_in_registry:
        print("ERROR: creative_registry missing datacenters -> " + ", ".join(sorted(missing_in_registry)))
        sys.exit(1)

    extra_registry = [item_id for item_id in registry_ids if item_id not in feature_props]
    if extra_registry:
        print("ERROR: creative_registry contains unknown datacenters -> " + ", ".join(sorted(extra_registry)))
        sys.exit(1)

    for item in datacenter_items:
        item_id = item.get("id")
        if item.get("status") != "done":
            print(f"ERROR: creative_registry entry {item_id} must have status 'done'.")
            sys.exit(1)
        props = feature_props[item_id]
        for key in ("name", "state", "regionGroup", "powerTier"):
            if (item.get(key) or "") != props[key]:
                print(
                    "ERROR: creative_registry entry"
                    f" {item_id} field {key!r} does not match datacenters.geojson."
                )
                sys.exit(1)

    print("OK: datacenters.geojson meets 2025 style, count, and distribution targets.")


if __name__ == "__main__":
    main()
