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
   Win Aura Clashes / train  <----  Condense Immortal Cores (spend free AP)
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

A character's effective rating in a stat = **mortal cores + immortal cores**.

| Core       | Fantasy meaning                | CK3 hook (target)                          |
|------------|--------------------------------|--------------------------------------------|
| Power      | Raw striking / destructive aura| Prowess; Aura Clash attack                 |
| Agility    | Speed, evasion, finesse        | Prowess/Intrigue; Aura Clash initiative    |
| Fortitude  | Toughness, endurance, healing  | Health, fewer wounds; Aura Clash defense   |
| Soul       | Willpower, perception, control | Stress/dread resistance; Aura Clash tempo  |

Cores are tracked as engine variables — mortal `aura_mc_{power,fortitude,agility,soul}`
and immortal `aura_ic_{…}` — summed by script values `aura_{stat}_value`. They feed
the Aura Clash resolution today; variable-driven passive modifiers come later.

## Elements (8, master up to 2)

Fire, Storm, Wind, Earth, Ice, Water, Light, Darkness — each a non-exclusive
trait (`aura_element_*`). A scripted trigger caps mastery at the appropriate
number of elements (normally 2). Elements color the aura and gate certain techniques.

## Martial arts styles (5)

Distinct combat philosophies (`aura_style_*`) that bias the cores and unlock
style-specific techniques. A character commits to a style as they cultivate.

## Aura Clash (the duel)

A character interaction, `aura_clash_interaction`, lets one martial artist
challenge another. Resolution compares effective cores (mortal + immortal,
immortal weighted heavier) via `aura_clash_power_value`, and will grow to factor
in elements/styles and spent Chi through a structured event chain — producing a
winner, consequences (prestige, injuries, claims, hooks), and flavor. This is the
signature system and will be expanded in its own iteration.

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
