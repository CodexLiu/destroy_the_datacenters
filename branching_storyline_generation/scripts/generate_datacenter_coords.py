#!/usr/bin/env python3
"""Generate candidate lat/lon pairs within a given US state."""
from __future__ import annotations

import argparse
import json
import random
import sys
from typing import List, Tuple

try:
    from validate_datacenters import STATE_BOUNDS
except ImportError:
    print("ERROR: Unable to import STATE_BOUNDS from validate_datacenters.py.")
    sys.exit(1)


def generate(state: str, count: int) -> List[Tuple[float, float]]:
    bounds = STATE_BOUNDS[state]
    lat_min, lat_max = bounds["lat"]
    lon_min, lon_max = bounds["lon"]
    return [
        (
            random.uniform(lat_min, lat_max),
            random.uniform(lon_min, lon_max),
        )
        for _ in range(count)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate random coordinates inside a state's bounding box.")
    parser.add_argument("--state", "-s", required=True, help="Two-letter state code (e.g., VA, OR).")
    parser.add_argument("--count", "-c", type=int, default=3, help="How many coordinate pairs to output (default 3).")
    parser.add_argument("--seed", type=int, help="Optional RNG seed for reproducibility.")
    parser.add_argument(
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Output format: csv => 'lat,lon' per line; json => array of [lat, lon] pairs.",
    )
    args = parser.parse_args()

    state = args.state.upper()
    if state not in STATE_BOUNDS:
        print(f"ERROR: Unknown state '{state}'.")
        sys.exit(1)

    if args.count <= 0:
        print("ERROR: count must be positive.")
        sys.exit(1)

    if args.seed is not None:
        random.seed(args.seed)

    coords = generate(state, args.count)

    if args.format == "json":
        print(json.dumps([[round(lat, 6), round(lon, 6)] for lat, lon in coords], indent=2))
    else:
        for lat, lon in coords:
            print(f"{lat:.6f},{lon:.6f}")


if __name__ == "__main__":
    main()
