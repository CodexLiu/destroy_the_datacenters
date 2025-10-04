# Datacenter Research Prompt (2025 Map)

## Quick Reference
- Spec: `../spec.md`
- Roadmap: `../datacenters/roadmap.md`
- Style: `../style/style_guide.md`
- Registry: `../creative_registry.json`
- Content file: `../content/datacenters.geojson`
- Validator: `../scripts/validate_datacenters.py`

## Workflow
0. You are the single datacenter researcher for this project—cover all 60 sites.
1. Open `creative_registry.json` → `categories.datacenters.items`.
   - Claim the first entry with `status` `"pending"` by flipping it to `"in_progress"`.
   - If no pending records exist and the map has fewer than 60 features, append a stub such as:
     ```json
     {"id": "dc:pending-###", "regionGroup": "mountain", "powerTier": "medium", "status": "in_progress"}
     ```
     Choose `regionGroup`/`powerTier` combos that keep distributions balanced.
2. Research or invent a lightly fictionalized 2025 site:
   - Base it on real expansion plans, environmental controversies, or AI cluster news.
   - Swap brand names for the agreed puns (Bananazon, Giggle Cloud, Metaverse Logistics, etc.).
3. Run `./scripts/generate_datacenter_coords.py --state XX` (replace `XX` with the two-letter code) to generate coordinate candidates. Pick the pair that best matches the city/region you’re targeting; the script prints `lat,lon` lines you can paste.
4. Insert a new GeoJSON `Feature` into `content/datacenters.geojson`.
   - Include coordinates (city-level accuracy). If fictionalizing, note that in `notes`.
   - Populate required properties: `id`, `name`, `operator`, `region`, `regionGroup`, `state`, `powerMW`, `powerTier`, `computeUnits`, `healthMax`, `defense`, `agiImpact`, `status` (default `"intact"`), `icon`, `imagePrompt`.
   - `state` must be an uppercase USPS code (e.g., `VA`).
   - `imagePrompt` must follow the shared template with a `{datacenter subject}` like `desert server farm guarded by autonomous taxis`.
   - Add optional `notes` for source links or justification if helpful.
5. Update the registry entry you claimed with the final `id`, `name`, `state`, `regionGroup`, `powerTier`, and any `notes`, then set `status` to `"done"`.
6. Run `./scripts/validate_datacenters.py` to confirm state, regional, and power-tier quotas remain on track. Do **not** edit the validator; keep iterating on data until the test passes.
7. If a quota is running low, add extra `pending` placeholders in the registry for future agents.

## Research Checklist
- Double-check power tiers align with the roadmap ranges (<40 low, 40–100 medium, etc.).
- Tie each description to a 2025 tension point (water usage, wildfire smoke, AGI race, labor unrest).
- Spotlight recognizable tech touchpoints (Waymo patrol convoys, Bananazon delivery drones, Giggle Cloud cooling barges) to keep satire obvious.
- Keep coordinates within the continental US for this MVP.
- Ensure no real facility is directly exposed—fictionalize naming/location slightly when needed.
