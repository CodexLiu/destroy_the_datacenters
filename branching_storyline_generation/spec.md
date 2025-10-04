# Destroy The Datacenters — Data Structure Spec

Purpose: Define the content format, runtime state, and minimal APIs for a simple React webapp where players plan and execute actions to destroy data centers across the continental US, in a Plague Inc–style loop with branching events and choices.

Scope: Client-first (no login). All game content loads from static JSON/GeoJSON. Game state persists locally (LocalStorage/IndexedDB). A server is optional for content delivery; not required for gameplay.

Creative tone: situate the campaign explicitly in **2025**, leverage recognizable-but-accessible current events, and keep every description in reach for an average tech worker—clever without deep niche jargon. Humor should stay satirical, not celebratory.

## Core Concepts

- Datacenter: A target node on the map with location, stats, and health.
- Weapon: A tool or tactic that inflicts damage or changes global modifiers.
- Agent: A unit (e.g., revolutionary, programmer) that executes actions with weapons.
- Event: A triggered narrative beat with branching choices that apply effects.
- Global Metrics: AGI progress, funds, public support, heat/retaliation.
- Action/Mission: Player-initiated operation (e.g., attack a datacenter) resolved by rules.

## Content Files (Static)

- `content/datacenters.geojson` — GeoJSON FeatureCollection of datacenters.
- `content/weapons.json` — Array of weapon definitions.
- `content/agents.json` — Array of agent/unit definitions (optional; can inline into weapons if simplifying).
- `content/events.json` — Array of events with trigger conditions and branching choices.
- `content/constants.json` — Tunable global constants and balancing parameters.
- `creative_registry.json` — Master checklist that tracks progress across events, weapons, agents, and datacenters so content authors don’t have to scan entire files.

All content files should include a top-level `version` string to support migrations.

## Type Shapes (TypeScript)

These interfaces describe the JSON structure used by the client. JSON Schema can be derived later if needed.

```ts
// Common
export type ID = string; // e.g. "dc:aws-us-east-1a", "wp:drone-bomb"

export interface NumericRange { min: number; max: number } // inclusive

export interface Effect { 
  // Declarative effect patches applied to state and/or entities
  // Positive increases; negative decreases
  target: 
    | { type: 'global'; key: 'agiProgress' | 'agiRate' | 'funds' | 'publicSupport' | 'heat' }
    | { type: 'datacenter'; id: ID; key: 'health' | 'defense' }
    | { type: 'datacenters'; key: 'defense' | 'health' | 'agiImpact' } // broadcast
    | { type: 'inventory'; key: ID; }; // add/remove weapons/agents by id
  op: 'add' | 'mul' | 'set';
  value: number;
}

export interface Requirement {
  type: 'global' | 'datacenter' | 'inventory';
  key: string; // e.g., 'funds', 'publicSupport', 'heat', 'status'
  cmp: 'gte' | 'lte' | 'eq' | 'ne';
  value: number | string | boolean;
  // Optional scoping
  datacenterId?: ID;
}

export interface Trigger {
  // Logical OR across triggers; within each trigger, conditions are ANDed
  when: 'onStart' | 'onTick' | 'onDestroy' | 'onDamage' | 'onTimer' | 'manual';
  // Optional filters
  datacenterId?: ID;
  // Conditions
  requires?: Requirement[];
  // For timers
  afterTicks?: number; // ticks since game start or since previous trigger
  chance?: number; // 0..1 random chance when evaluated
}
```

### Datacenters (GeoJSON)

`content/datacenters.geojson` is a GeoJSON `FeatureCollection` where each `Feature` has Point geometry and datacenter properties.

```ts
export interface DatacenterProps {
  id: ID;
  name: string;
  operator?: string; // e.g., AWS, Google, Meta
  region?: string; // e.g., 'US-EAST'
  regionGroup?: 'northeast' | 'southeast' | 'midwest' | 'mountain' | 'west' | 'swSpecial';
  state?: string; // two-letter state code for lat/lon validation
  powerMW?: number; // electricity usage estimate
  powerTier?: 'low' | 'medium' | 'high' | 'mega';
  computeUnits?: number; // abstract capacity metric
  healthMax: number; // e.g., 100
  defense: number; // 0..1 reduces damage
  agiImpact: number; // contribution to AGI progress when intact
  status: 'intact' | 'damaged' | 'destroyed';
  icon?: string; // UI hint for marker
  imagePrompt?: string; // AI image prompt aligned to style guide
}

// GeoJSON Feature<DatacenterProps>
export interface DatacenterFeature {
  type: 'Feature';
  id: ID;
  geometry: { type: 'Point'; coordinates: [number, number] }; // [lon, lat]
  properties: DatacenterProps;
}
```

Example feature (minified for brevity):

```json
{
  "type": "Feature",
  "id": "dc:example-1",
  "geometry": { "type": "Point", "coordinates": [-77.0365, 38.8977] },
  "properties": {
    "id": "dc:example-1",
    "name": "Example DC",
    "operator": "ExampleCloud",
    "region": "US-EAST",
    "regionGroup": "northeast",
    "state": "VA",
    "powerMW": 120,
    "computeUnits": 500,
    "healthMax": 100,
    "defense": 0.25,
    "agiImpact": 8,
    "status": "intact",
    "icon": "datacenter"
  }
}
```

### Weapons

`content/weapons.json` is an object with `version` and an array of `Weapon`.

```ts
export type DamageType = 'explosive' | 'incendiary' | 'cyber' | 'social' | 'sabotage';

export interface Weapon {
  id: ID;
  name: string;
  description?: string;
  icon?: string;
  imagePrompt?: string; // AI art prompt for consistent weapon imagery
  category?: 'improvised' | 'drone' | 'cyber' | 'social' | 'support';
  primaryEffects?: Array<'heat' | 'agi' | 'funds' | 'publicSupport' | 'defense' | 'inventory'>;
  damage: number; // base damage per use
  damageType: DamageType;
  variance?: number; // +/- percentage randomness (e.g., 0.2 for 20%)
  stealth?: number; // 0..1 reduces heat gains / detection
  cooldownTicks?: number;
  cost?: number; // funds required to use/acquire
  requires?: Requirement[]; // e.g., funds >= 100
  effects?: Effect[]; // additional global or entity modifiers
  allowedTargets?: ('datacenter')[]; // future expansion
}
```

Example entry:

```json
{
  "id": "wp:drone-bomb",
  "name": "Drone with Improvised Explosive",
  "icon": "drone",
  "damage": 30,
  "damageType": "explosive",
  "variance": 0.15,
  "stealth": 0.3,
  "cooldownTicks": 2,
  "cost": 200,
  "effects": [ { "target": { "type": "global", "key": "heat" }, "op": "add", "value": 5 } ]
}
```

### Agents (optional but recommended)

`content/agents.json` lists units that can carry out missions. If simplifying, you can skip agents and let weapons be used directly.

```ts
export interface Agent {
  id: ID;
  name: string; // e.g., 'Revolutionary', 'Disgruntled Programmer'
  icon?: string;
  imagePrompt?: string; // AI prompt for character art
  role?: 'operative' | 'logistics' | 'tech';
  successRate: number; // base probability of mission success (0..1)
  speed?: number; // abstract travel speed between targets
  risk?: number; // base capture risk (0..1)
  capacity?: number; // how many weapons/uses per mission
  cost?: number; // recruitment/training
  requires?: Requirement[];
  primaryEffects?: Array<'heat' | 'funds' | 'agi' | 'publicSupport' | 'defense' | 'inventory'>;
  effects?: Effect[]; // passive modifiers while owned/deployed
}
```

### Events and Choices

`content/events.json` contains narrative beats with triggers and branching choices.

```ts
export interface EventChoice {
  id: ID;
  label: string; // UI label
  description?: string; // shown on hover/details
  requires?: Requirement[]; // gating logic
  effects?: Effect[]; // applied if chosen
  followupEventId?: ID; // chain to another event
}

export interface GameEvent {
  id: ID;
  title: string;
  body: string; // narrative text
  year: 2025; // fixed in-universe year to anchor realism
  icon?: string;
  imagePrompt?: string; // AI art prompt for event card illustration
  priority?: number; // higher shows earlier if multiple fire
  triggers: Trigger[]; // any one trigger can fire the event
  oneTime?: boolean; // default true
  choices: EventChoice[]; // at least one; if none, auto-close
}
```

Example event:

```json
{
  "id": "ev:dji-partnership",
  "title": "Rumors of a Drone Supplier",
  "body": "A source hints at bulk drone purchases via a gray-market supplier.",
  "triggers": [ { "when": "onTick", "requires": [{ "type": "global", "key": "funds", "cmp": "gte", "value": 200 }] } ],
  "oneTime": true,
  "choices": [
    { "id": "ch:buy-drones", "label": "Buy drones", "effects": [
      { "target": { "type": "inventory", "key": "wp:drone-bomb" }, "op": "add", "value": 3 },
      { "target": { "type": "global", "key": "funds" }, "op": "add", "value": -200 },
      { "target": { "type": "global", "key": "heat" }, "op": "add", "value": 3 }
    ] },
    { "id": "ch:lay-low", "label": "Lay low", "effects": [
      { "target": { "type": "global", "key": "heat" }, "op": "add", "value": -2 }
    ] }
  ]
}
```

### Constants and Balancing

`content/constants.json` centralizes tunables.

```ts
export interface Constants {
  version: string;
  tickMs: number; // client timer (e.g., 500)
  startingFunds: number;
  startingPublicSupport: number;
  startingHeat: number;
  startingAgiProgress: number; // 0..100
  baseAgiRatePerTick: number; // AGI progress per tick pre-modifiers
  heatAffectsAgiRate: number; // multiplier per heat point
  destroyedDcAgiPenalty: number; // applied when a DC is destroyed
  damageDefenseFactor: number; // how defense reduces damage (0..1)
  randomVarianceDefault: number; // fallback when not defined by weapon
}
```

## Runtime Game State (Client)

All gameplay runs on the client and persists to LocalStorage/IndexedDB.

```ts
export interface DatacenterRuntime {
  id: ID;
  health: number;
  status: 'intact' | 'damaged' | 'destroyed';
}

export interface InventoryItem {
  id: ID; // weapon or agent id
  count: number; // discrete uses or unit count
  cooldownUntilTick?: number; // per-item cooldown tracking
}

export interface GameState {
  version: string; // aligns to content version
  seed: number; // RNG seed for determinism
  tick: number;
  funds: number;
  publicSupport: number; // 0..100
  heat: number; // retaliation pressure
  agiProgress: number; // 0..100, lose if reaches 100
  agiRate: number; // derived per tick
  datacenters: Record<ID, DatacenterRuntime>;
  inventory: Record<ID, InventoryItem>; // weapons/agents
  seenEvents: Record<ID, boolean>; // for oneTime events
  activeTimers: Array<{ id: ID; resumeTick: number; payload?: any }>; // simple timer queue
}
```

Recommended save key: `destroy-the-datacenters:v1:save` with JSON-serialized `GameState`.

## Actions/Missions (Client-Only API)

Actions mutate `GameState` via rules using the declarative data above.

- `attackDatacenter(payload)`
  - Input: `{ datacenterId: ID, weaponId: ID, agentId?: ID }`
  - Compute damage: `raw = weapon.damage * (1 ± variance)`,
    `effective = raw * (1 - defense * constants.damageDefenseFactor)`
  - Apply to runtime `health`; update `status` thresholds
  - Apply weapon `effects`; adjust `heat`, `funds`, cooldowns
  - On destroy: apply `destroyedDcAgiPenalty`, trigger `onDestroy` events

- `resolveTick()` (game loop step)
  - Increment `tick`
  - Update `agiRate = baseAgiRatePerTick * (1 + heat * heatAffectsAgiRate) - sum(dcDestroyed.agiImpactMods)`
  - Clamp and apply `agiProgress += agiRate`
  - Evaluate `onTick` triggers and timers; enqueue events

- `chooseEventOption(eventId, choiceId)`
  - Validate `requires`; apply `effects`; mark event as seen; queue `followupEventId` if present

Lose condition: `agiProgress >= 100`.
Win condition: all datacenters `status === 'destroyed'`.

## IDs and Referencing

- Use stable string IDs with prefixes: `dc:` datacenters, `wp:` weapons, `ag:` agents, `ev:` events, `ch:` choices.
- GeoJSON Feature `id` must match `properties.id` and runtime `DatacenterRuntime.id`.
- Cross-file references (e.g., event effects targeting a datacenter) must use these IDs.

## Map Integration

- Load `datacenters.geojson` into Mapbox as a source/layer.
- Each feature uses its `icon` for styling; defaults to a generic marker.
- Clicking a marker opens a side panel with properties and actions (weapons available, expected damage).

## Persistence and Versioning

- Store `GameState` in LocalStorage with `version`.
- If content `version` mismatches a save, run a lightweight migration or prompt to restart.
- Optionally, mirror saves to IndexedDB for robustness if sizes grow.

## Minimal File Layout

```
content/
  datacenters.geojson
  weapons.json
  agents.json
  events.json
  constants.json
src/
  lib/
    contentLoader.ts   // fetch + validate content
    engine.ts          // tick loop, actions, RNG
    state.ts           // GameState helpers, persistence
  app/
    MapView.tsx        // Mapbox layer + interactions
    Sidebar.tsx        // Details, actions, inventory
    EventsPanel.tsx    // Event queue and choices
```

## Notes on Simplification

- If SQLite is desired for authoring, export to JSON/GeoJSON for the client bundle.
- Agents can be initially omitted; weapons can act directly for MVP.
- Start with a handful of datacenters and events; scale content later.
- Each creative contributor reads the relevant `*_creative_prompt.md`, claims the next pending item from `creative_registry.json`, updates the appropriate content file, then marks their work as `done` in the registry to avoid duplicate effort.
- The creative workflow assumes **three dedicated authors**: one for datacenters, one for events, and one for weapons. Each owns their category end to end.
- Use `./scripts/generate_datacenter_coords.py` to produce believable lat/lon pairs per state, and `./scripts/validate_datacenters.py` to confirm coordinates land within the correct state bounds.
- Never modify the validator scripts under `scripts/`; your work is complete only when the matching validator runs clean.
- Datacenter entries should lean on recognizable 2025 tech references (Waymo patrols, Amazon drone fleets, cooling scandals) while keeping names lightly fictionalized.
- Event narratives should weave in headline AI figures (e.g., Alex Wang, Sundar, Zuckerberg) in satirical fashion without misrepresentation.

## Creative Style Theme

- Art direction: "retro-futurist protest zine" — bold flat colors, grainy screenprint texture, chunky sans-serif captions, light cyan/persimmon palette.
- AI prompt template: `"retro futurist protest poster, screenprint texture, light cyan and persimmon palette, {subject}, dynamic perspective, simple shapes, minimal text, 2025 dystopian satire"`.
- Reuse the palette and texture for all event cards, weapon illustrations, and map icons to keep cohesion.
