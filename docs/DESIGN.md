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
Absorb Chi  ->  Refine Chi into a Core / Aura  ->  Meet realm threshold
     ^                                                     |
     |                                                     v
 Win Aura Clashes / train / meditate  <-----------  Advance Realm (new powers)
```

- **Chi** is a per-character stored resource (engine variable `aura_chi`).
- Characters gain Chi over time (meditation, training, victories, locations,
  decisions) and spend it to **advance realms** and fuel **techniques**.
- Each **realm** grants a tiered trait with escalating modifiers and unlocks new
  options (more element slots, stronger techniques, access to higher sects).

## Cultivation realms (initial ladder)

| Level | Realm trait            | Theme                         |
|-------|------------------------|-------------------------------|
| 0     | *(none)* — Mortal      | No aura; cannot sense Chi     |
| 1     | `aura_realm_initiate`  | First Chi sensing / awakening |
| 2     | `aura_realm_adept`     | Aura forged                   |
| 3     | `aura_realm_warrior`   | Aura manifests in combat      |
| 4     | `aura_realm_master`    | Element mastery deepens       |
| 5     | `aura_realm_grandmaster`| Techniques empower the realm |
| 6     | `aura_realm_sovereign` | Aura dominates the battlefield|
| 7     | `aura_realm_ascendant` | Heavenly Ascension achieved   |

These names/thresholds are placeholders to be tuned. The grouped-trait
implementation means a character holds exactly one realm trait at a time and
advancing automatically removes the previous one.

## The four cores

| Core       | Fantasy meaning                | CK3 hook (initial)                         |
|------------|--------------------------------|--------------------------------------------|
| Power      | Raw striking / destructive Chi | Prowess; Aura Clash attack                 |
| Agility    | Speed, evasion, finesse        | Prowess/Intrigue; Aura Clash initiative    |
| Fortitude  | Toughness, endurance, healing  | Health, fewer wounds; Aura Clash defense   |
| Soul       | Willpower, perception, control | Stress/dread resistance; Aura Clash tempo  |

Cores are tracked as engine variables (`aura_power`, `aura_agility`,
`aura_fortitude`, `aura_soul`) so they can grow independently of realm and feed
both passive modifiers and the Aura Clash resolution.

## Elements (8, master up to 2)

Fire, Storm, Wind, Earth, Ice, Water, Light, Darkness — each a non-exclusive
trait (`aura_element_*`). A scripted trigger caps mastery at the realm-appropriate
number of elements. Elements color the aura and gate certain techniques.

## Martial arts styles (5)

Distinct combat philosophies (`aura_style_*`) that bias the cores and unlock
style-specific techniques. A character commits to a style as they cultivate.

## Aura Clash (the duel)

A character interaction, `aura_clash_interaction`, lets one cultivator challenge
another. Resolution compares cores + realm + elements/styles + spent Chi through
a structured event chain, producing a winner, consequences (prestige, injuries,
claims, hooks), and flavor. This is the signature system and will be expanded in
its own iteration.

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
