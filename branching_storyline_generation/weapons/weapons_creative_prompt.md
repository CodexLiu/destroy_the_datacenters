# Weapon Designer Prompt (2025 Arsenal)

## Quick Reference
- Spec: `../spec.md`
- Roadmap: `../weapons/roadmap.md`
- Style: `../style/style_guide.md`
- Registry: `../creative_registry.json`
- Content file: `../content/weapons.json`
- Validator: `../scripts/validate_weapons.py`

## Workflow
0. You are the only weapons/arsenal designer—plan all 35 entries with progression in mind and sync with the events/datacenter leads when cross-referencing unlocks.
1. Open `creative_registry.json` → `categories.weapons.items`.
   - Claim the first `"pending"` weapon by switching its `status` to `"in_progress"`.
   - If no pending entries exist and fewer than 35 weapons are defined, append a stub:
     ```json
     {"id": "wp:pending-###", "name": "TBD", "category": "cyber", "status": "in_progress"}
     ```
     Choose a category that helps hit the roadmap quotas.
2. Check category, damage tier, stealth, and heat distribution targets in the roadmap to see which slots need attention.
3. Add the full weapon definition to `content/weapons.json` under the `weapons` array.
   - Required fields: `id`, `name`, `category`, `description`, `icon`, `imagePrompt`, `damage`, `damageType`, `variance`, `stealth`, `cooldownTicks`, `cost`, `primaryEffects`, `effects`.
   - Every description should reference a 2025 reality (post-layoff technicians, drone export rules, etc.).
   - Balance damage vs. stealth vs. heat so trade-offs remain interesting.
   - Build the `imagePrompt` via the shared template with a `{weapon subject}` phrase (≤10 words).
4. Update the registry entry with real data: finalize `id`, `name`, `category`, add optional `notes` (e.g., `"heavy tier, heat++"`), and flip `status` to `"done"`.
5. Run `./scripts/validate_weapons.py` to confirm counts, stealth bands, heat modifiers, AGI/public support coverage. Do **not** modify the validator; completion requires a clean test run.
6. If the validator flags distribution gaps, queue additional `pending` records in the registry to signal future needs.

## Design Checklist
- Keep weapon concepts funny yet believable for DIY 2025 activism.
- Tie at least one element to recognizable tech brands or personalities (Waymo, Amazon drones, Meta headset refits, Alex Wang's contractors) while keeping names lightly spoofed.
- Ensure at least two stat interactions per weapon (e.g., damage + heat, or funds + AGI).
- Reuse punny operator aliases from the datacenter glossary when applicable.
- Avoid trademarked names; describe tech by function instead ("self-driving taxi convoy" instead of brand).
