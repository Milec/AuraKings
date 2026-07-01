# Aura Clash → CK3 Mechanics Mapping

A quick-reference table translating each *Aura Clash* mechanic into the CK3
construct that implements (or will implement) it. "Status" notes whether the
groundwork commit has a working stub or it's a documented placeholder.

| Aura Clash concept            | CK3 implementation                                              | Where                                              | Status      |
|-------------------------------|----------------------------------------------------------------|----------------------------------------------------|-------------|
| **Aura Pressure** (cultivation meter) | Variables `aura_pressure_total` + `aura_pressure_free`; script values `aura_total_pressure_value` / `aura_free_pressure_value` | `common/scripted_effects`, `common/script_values` | done (basic) |
| **Chi** (combat stamina)      | *Not yet modeled* — will be a separate short-term pool (`maxchi = pool + soul/2`) | future | planned |
| **Martial Artist** (learned path) | **Multi-track trait** `aura_martial_artist` (`category = lifestyle`) with 4 tracks (power/fortitude/agility/soul); mortal cores = track XP | `common/traits/00_aura_core_traits.txt` | done (needs in-game check) |
| **Cultivator** (awakened)     | **Multi-track trait** `aura_cultivator` with 4 tracks; immortal cores = track XP; **one track level per 100 XP** (= 1 core = 100 AP), up to level 100 (10000 XP) per track | `common/traits/00_aura_core_traits.txt` | done (needs in-game check) |
| **Cores (per-stat tracked level)** | A core = 100 track XP (`add_trait_xp = { trait track value = 100 }`); **one track level per core** so progress is always visible; 4 track levels sum to total. Passive benefits are the **track-level modifiers** (cumulative). | trait tracks | done (needs in-game check) |
| **Mortal cores** (trained, max 8) | XP on `aura_martial_artist` tracks; 8-total cap via `aura_mortal_cores_total` variable | effects + traits | done (basic) |
| **Mortal-core training (EXP)** | Per-stat EXP `aura_mc_{stat}_exp`; 100 EXP -> +1 core (`add_trait_xp`) via `aura_gain_mortal_core_exp_effect` | scripted effects + script values | done (basic) |
| **Martial Training session** | `aura_martial_training_decision` (6mo cooldown) -> format/core/method event chain `aura_kings.0100-0103`; variable EXP by roll | `common/decisions`, `events` | done (basic) |
| **Immortal cores** (condensed) | XP on `aura_cultivator` tracks; `aura_condense_immortal_core_effect` spends 100 AP -> `add_trait_xp` | effects + traits | done (basic) |
| **Passive benefits from cores** | Carried by the track-level modifiers themselves (Prowess on Pow/Agi/For; Health/life-expectancy/no-age-prowess on For; Learning on Soul). Agelessness (`aura_ageless`) granted at Fortitude track 50 via `aura_check_ageless_effect`. | trait tracks + effect | done (needs in-game check) |
| **Awakening**                 | `aura_awaken_cultivation_decision`/`_effect` -> forced first immortal core (`aura_kings.0003`) -> Foundation (`aura_kings.0004`) | `common/decisions`, `events` | done (basic) |
| **Foundations (types)**       | Traits `aura_foundation_*`: 4 Core, Fuel, 12 Zodiac, Flayed God, Jade Lotus. Chosen or inherited at awakening via two-step chooser (`aura_kings.0004`→`0005`/`0006`); `aura_inherit_foundation_effect`. Jade Dragon (cheat/start-bonus), elemental color-base, Kitsune, and mentor/sect gating are deferred. | `common/traits/03_aura_foundations.txt`, effects, events | done (basic) |
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
- **Cores live as trait-track XP**, not variables: `add_trait_xp = { trait =
  aura_martial_artist|aura_cultivator track = power|fortitude|agility|soul value = N }`;
  read with `has_trait_xp = { trait = X track = Y value >= N }`.
- Character variables:
  - Aura Pressure: `aura_pressure_total`, `aura_pressure_free`.
  - Mortal-core total (8 cap): `aura_mortal_cores_total`.
  - Mortal-core training EXP: `aura_mc_{stat}_exp` (0..100 sub-core progress).
  - Transient training session: `aura_training_target` (flag), `aura_training_format`
    (flag), `aura_training_format_bonus`, `aura_training_last_gain`,
    `aura_training_session_gain`, `aura_training_core_gained`.
  - Bookkeeping: `aura_initialized`.
- Traits: `aura_martial_artist`, `aura_cultivator` (multi-track leveled traits,
  `category = lifestyle`, tracks = the four cores), `aura_ageless`,
  `aura_foundation_*`, `aura_element_*`, `aura_style_*`.
- Scripted effects end in `_effect`, scripted triggers end in `_trigger`,
  script values end in `_value` (e.g. `aura_free_pressure_value`).
- Event namespace: `aura_kings` (e.g. `aura_kings.0001`).
- Localization keys mirror the object key (trait `aura_martial_artist` →
  loc key `aura_martial_artist` + `aura_martial_artist_desc`).

Keep this table in sync as mechanics move from `planned` → `stub` → `done`.
