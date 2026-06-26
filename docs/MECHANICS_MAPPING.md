# Aura Clash → CK3 Mechanics Mapping

A quick-reference table translating each *Aura Clash* mechanic into the CK3
construct that implements (or will implement) it. "Status" notes whether the
groundwork commit has a working stub or it's a documented placeholder.

| Aura Clash concept            | CK3 implementation                                              | Where                                              | Status      |
|-------------------------------|----------------------------------------------------------------|----------------------------------------------------|-------------|
| **Aura Pressure** (cultivation meter) | Variables `aura_pressure_total` + `aura_pressure_free`; script values `aura_total_pressure_value` / `aura_free_pressure_value` | `common/scripted_effects`, `common/script_values` | done (basic) |
| **Chi** (combat stamina)      | *Not yet modeled* — will be a separate short-term pool (`maxchi = pool + soul/2`) | future | planned |
| **Martial Artist** (learned path) | Trait `aura_martial_artist`; tracks mortal cores                  | `common/traits/00_aura_core_traits.txt`            | done (basic) |
| **Cultivator** (awakened)     | Trait `aura_cultivator` (requires & keeps Martial Artist); tracks immortal cores | `common/traits/00_aura_core_traits.txt`            | done (basic) |
| **Mortal cores** (trained, max 8) | Variables `aura_mc_{power,fortitude,agility,soul}`, capped via `aura_mortal_cores_remaining_value` | script values + effects | done (basic) |
| **Mortal-core training (EXP)** | Per-stat EXP `aura_mc_{stat}_exp`; 100 EXP -> +1 core via `aura_gain_mortal_core_exp_effect` | scripted effects + script values | done (basic) |
| **Martial Training session** | `aura_martial_training_decision` (6mo cooldown) -> format/core/method event chain `aura_kings.0100-0103`; variable EXP by roll. Promotable to a CK3 Activity later. | `common/decisions`, `events` | done (basic) |
| **Immortal cores** (condensed) | Variables `aura_ic_{power,fortitude,agility,soul}`; `aura_condense_immortal_core_effect` | script values + effects | done (basic) |
| **Effective core rating**     | `aura_{power,fortitude,agility,soul}_value` = mortal + immortal     | `common/script_values`                             | done (basic) |
| **Passive benefits from cores** | Prowess (Pow/Agi/For), Health & life-expectancy & agelessness (For), Learning (Soul), via `aura_recalculate_passives_effect` (delta-applied base stats + tiered modifiers + `aura_ageless` trait) | script values, effects, modifiers, traits | done (needs in-game check) |
| **Awakening**                 | `aura_awaken_cultivation_decision`/`_effect` -> forced first immortal core (`aura_kings.0003`) -> Foundation (`aura_kings.0004`) | `common/decisions`, `events` | done (basic) |
| **Foundations (12 Zodiac)**   | Traits `aura_foundation_*` (Boar..Wolf), each a distinct CK3 benefit; chosen or inherited at awakening (`aura_inherit_foundation_effect`). Elemental color-base + element-mastery layer is a future addition. | `common/traits/03_aura_foundations.txt`, effects, events | done (basic) |
| **Aura Pressure gathering**   | `aura_gather_pressure_decision` (placeholder for lifestyle/passive) | `common/decisions`                                 | placeholder |
| **8 Elements (master 2)**     | Non-exclusive traits `aura_element_*`, capped by trigger       | `common/traits/01_aura_elements.txt`               | stub        |
| **5 Martial arts styles**     | Traits `aura_style_*`                                          | `common/traits/02_aura_styles.txt`                 | stub        |
| **Ranks (Novice→Sage)**       | 0–5 ladder on styles/elements                                  | future                                             | planned     |
| **Aura color**                | Derived from mastered elements + style (cosmetic)              | future GUI + script value                          | planned     |
| **Techniques (slotted, max 4)**| Modifiers + "equipped" variables / perks                      | `common/modifiers` (future)                        | planned     |
| **Aura Clash (the duel)**     | Planned in-depth duel driven by techniques + decisions (round-by-round, Chi spend, matchups) — **not** a number comparison. Placeholder interaction removed. | TBD | planned     |
| **Sects / clans**             | Decisions + membership variable + native vassal/faction hooks  | future                                             | planned     |
| **Demonic corruption**        | Hellscape capacity vs Taint variables                          | future                                             | planned     |
| **Difficulty (Jade Dragon / Mortal Limits)** | Game rule scaling AP gain / clash difficulty    | `common/game_rules` (future)                       | planned     |

## Variable & trait naming conventions

- **Prefix everything `aura_`** to avoid collisions with the base game and other
  mods.
- Character variables:
  - Aura Pressure: `aura_pressure_total`, `aura_pressure_free`.
  - Mortal cores: `aura_mc_power`, `aura_mc_fortitude`, `aura_mc_agility`, `aura_mc_soul`.
  - Mortal-core EXP: `aura_mc_{stat}_exp` (0..100 per stat).
  - Immortal cores: `aura_ic_power`, `aura_ic_fortitude`, `aura_ic_agility`, `aura_ic_soul`.
  - Transient training session: `aura_training_target` (flag), `aura_training_format`
    (flag), `aura_training_format_bonus`, `aura_training_last_gain`,
    `aura_training_session_gain`, `aura_training_core_gained` — set up and torn
    down by the session effects.
  - Bookkeeping: `aura_initialized`.
- Traits: `aura_martial_artist`, `aura_cultivator` (identity flags; cores live in
  variables), `aura_element_*`, `aura_style_*`.
- Scripted effects end in `_effect`, scripted triggers end in `_trigger`,
  script values end in `_value` (e.g. `aura_free_pressure_value`).
- Event namespace: `aura_kings` (e.g. `aura_kings.0001`).
- Localization keys mirror the object key (trait `aura_martial_artist` →
  loc key `aura_martial_artist` + `aura_martial_artist_desc`).

Keep this table in sync as mechanics move from `planned` → `stub` → `done`.
