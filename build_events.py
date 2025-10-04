import json
from pathlib import Path

phase_variations = [
    {
        "phase": "early",
        "chance": 0.3,
        "requires": {"type": "global", "key": "publicSupport", "cmp": "gte", "value": 5},
    },
    {
        "phase": "early",
        "chance": 0.28,
        "requires": {"type": "global", "key": "funds", "cmp": "gte", "value": 8},
    },
    {
        "phase": "early",
        "chance": 0.26,
        "requires": {"type": "global", "key": "heat", "cmp": "lte", "value": 45},
    },
    {
        "phase": "mid",
        "chance": 0.24,
        "requires": {"type": "global", "key": "publicSupport", "cmp": "gte", "value": 12},
    },
    {
        "phase": "mid",
        "chance": 0.22,
        "requires": {"type": "global", "key": "heat", "cmp": "lte", "value": 60},
    },
    {
        "phase": "mid",
        "chance": 0.2,
        "requires": {"type": "global", "key": "funds", "cmp": "gte", "value": 15},
    },
    {
        "phase": "mid",
        "chance": 0.18,
        "requires": {"type": "global", "key": "agiProgress", "cmp": "gte", "value": 25},
    },
    {
        "phase": "late",
        "chance": 0.16,
        "requires": {"type": "global", "key": "heat", "cmp": "gte", "value": 50},
    },
    {
        "phase": "late",
        "chance": 0.14,
        "requires": {"type": "global", "key": "agiProgress", "cmp": "gte", "value": 60},
    },
    {
        "phase": "endgame",
        "chance": 0.12,
        "requires": {"type": "global", "key": "agiProgress", "cmp": "gte", "value": 80},
    },
]

logistics_type = {
    0: "inventory",
    1: "funds",
    2: "defense",
    3: "funds",
    4: "funds",
    5: "defense",
    6: "funds",
    7: "defense",
    8: "funds",
    9: "inventory",
}

phase_effects = {
    "early": {
        "broadcast": {"publicSupport": 7, "heat": 4},
        "stealth": {"agiProgress": -5, "heat": 3},
        "funds": {"funds": 10, "publicSupport": -2},
        "inventory": {"funds": -6, "inventory": 1},
        "defense": {"defense": -3, "heat": 3},
    },
    "mid": {
        "broadcast": {"publicSupport": 9, "heat": 5},
        "stealth": {"agiProgress": -7, "heat": 4},
        "funds": {"funds": 14, "publicSupport": -3},
        "inventory": {"funds": -8, "inventory": 1},
        "defense": {"defense": -4, "heat": 4},
    },
    "late": {
        "broadcast": {"publicSupport": 11, "heat": 6},
        "stealth": {"agiProgress": -9, "heat": 5},
        "funds": {"funds": 18, "publicSupport": -4},
        "inventory": {"funds": -10, "inventory": 1},
        "defense": {"defense": -5, "heat": 5},
    },
    "endgame": {
        "broadcast": {"publicSupport": 13, "heat": 7},
        "stealth": {"agiProgress": -11, "heat": 6},
        "funds": {"funds": 22, "publicSupport": -5},
        "inventory": {"funds": -12, "inventory": 1},
        "defense": {"defense": -6, "heat": 6},
    },
}

contexts = [
    {
        "slug": "openai-rationing",
        "figure": "Sam Altman",
        "title_suffix": "Compute Rationing Stop",
        "hook_template": "OpenAI's 2025 compute rationing roadshow stops in {location} after the Senate subpoena on GPU hoarding",
        "angle": "Altman keeps promising a pause while shopping for off-book clusters.",
        "subject_template": "activists surrounding 2025 OpenAI compute rationing stage in {location}",
        "broadcast_label": "Hijack Altman's rationing Q&A in {location}.",
        "broadcast_body": "Beam in union pay stubs while Altman dodges the pause pledge.",
        "stealth_label": "Slip our analysts into the OpenAI support tent.",
        "stealth_body": "Clone the compliance tablets that track emergency GPU shipments.",
        "logistics_templates": {
            "funds": {
                "label": "Work the venture hangers-on outside {location}.",
                "body": "Trade rumors about the next GPT pivot for hush-money pledges.",
            },
            "inventory": {
                "label": "Lift badge stock from the merch kiosk.",
                "body": "Pocket NFC laminates before security clocks the swap.",
            },
            "defense": {
                "label": "Feed spoofed evacuation maps to the venue ops.",
                "body": "Send their private patrols chasing phantom bomb threats.",
            },
        },
        "locations": [
            {"name": "San Francisco", "detail": "Embarcadero pier stage"},
            {"name": "Sacramento", "detail": "Capitol annex lawn"},
            {"name": "Seattle", "detail": "South Lake Union amphitheater"},
            {"name": "Austin", "detail": "South Congress pop-up"},
            {"name": "Chicago", "detail": "Riverwalk pavilion"},
            {"name": "Boston", "detail": "Seaport innovation pier"},
            {"name": "Atlanta", "detail": "Midtown media lot"},
            {"name": "Denver", "detail": "RiNo warehouse"},
            {"name": "Miami", "detail": "Wynwood soundstage"},
            {"name": "New York City", "detail": "Hudson Yards atrium"},
        ],
    },
    {
        "slug": "google-curfew",
        "figure": "Sundar Pichai",
        "title_suffix": "Waymo Curfew Briefing",
        "hook_template": "Waymo's 2025 midnight curfew pilots roll through {location} after the Phoenix protests",
        "angle": "Pichai claims curfews keep streets safe while lobbyists map new surveillance routes.",
        "subject_template": "activists surrounding 2025 Waymo curfew briefing in {location}",
        "broadcast_label": "Hijack the Waymo safety briefing livestream.",
        "broadcast_body": "Loop curfew dashcam clips that show empty streets and idle cops.",
        "stealth_label": "Shadow the lidar calibration van.",
        "stealth_body": "Swap the firmware on their night patrol routes.",
        "logistics_templates": {
            "funds": {
                "label": "Pass the hat at the rideshare driver meetup.",
                "body": "Trade strike intel for donations before they clock out.",
            },
            "inventory": {
                "label": "Borrow the spare lidar rigs from their demo tent.",
                "body": "Wheel them onto our shuttle before PR notices.",
            },
            "defense": {
                "label": "Feed fake curfew alerts to the precinct desk.",
                "body": "Force their drones to babysit phantom protests.",
            },
        },
        "locations": [
            {"name": "Phoenix", "detail": "Roosevelt Row stage"},
            {"name": "San Diego", "detail": "Gaslamp garage"},
            {"name": "Los Angeles", "detail": "Arts District depot"},
            {"name": "Las Vegas", "detail": "Fremont Street terminal"},
            {"name": "Houston", "detail": "EaDo shuttle lot"},
            {"name": "Miami", "detail": "Brickell plaza"},
            {"name": "Atlanta", "detail": "BeltLine hub"},
            {"name": "Chicago", "detail": "Fulton Market bay"},
            {"name": "Newark", "detail": "Ironbound garage"},
            {"name": "Washington, D.C.", "detail": "NoMa command van"},
        ],
    },
    {
        "slug": "microsoft-water",
        "figure": "Satya Nadella",
        "title_suffix": "Desert Cooling Hearing",
        "hook_template": "Microsoft's 2025 desert cooling purchase hearings hit {location} after the Arizona water lawsuits",
        "angle": "Nadella keeps promising recycled water while pumping rivers dry.",
        "subject_template": "activists challenging 2025 Microsoft desert cooling hearing in {location}",
        "broadcast_label": "Broadcast the evaporative tower protest in {location}.",
        "broadcast_body": "Cut in footage of dried canals while Nadella talks sustainability.",
        "stealth_label": "Tap the environmental sensors in the testimony room.",
        "stealth_body": "Copy the discharge readings before they get scrubbed.",
        "logistics_templates": {
            "funds": {
                "label": "Host a pop-up merch table for the water rights coalition.",
                "body": "Sell reclaimed tech and split the haul with organizers.",
            },
            "inventory": {
                "label": "Stash the trial desal membranes in our van.",
                "body": "Borrow the demo kit before the lobbyists pack it up.",
            },
            "defense": {
                "label": "Send sabotage tips to the irrigation contractors.",
                "body": "Coach them on how to ride the cooling pipes until valves snap.",
            },
        },
        "locations": [
            {"name": "Phoenix", "detail": "Tempe municipal court"},
            {"name": "Tucson", "detail": "Sonoran civic hall"},
            {"name": "Las Cruces", "detail": "Mesilla county chambers"},
            {"name": "Albuquerque", "detail": "South Valley hearing room"},
            {"name": "Salt Lake City", "detail": "Jordan River forum"},
            {"name": "Reno", "detail": "Truckee basin council"},
            {"name": "El Paso", "detail": "Franklin Mountains annex"},
            {"name": "San Bernardino", "detail": "Inland Empire water board"},
            {"name": "Fresno", "detail": "Central Valley rotunda"},
            {"name": "Las Vegas", "detail": "Clark County commission dais"},
        ],
    },
    {
        "slug": "nvidia-lotto",
        "figure": "Jensen Huang",
        "title_suffix": "GPU Lottery Showcase",
        "hook_template": "NVIDIA's 2025 GPU lottery showcase parks in {location} after new export license rules",
        "angle": "Huang parades golden wafers while labs without clearance beg for scraps.",
        "subject_template": "activists surrounding 2025 NVIDIA GPU lottery showcase in {location}",
        "broadcast_label": "Crash the GPU raffle stream in {location}.",
        "broadcast_body": "Splice in the clip where Huang jokes about compute scarcity.",
        "stealth_label": "Seed our malware into the demo cluster.",
        "stealth_body": "Slip a patch onto the DGX rack before it ships.",
        "logistics_templates": {
            "funds": {
                "label": "Auction counterfeit backdoor keys to desperate founders.",
                "body": "Trade access rumors for crypto pledges.",
            },
            "inventory": {
                "label": "Pocket the spare PCIe bridges from their bench.",
                "body": "Swap in blanks before the engineers notice.",
            },
            "defense": {
                "label": "Feed thermal sabotage tips to unionized installers.",
                "body": "Teach them to miscalibrate coolant loops.",
            },
        },
        "locations": [
            {"name": "San Jose", "detail": "Convention rotunda"},
            {"name": "Sunnyvale", "detail": "Mathilda Ave pavilion"},
            {"name": "Portland", "detail": "Pearl District expo"},
            {"name": "Vancouver", "detail": "Waterfront tech pier"},
            {"name": "Boise", "detail": "Treasure Valley hall"},
            {"name": "Minneapolis", "detail": "North Loop arena"},
            {"name": "Detroit", "detail": "New Center hangar"},
            {"name": "Toronto", "detail": "Harbourfront innovation dome"},
            {"name": "Montreal", "detail": "Old Port tradeshow"},
            {"name": "Boston", "detail": "Hynes convention bay"},
        ],
    },
    {
        "slug": "meta-llama",
        "figure": "Mark Zuckerberg",
        "title_suffix": "Llama Licensing Town Hall",
        "hook_template": "Meta's 2025 Llama licensing town hall pitches roll through {location} after the EU AI Act deal",
        "angle": "Zuckerberg touts openness while hoarding moderation data.",
        "subject_template": "activists heckling 2025 Meta llama licensing town hall in {location}",
        "broadcast_label": "Flood the Llama Q&A with our data-tracking dossier.",
        "broadcast_body": "Project the slide where Meta begged Brussels for exemptions.",
        "stealth_label": "Ghost into the reality lab breakout room.",
        "stealth_body": "Copy the licensing contracts they promised regulators.",
        "logistics_templates": {
            "funds": {
                "label": "Charge donor selfies with the retro headset prototypes.",
                "body": "Upsell them on naming rights for safe model releases.",
            },
            "inventory": {
                "label": "Pocket the AR input gloves from backstage.",
                "body": "Hand them to our researchers for sensor spoofing.",
            },
            "defense": {
                "label": "Feed misinformation into their threat hunting queue.",
                "body": "Force Meta's red team to chase our planted phantom leaks.",
            },
        },
        "locations": [
            {"name": "Menlo Park", "detail": "MPK campus plaza"},
            {"name": "Austin", "detail": "Domain XR studio"},
            {"name": "New York City", "detail": "Chelsea event loft"},
            {"name": "London", "detail": "King's Cross gallery"},
            {"name": "Paris", "detail": "La Défense atrium"},
            {"name": "Berlin", "detail": "Kreuzberg warehouse"},
            {"name": "Dublin", "detail": "Docklands forum"},
            {"name": "Madrid", "detail": "Gran Via theatre"},
            {"name": "Rome", "detail": "Eur convention hall"},
            {"name": "Warsaw", "detail": "Vistula tech hub"},
        ],
    },
    {
        "slug": "xai-grok",
        "figure": "Elon Musk",
        "title_suffix": "xAI Grok Recruitment Rally",
        "hook_template": "xAI's 2025 Grok recruitment rallies storm {location} after the Texas gigafactory data breach",
        "angle": "Musk promises open-source truths while training on every leaked DM.",
        "subject_template": "activists skewering 2025 xAI grok rally in {location}",
        "broadcast_label": "Hijack Musk's Grok monologue with our fact-check crawl.",
        "broadcast_body": "Overlay the breach timeline as he riffs about free speech.",
        "stealth_label": "Slip EMP tags into the recruit swag bags.",
        "stealth_body": "Track which regions their scouts target for compute.",
        "logistics_templates": {
            "funds": {
                "label": "Sell limited-run 'Grok ate my homework' zines.",
                "body": "Swap them for crypto donations from disillusioned fans.",
            },
            "inventory": {
                "label": "Rewire the starlink demo routers.",
                "body": "Pocket the mesh nodes once the lights go down.",
            },
            "defense": {
                "label": "Feed bogus FAA compliance logs to the drone marshals.",
                "body": "Send their escorts on a paperwork goose chase.",
            },
        },
        "locations": [
            {"name": "Austin", "detail": "Gigafactory pavilion"},
            {"name": "Dallas", "detail": "Deep Ellum hangar"},
            {"name": "Houston", "detail": "Spaceport visitor center"},
            {"name": "Boca Chica", "detail": "Starbase amphitheater"},
            {"name": "Tulsa", "detail": "Riverfront stage"},
            {"name": "Kansas City", "detail": "West Bottoms arena"},
            {"name": "St. Louis", "detail": "Gateway freight shed"},
            {"name": "Nashville", "detail": "Gulch tech loft"},
            {"name": "Orlando", "detail": "Space Coast expo"},
            {"name": "Charlotte", "detail": "South End studio"},
        ],
    },
    {
        "slug": "anthropic-drill",
        "figure": "Dario Amodei",
        "title_suffix": "Redwood Safety Drill",
        "hook_template": "Anthropic's 2025 Redwood Coast safety drills land in {location} after the leaked scaling manifesto",
        "angle": "Amodei swears safety is baked in while negotiating secret Titania leases.",
        "subject_template": "activists observing 2025 Anthropic safety drill in {location}",
        "broadcast_label": "Stream the overclocked fire drill in {location}.",
        "broadcast_body": "Highlight the slide where Dario shrugs off transformer risks.",
        "stealth_label": "Ghostwrite the incident report tablets.",
        "stealth_body": "Insert our redlines into their emergency scripts.",
        "logistics_templates": {
            "funds": {
                "label": "Host a midnight teach-in on Anthropic's venture loans.",
                "body": "Collect pledges from climate groups sharing the stage.",
            },
            "inventory": {
                "label": "Pocket the redundant thermal cameras.",
                "body": "Mount them on our next reconnaissance van.",
            },
            "defense": {
                "label": "Feed sabotage macros to the contractor clipboard.",
                "body": "Rewrite their lockout-tagout checklist.",
            },
        },
        "locations": [
            {"name": "Arcata", "detail": "Humboldt fairground"},
            {"name": "Eureka", "detail": "Harborfront drill site"},
            {"name": "Portland", "detail": "Willamette annex"},
            {"name": "Sacramento", "detail": "Natomas training yard"},
            {"name": "Salem", "detail": "Capitol mall staging"},
            {"name": "Olympia", "detail": "Maritime incident dome"},
            {"name": "Bellingham", "detail": "Bayside depot"},
            {"name": "Tacoma", "detail": "Port authority bunker"},
            {"name": "Vancouver", "detail": "False Creek terminal"},
            {"name": "Victoria", "detail": "Inner Harbour drill yard"},
        ],
    },
    {
        "slug": "scaleai-contract",
        "figure": "Alex Wang",
        "title_suffix": "Defense Labeling Expo",
        "hook_template": "Scale AI's 2025 defense labeling expo hits {location} after the Pentagon drone tender leaks",
        "angle": "Wang talks about safety while inking live-fire annotation deals.",
        "subject_template": "activists infiltrating 2025 Scale AI defense expo in {location}",
        "broadcast_label": "Hijack the Pentagon showcase livestream.",
        "broadcast_body": "Roll the leaked contract slide that prices out soldier data.",
        "stealth_label": "Swap their sample drone footage.",
        "stealth_body": "Slip our deepfake overlays into the training set.",
        "logistics_templates": {
            "funds": {
                "label": "Charge consulting fees to anxious subcontractors.",
                "body": "Upsell them on 'ethics compliance' kits we invented.",
            },
            "inventory": {
                "label": "Pocket the hardened SSDs from the booth.",
                "body": "Seed them into our mobile racks.",
            },
            "defense": {
                "label": "Feed false readiness stats to the visiting generals.",
                "body": "Force them to reassign guards to meaningless demos.",
            },
        },
        "locations": [
            {"name": "San Antonio", "detail": "Port San Antonio hangar"},
            {"name": "Colorado Springs", "detail": "Space command concourse"},
            {"name": "Tampa", "detail": "MacDill expo hall"},
            {"name": "Norfolk", "detail": "Naval yard pavilion"},
            {"name": "San Diego", "detail": "Miramar flightline"},
            {"name": "Huntsville", "detail": "Rocket City arsenal"},
            {"name": "Dayton", "detail": "Wright-Patt briefing room"},
            {"name": "Charleston", "detail": "Joint Base hangar"},
            {"name": "Anchorage", "detail": "Arctic testing dome"},
            {"name": "Honolulu", "detail": "Pearl Harbor ops deck"},
        ],
    },
    {
        "slug": "stanford-ethics",
        "figure": "Fei-Fei Li",
        "title_suffix": "AI Ethics Hackathon",
        "hook_template": "Stanford's 2025 AI ethics hackathon roadshow lands in {location} after the White House data rights order",
        "angle": "Li invites Big Tech to workshop guidelines while quietly logging every participant's biometrics.",
        "subject_template": "activists remixing 2025 AI ethics hackathon in {location}",
        "broadcast_label": "Seize the ethics keynote stream in {location}.",
        "broadcast_body": "Project the new federal order while sponsors pitch growth hacks.",
        "stealth_label": "Slip our prompts into the judging rubric.",
        "stealth_body": "Steer their prototypes toward datacenter vulnerabilities.",
        "logistics_templates": {
            "funds": {
                "label": "Launch a flash grant booth for community labs.",
                "body": "Redirect corporate philanthropy into our strike fund.",
            },
            "inventory": {
                "label": "Pocket the donated edge TPUs.",
                "body": "Wire them into our sensor nets.",
            },
            "defense": {
                "label": "Feed critique packets to campus facility crews.",
                "body": "Convince them to delay badge upgrades at Big Tech satellites.",
            },
        },
        "locations": [
            {"name": "Palo Alto", "detail": "Main quad pavilion"},
            {"name": "San Francisco", "detail": "Mission Street loft"},
            {"name": "Los Angeles", "detail": "Arts District studio"},
            {"name": "New York City", "detail": "SoHo maker loft"},
            {"name": "Boston", "detail": "Kendall Square lab"},
            {"name": "Toronto", "detail": "MaRS discovery hall"},
            {"name": "Seattle", "detail": "South Lake Union hub"},
            {"name": "Chicago", "detail": "South Loop incubator"},
            {"name": "Austin", "detail": "East Side co-op"},
            {"name": "Atlanta", "detail": "Poncey-Highland civic lab"},
        ],
    },
    {
        "slug": "ftc-audit",
        "figure": "Lina Khan",
        "title_suffix": "Data Audit Dragnet",
        "hook_template": "The FTC's 2025 AI data audit dragnet sweeps through {location} after the whistleblower leaks",
        "angle": "Khan promises accountability while the corps stage-managed every raid.",
        "subject_template": "activists tailing 2025 FTC data audit teams in {location}",
        "broadcast_label": "Livestream the audit convoy bottleneck.",
        "broadcast_body": "Narrate how the firms rehearsed every search warrant.",
        "stealth_label": "Ride along with the seized server crates.",
        "stealth_body": "Swap labels so the juiciest racks land in public evidence.",
        "logistics_templates": {
            "funds": {
                "label": "Turn the press scrum into a fundraiser.",
                "body": "Sell rapid-response legal consults to anxious startups.",
            },
            "inventory": {
                "label": "Pocket the leftover Faraday bags.",
                "body": "Line our safehouse shelves with them.",
            },
            "defense": {
                "label": "Feed fake compliance memos to the private guards.",
                "body": "Make them reassign patrols away from our next target.",
            },
        },
        "locations": [
            {"name": "San Francisco", "detail": "South of Market convoy"},
            {"name": "Seattle", "detail": "Sodo loading dock"},
            {"name": "Portland", "detail": "Lower Albina warehouse"},
            {"name": "Los Angeles", "detail": "Silicon Beach office park"},
            {"name": "Phoenix", "detail": "Tempe records annex"},
            {"name": "Dallas", "detail": "Legacy tech corridor"},
            {"name": "Chicago", "detail": "West Loop freight lane"},
            {"name": "New York City", "detail": "Hudson River pier"},
            {"name": "Boston", "detail": "Seaport evidence bay"},
            {"name": "Washington, D.C.", "detail": "Navy Yard evidence bunker"},
        ],
    },
]


def slugify(text: str) -> str:
    return "-".join(
        "".join(ch.lower() for ch in part if ch.isalnum())
        for part in text.split()
    )


def build_body(context: dict, location: dict) -> str:
    return (
        f"In 2025, {context['hook_template'].format(location=location['name'])}. "
        f"{context['figure']} floods {location['name']} with cameras at the {location['detail']}, "
        f"and our crews can bend the spectacle to tilt public support, funds, AGI momentum, and heat before security closes ranks."
    )


def build_image_prompt(context: dict, location: dict) -> str:
    subject = context["subject_template"].format(location=location["name"])
    return (
        "retro futurist protest poster, screenprint texture, light cyan and persimmon palette, "
        f"{subject}, dynamic perspective, simple shapes, minimal text, 2025 dystopian satire"
    )


def build_choice(event_id: str, kind: str, context: dict, location: dict, phase: str):
    effects_config = phase_effects[phase][kind]
    effects = []
    if kind == "broadcast":
        effects.append({
            "target": {"type": "global", "key": "publicSupport"},
            "op": "add",
            "value": effects_config["publicSupport"],
        })
        effects.append({
            "target": {"type": "global", "key": "heat"},
            "op": "add",
            "value": effects_config["heat"],
        })
        label = context["broadcast_label"].format(location=location["name"])
        body = context["broadcast_body"].format(location=location["name"])
    elif kind == "stealth":
        effects.append({
            "target": {"type": "global", "key": "agiProgress"},
            "op": "add",
            "value": effects_config["agiProgress"],
        })
        effects.append({
            "target": {"type": "global", "key": "heat"},
            "op": "add",
            "value": effects_config["heat"],
        })
        label = context["stealth_label"].format(location=location["name"])
        body = context["stealth_body"].format(location=location["name"])
    else:
        template = context["logistics_templates"][kind]
        label = template["label"].format(location=location["name"])
        body = template["body"].format(location=location["name"])
        if kind == "funds":
            effects.append({
                "target": {"type": "global", "key": "funds"},
                "op": "add",
                "value": effects_config["funds"],
            })
            effects.append({
                "target": {"type": "global", "key": "publicSupport"},
                "op": "add",
                "value": effects_config["publicSupport"],
            })
        elif kind == "inventory":
            inventory_key = f"inv:{slugify(event_id)}"
            effects.append({
                "target": {"type": "inventory", "key": inventory_key},
                "op": "add",
                "value": 1,
            })
            effects.append({
                "target": {"type": "global", "key": "funds"},
                "op": "add",
                "value": effects_config["funds"],
            })
        elif kind == "defense":
            effects.append({
                "target": {"type": "datacenters", "key": "defense"},
                "op": "add",
                "value": effects_config["defense"],
            })
            effects.append({
                "target": {"type": "global", "key": "heat"},
                "op": "add",
                "value": effects_config["heat"],
            })
    return {
        "id": f"ch:{slugify(event_id)}-{kind}",
        "label": label,
        "body": body,
        "effects": effects,
    }


def primary_stats_for(kind: str) -> list[str]:
    base = ["heat", "funds", "publicSupport", "agi"]
    if kind == "inventory":
        base.append("inventory")
    elif kind == "defense":
        base.append("defense")
    return base


def main() -> None:
    events = []
    for context in contexts:
        for idx, location in enumerate(context["locations"]):
            variation = phase_variations[idx]
            phase = variation["phase"]
            logistics = logistics_type[idx]
            event_id = f"ev:{context['slug']}-{slugify(location['name'])}"
            title = f"{location['name']} {context['title_suffix']}"
            body = build_body(context, location)
            trigger = {
                "when": "onTick",
                "chance": variation["chance"],
            }
            requires = variation.get("requires")
            if requires:
                trigger["requires"] = [requires]
            event = {
                "id": event_id,
                "title": title,
                "body": body,
                "year": 2025,
                "phase": phase,
                "primaryStats": primary_stats_for(logistics),
                "triggers": [trigger],
                "oneTime": True,
                "choices": [
                    build_choice(event_id, "broadcast", context, location, phase),
                    build_choice(event_id, "stealth", context, location, phase),
                    build_choice(event_id, logistics, context, location, phase),
                ],
                "imagePrompt": build_image_prompt(context, location),
            }
            events.append(event)
    data = {
        "version": "2025.0",
        "style": {
            "year": 2025,
            "imagePromptTemplate": "retro futurist protest poster, screenprint texture, light cyan and persimmon palette, {subject}, dynamic perspective, simple shapes, minimal text, 2025 dystopian satire",
            "languageNotes": "Keep every blurb understandable by an average tech worker; reference real 2024-2025 happenings before leaning into satire.",
        },
        "targets": {
            "totalEvents": 100,
            "phases": {
                "early": 30,
                "mid": 40,
                "late": 20,
                "endgame": 10,
            },
            "statCoverageMinimums": {
                "heat": 40,
                "agi": 35,
                "funds": 45,
                "publicSupport": 30,
                "defense": 25,
                "inventory": 20,
            },
        },
        "templates": [
            {
                "id": "ev:template",
                "title": "Template Title",
                "body": "One-paragraph summary of a 2025 tech backlash scenario.",
                "year": 2025,
                "phase": "early",
                "primaryStats": ["heat", "funds"],
                "triggers": [],
                "oneTime": True,
                "choices": [],
                "imagePrompt": "retro futurist protest poster, screenprint texture, light cyan and persimmon palette, laid-off engineers debating drone strike ethics, dynamic perspective, simple shapes, minimal text, 2025 dystopian satire",
            }
        ],
        "events": events,
    }
    output_path = Path("branching_storyline_generation/content/events.json")
    output_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
