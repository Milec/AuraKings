# Aura Clash → CK3 Mechanics Mapping

A quick-reference table translating each *Aura Clash* mechanic into the CK3
construct that implements (or will implement) it. "Status" notes whether the
groundwork commit has a working stub or it's a documented placeholder.

| Aura Clash concept            | CK3 implementation                                              | Where                                              | Status      |
|-------------------------------|----------------------------------------------------------------|----------------------------------------------------|-------------|
| **Chi** (life-energy resource)| Character variable `aura_chi`, gained/spent via effects        | `common/scripted_effects`, `common/script_values`  | stub        |
| **Aura awakening**            | "Begin Cultivation" decision granting realm 1                  | `common/decisions`, `events`                       | stub        |
| **Cultivation realms**        | Grouped tiered traits `aura_realm_*` (auto mutually exclusive) | `common/traits/00_aura_realms.txt`                 | stub        |
| **Advancing a realm**         | `aura_advance_realm_effect` + `aura_can_advance_realm_trigger` | `common/scripted_effects`, `common/scripted_triggers` | stub     |
| **Core: Power**               | Variable `aura_power`; feeds Prowess & clash attack            | script values + traits                             | stub        |
| **Core: Agility**             | Variable `aura_agility`; clash initiative                      | script values                                      | stub        |
| **Core: Fortitude**          | Variable `aura_fortitude`; health & clash defense              | script values + traits                             | stub        |
| **Core: Soul**               | Variable `aura_soul`; stress/dread resistance & clash tempo    | script values                                      | stub        |
| **8 Elements (master 2)**     | Non-exclusive traits `aura_element_*`, capped by trigger       | `common/traits/01_aura_elements.txt`               | stub        |
| **5 Martial arts styles**     | Traits `aura_style_*`                                          | `common/traits/02_aura_styles.txt`                 | stub        |
| **Aura color**                | Derived from mastered elements (variable / cosmetic)           | future GUI + script value                          | planned     |
| **Techniques (passive/slotted)**| Modifiers + "equipped" variables / perks                     | `common/modifiers` (future)                        | planned     |
| **Aura Clash (combat check)** | Character interaction + resolution event chain                | `common/character_interactions`, `events`          | stub        |
| **Sects (Archonate, etc.)**   | Decisions + membership variable + court-role analog            | future                                             | planned     |
| **Heavenly Ascension Trials** | End-game realm (`aura_realm_ascendant`) event chain           | `events` (future)                                  | planned     |
| **Difficulty (Jade Dragon / Mortal Limits)** | Game rule scaling Chi gain                      | `common/game_rules` (future)                       | planned     |

## Variable & trait naming conventions

- **Prefix everything `aura_`** to avoid collisions with the base game and other
  mods.
- Character variables: `aura_chi`, `aura_power`, `aura_agility`,
  `aura_fortitude`, `aura_soul`, `aura_initialized`.
- Traits: `aura_realm_*` (grouped, `group = aura_realm`), `aura_element_*`,
  `aura_style_*`.
- Scripted effects end in `_effect`, scripted triggers end in `_trigger`,
  script values are nouns (`aura_chi_to_advance_value`).
- Event namespace: `aura_kings` (e.g. `aura_kings.0001`).
- Localization keys mirror the object key (trait `aura_realm_initiate` →
  loc key `aura_realm_initiate` + `aura_realm_initiate_desc`).

Keep this table in sync as mechanics move from `planned` → `stub` → `done`.
