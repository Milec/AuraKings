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

## The four cores (two tiers each)

A character's effective rating in a stat = **mortal cores + immortal cores**
(counted equally). High cultivators leave the human range entirely — an Archon
(~100 cores, ~10k AP) lives for centuries and slays great spirit beasts.

Cores are tracked as engine variables — mortal `aura_mc_{power,fortitude,agility,soul}`
and immortal `aura_ic_{…}` — summed by script values `aura_{stat}_value`.

### Passive benefits (per effective core in that stat)

| Core | Benefit per core | Notes |
|------|------------------|-------|
| **Power** | +1.5 Prowess | Raw striking force |
| **Agility** | +1.2 Prowess | Speed / finesse in a fight |
| **Fortitude** | +0.5 Prowess, +0.05 Health, +5 yrs life expectancy | Durability & longevity |
| **Soul** | +0.25 Learning | Insight / perception (more once techniques exist) |

**Fortitude longevity thresholds:** at **10** cores, age stops sapping prowess
(`no_prowess_loss_from_age` modifier); health & life expectancy rise (stepped per
10 cores); at **50** cores the character gains the **`aura_ageless`** trait
(`immortal = yes`) and can no longer die of old age.

Implementation (verified against `wiki_pages/`): `aura_recalculate_passives_effect`
recomputes the totals from core counts and applies them —
- **Prowess** (Pow/Agi/For) and **Learning** (Soul) via `add_prowess_skill` /
  `add_learning_skill`, as a delta vs `aura_applied_*` (values may be fractional;
  sub-point drift is cosmetic at these magnitudes);
- **Health + life expectancy** via stepped Fortitude tier modifiers
  (`aura_fortitude_tier_1..4`) — there is no `add_health` effect, so health must
  come from a modifier;
- **no-age-prowess-loss** and **agelessness** by threshold.

It runs whenever cores change and at game start. Soul's Dread / Prestige flavor
and a smooth (vs stepped) Fortitude curve are still to come.

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
