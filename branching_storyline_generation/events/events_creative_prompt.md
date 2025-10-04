# Event Author Prompt (2025 Campaign)

## Quick Reference
- Spec: `../spec.md`
- Roadmap: `../events/roadmap.md`
- Style: `../style/style_guide.md`
- Registry: `../creative_registry.json`
- Content file: `../content/events.json`
- Validator: `../scripts/validate_events.py`

## Workflow
0. Remember: you are the sole events creative for this project—own the entire 100-event backlog and coordinate with the datacenter/weapon leads via registry notes.
1. Open `creative_registry.json` → `categories.events.items`.
   - Claim the first item whose `status` is `"pending"` by changing it to `"in_progress"`.
   - If no pending entries exist and the total event count is still below 100, append a new stub such as:
     ```json
     {"id": "ev:pending-###", "title": "TBD", "phase": "mid", "stats": [], "status": "in_progress"}
     ```
     Pick a phase that helps balance the roadmap targets.
2. Review the roadmap distribution goals (phase counts, stat coverage, pacing). Choose an event concept grounded in a real 2024/2025 headline, then push it slightly into satire.
3. Author the full event entry inside `content/events.json` under the `events` array.
   - Required fields: `id`, `title`, `body`, `year` (always 2025), `phase`, `primaryStats`, `triggers`, `choices`, `imagePrompt`.
   - Keep language accessible: one-paragraph body, clear stakes, explicit stat trade-offs.
   - Ensure every choice includes at least one `effect` impacting the tracked stats.
   - Craft the `imagePrompt` by filling `{subject}` in the shared template: `retro futurist protest poster, screenprint texture, light cyan and persimmon palette, {subject}, dynamic perspective, simple shapes, minimal text, 2025 dystopian satire`.
4. Update the registry entry you claimed:
   - Replace the stub `id` with the real event id (`ev:short-name`).
   - Set `title`, `phase`, and `stats` (matching `primaryStats`).
   - Set `status` to `"done"` once the event is saved.
5. Run `./scripts/validate_events.py` from the project root. Resolve any reported distribution gaps before finishing. Do **not** edit the validator script; your task ends only when this check passes.
6. Leave a short note in the registry item if you adjusted distribution targets (e.g., `{ "notes": "counts toward mid/heat" }`).

## Writing Checklist
- Reference at least one recognizable 2024/2025 tech news hook.
- Name-drop headline AI figures (Alex Wang, Sundar Pichai, Mark Zuckerberg, Sam Altman, etc.) in satirical-yet-recognizable ways.
- Mention immediate consequences (heat/AGI/public support) explicitly.
- Keep the tone satirical but grounded; no glorification of violence.
- Verify the AGI and heat numbers stay within plausible ranges for balance.
