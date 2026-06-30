# Aura Kings — Design Document

## Vision

CK3 is, at its heart, a simulation of people competing for power through
inheritance, war, intrigue, and faith. *Aura Clash* is a simulation of a person
becoming powerful through cultivation. *Aura Kings* fuses the two: every
character can walk the path of cultivation, and **personal power becomes a form
of political power**. A peasant who cultivates to a high realm can challenge —
and overthrow — a king who never trained.

The mod should feel like CK3 first: it adds systems via traits, decisions,
events, character interactions, and modifiers rather than fighting the engine.

## Design pillars

1. **Cultivation is a parallel progression track.** It runs alongside (not
   instead of) titles and lifestyles. A character advances through **realms** by
   accumulating and refining **Chi**.
2. **The four cores matter mechanically.** Power, Agility, Fortitude, and Soul
   each hook into existing CK3 systems (combat, schemes, health, stress/sanity)
   so cultivation has tangible payoffs.
3. **Identity through choice.** Elements (pick 2 of 8) and martial styles
   (pick from 5) give every cultivator a distinct kit and flavor, expressed via
   traits, modifiers, and unlocked techniques.
4. **Conflict resolves in the Aura Clash.** A bespoke character interaction lets
   cultivators duel with their auras — a structured, stat-driven confrontation
   that can settle rivalries, claims, and honor.
5. **Sects are the social layer.** Cultivation organizations sit alongside (and
   eventually intertwine with) faiths and factions, providing teachers,
   techniques, and politics.

## Core loop

```
                  Begin Martial Training (aura_martial_artist)
                              |  forge mortal cores (max 8)
                              v
   Gather Aura Pressure  ->  free AP accumulates  ->  Awaken (aura_cultivator)
        ^                                                     |  + Foundation
        |                                                     v
   train / earn AP  <------------  Condense Immortal Cores (spend free AP)
```

There are **two progression layers** (see the source guide,
`AURA_CLASH_GAME_GUIDE.md`):

1. **Mortal cores** — trained by any **Martial Artist** (`aura_martial_artist`
   trait, learned from a teacher / manual / self-study). Capped at **8 total**
   across the four stats; everyone starts with 1 in each (4 free to place).
2. **Immortal cores** — condensed from **free Aura Pressure** once a Martial
   Artist **awakens** into a **Cultivator** (`aura_cultivator` trait, which is
   kept alongside Martial Artist) and gains a **Foundation**.

- **Aura Pressure** is the long-term cultivation meter, tracked two ways:
  `aura_pressure_total` (lifetime) and `aura_pressure_free` (unspent, condensable
  into immortal cores).
- **Chi** (a separate, short-term *combat stamina* pool — not yet modeled) is
  spent during the Aura Clash; do not conflate it with Aura Pressure.

## The four cores — multi-track leveled traits

The cores are **multi-track leveled traits** (the same machinery as vanilla
`lifestyle_hunter`/`blademaster`). Each stat — Power, Fortitude, Agility, Soul —
is a **track** inside the trait: a track's XP is the cores forged in that stat,
its level is that core's **realm tier**, and the four track levels sum to the
trait's overall level.

- `aura_martial_artist` — 4 mortal-core tracks (8-core cap; small tiers).
- `aura_cultivator` — 4 immortal-core tracks; 5 realm tiers per track at
  **1 / 10 / 30 / 75 / 150** cores. A focused Archon (~100–150 in one core) is
  flatly superhuman.

A core is one point of track XP: `add_trait_xp = { trait = … track = … value = 1 }`.
**Passive benefits are the track-level modifiers themselves** (cumulative — base
+ every reached level, exactly like blademaster's +3/+6/+12), so there is no
separate stat recalculation:

| Core | Track modifiers (cumulative across tiers) |
|------|-------------------------------------------|
| **Power** | Prowess (→ ~+100 at the top tier) |
| **Agility** | Prowess (→ ~+80) |
| **Fortitude** | Prowess + Health + life expectancy; **no-age-prowess-loss at tier 2 (10 cores)** |
| **Soul** | Learning (+ minor piety) |

**Agelessness:** when the Fortitude immortal track passes **50** cores,
`aura_check_ageless_effect` grants the **`aura_ageless`** trait (`immortal = yes`)
— a trait can't be granted by a track modifier, so this one step is scripted.

Numbers verified against vanilla (track modifiers stack; `add_trait_xp` /
`has_trait_xp` confirmed). Soul Dread/Prestige flavor and richer per-core
benefits can be layered into the track levels later.

## Elements (8, master up to 2)

Fire, Storm, Wind, Earth, Ice, Water, Light, Darkness — each a non-exclusive
trait (`aura_element_*`). A scripted trigger caps mastery at the appropriate
number of elements (normally 2). Elements color the aura and gate certain techniques.

## Martial arts styles (5)

Distinct combat philosophies (`aura_style_*`) that bias the cores and unlock
style-specific techniques. A character commits to a style as they cultivate.

## Aura Clash (the duel) — planned, not yet built

The signature confrontation between cultivators. This will **not** be a single
"bigger number wins" comparison — it is meant to be an in-depth, interactive duel
driven by **techniques and decisions**: round-by-round choices, spending Chi,
elemental/style matchups, feints and counters, with cores as inputs rather than
the whole story. Designed in its own iteration. (An earlier placeholder
interaction that just compared a clash-power value has been removed so it doesn't
anchor the design to that approach.)

## Sects (future)

Cultivation organizations that teach techniques, grant ranks, and create
politics. Modeled later — likely as a blend of decisions, court-position-like
roles, and a custom membership variable. Tracked here so current data leaves
room for it (e.g., realm thresholds reference "sect access").

## Out of scope for the groundwork commit

Balancing, art assets, full technique catalog, sect simulation, AI cultivation
behavior, and map/setting changes. The current commit establishes structure and
the minimal working spine (initialize -> gain Chi -> advance realm -> clash stub)
so these can be layered in.
