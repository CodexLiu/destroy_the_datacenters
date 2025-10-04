# Datacenters Research Roadmap

## Goals

- Curate **60 datacenter targets** for the continental US MVP, blending real facilities with lightly fictionalized counterparts.
- Cover all major operators (AWS, Google, Microsoft, Meta, Oracle, IBM, colocation) plus a handful of cutting-edge AI clusters (OpenAI/Microsoft, Anthropic, Tesla Dojo, Meta FAIR).
- Assign believable stats: power draw (MW), compute capacity (abstract units), defense rating, AGI contribution, narrative hooks.
- Provide geographic spread across regions to support pacing and travel decisions.
- Keep the timeline locked to **2025**—start with plausible builds from current expansions and then exaggerate slightly for satire.
- Write descriptions so an average tech worker immediately grasps why each site matters (power, politics, partners).
- Satire should highlight recognizable technologies (Waymo security patrols, Bananazon drone fleets, Giggle Cloud delivery blimps) so players immediately get the joke.

## Distribution Targets

- Northeast: 12 (Virginia, New Jersey, New York, Massachusetts).
- Southeast: 10 (Georgia, North Carolina, Florida, Texas gulf).
- Midwest: 10 (Ohio, Iowa, Illinois, Nebraska).
- Mountain West: 8 (Utah, Nevada, Arizona, Colorado).
- West Coast: 12 (Washington, Oregon, Northern/Southern California).
- Southern California & Southwest specialized AI labs: 8 (San Jose, LA, Austin, Phoenix, Vegas).

## Research Checklist

- [ ] Gather public lists/maps: Uptime Institute, Data Center Knowledge, hyperscaler infrastructure press releases, FOIA reports.
- [ ] Identify flagship AI/ML facilities (e.g., Microsoft & OpenAI in Iowa, Google Cloud in The Dalles, Meta in Prineville, Amazon in Northern Virginia).
- [ ] Cross-reference power usage data (PUF filings, local utility reports) to estimate powerMW tiers: low (<40), medium (40–100), high (100–200), mega (>200).
- [ ] Capture lat/long coordinates (approximate but consistent); note if fictionalized to avoid targeting specifics.
- [ ] Record the two-letter state code for every site so coordinates can be validated.
- [ ] Note local narratives: community pushback, water usage controversies, union efforts, drone no-fly zones.
- [ ] Flag datacenters tied to current events (e.g., AI chip shortages, water cooling limits, wildfire risks) for event synergy.
- [ ] Draft short flavor blurbs referencing 2025 context (e.g., "post-layoff skeleton crew", "heat dome overstressing chillers").
- [ ] Ensure each site name/description nods to a real 2025 tech storyline (Waymo patrols, Amazon delivery drones, FAA hearings, etc.).

## Naming & Tone

- Fictionalize brand names lightly: Amazon → "Bananazon Compute", Google → "Giggle Cloud", Meta → "Metaverse Logistics". Keep puns readable, not cryptic.
- Note when locations are offset or renamed for safety; keep coordinates approximate to city-level, not street-level.
- Maintain satirical voice while acknowledging real-world consequences (resource strain, labor conditions).

## Stat Modeling Guidelines

- Health scales with physical footprint/power tier; mega sites get higher HP but also larger AGI impact.
- Defense factors: consider operator security posture, proximity to urban centers, presence of autonomous security (Waymo patrols, Boston Dynamics).
- AGI contribution: base on compute capacity tier; high-tier AI labs accelerate AGI rate more significantly.
- Special properties: mark datacenters that unlock unique events (e.g., "drain Denver reservoir" sabotage) or trigger operator retaliation.

## Data Production Steps

- [ ] Build CSV master list with columns: id, name, operator, city, state, coordinates, power tier, compute units, agiImpact, defense, notes.
- [ ] Convert punny operator names and city aliases into a shared glossary for consistency across events/weapons.
- [ ] Export to GeoJSON (`content/datacenters.geojson`) with consistent IDs and properties.
- [ ] Create quick Mapbox preview to validate coverage and clustering.
- [ ] Document assumptions for each stat (e.g., "powerMW estimated from news article dated 2025-09-07").
- [ ] Use `./scripts/generate_datacenter_coords.py --state XX` to draft candidate coordinates, then run `./scripts/validate_datacenters.py` to ensure state compliance.

## Image Prompt Guidance

- Template: `retro futurist protest poster, screenprint texture, light cyan and persimmon palette, {datacenter subject}, dynamic perspective, simple shapes, minimal text, 2025 dystopian satire`.
- `{datacenter subject}` examples: `massive server farm glowing in desert heat`, `data fortress guarded by autonomous taxis`, `cooling towers spraying mist over protesters`.
- Avoid real logos; describe architectures, landscapes, and vibes.
