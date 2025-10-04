# Agent Roster Prompt (2025 Crew)

> Note: We currently have three core creatives (datacenters, events, weapons). Agents are optional and typically handled by the weapons designer when bandwidth allows.

## Quick Reference
- Spec: `../spec.md`
- Roadmap: `../weapons/roadmap.md` (for tone overlap) and future `agents` guidelines when expanded
- Style: `../style/style_guide.md`
- Registry: `../creative_registry.json`
- Content file: `../content/agents.json`
- Validator: `../scripts/validate_agents.py`

## Workflow
1. Open `creative_registry.json` → `categories.agents.items`.
   - Claim the earliest `"pending"` entry by setting `status` to `"in_progress"`.
   - If the roster has fewer than 15 agents and no pending tasks remain, append a stub:
     ```json
     {"id": "ag:pending-###", "role": "logistics", "status": "in_progress"}
     ```
     Pick a role that keeps the operative/logistics/tech split balanced.
2. Draft a 2025 character concept: laid-off specialists, union organizers, drone hobbyists, safety researchers, etc. Keep it witty but empathetic.
3. Add the agent definition to `content/agents.json` under the `agents` array.
   - Required fields: `id`, `name`, `role`, `description`, `icon`, `imagePrompt`, `successRate`, `speed`, `risk`, `capacity`, `cost`, `primaryEffects`, `effects`.
   - `imagePrompt` should follow the shared template with `{subject}` like `2025 coder coordinating a drone strike via laptop` (≤10 words).
   - Ensure `primaryEffects` lists the main stats this agent influences (heat, funds, agi, etc.).
4. Update the registry item with the final `id`, `name`, `role`, optional `notes`, and set `status` to `"done"`.
5. Run `./scripts/validate_agents.py` to confirm role distribution and style compliance.
6. If role counts are uneven, drop additional `pending` stubs to guide the next contributor.

## Writing Checklist
- Mention how the agent’s background ties to 2025 layoffs, AI hype, or infrastructure backlash.
- Keep descriptions concise (≤2 sentences) and jargon-free.
- Avoid real people or easily identifiable analogues; use archetypes.
- Balance successRate vs. risk so no agent is universally dominant.
