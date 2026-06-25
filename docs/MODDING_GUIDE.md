# Aura Kings — Modding Guide & Conventions

Read this before contributing. CK3 scripting is unforgiving about a few things
(encoding, load order, namespaces); these conventions keep the mod loadable.

## Repository = mod root

The repository root **is** the mod folder. `descriptor.mod` lives here and the
folder layout matches what CK3 expects (`common/`, `events/`, `localization/`,
`gui/`, `gfx/`). Don't nest the mod inside a subfolder.

## Load order & file naming

CK3 loads files in a folder alphabetically and later definitions override earlier
ones. We prefix files with a two-digit number to make order explicit, e.g.
`00_aura_core_traits.txt`, `01_aura_elements.txt`. New data files should follow the
same `NN_aura_<topic>.txt` pattern.

## Namespacing

- Every key we define is prefixed `aura_` (traits, effects, triggers, script
  values, decisions, interactions, variables).
- Events use the `aura_kings` namespace and are declared once at the top of each
  event file: `namespace = aura_kings`.
- This prevents collisions with vanilla and other mods.

## Localization (IMPORTANT: BOM)

- Loc files live in `localization/english/` and **must be UTF-8 *with* BOM**.
  CK3 silently fails to read loc files saved as UTF-8 without a BOM.
- File header is `l_english:` on the first line (after the BOM).
- Entries use a version number: `my_key:0 "My text"`.
- `.gitattributes` is configured to preserve the BOM; don't "fix" it away.
- Every defined trait/decision/interaction/event needs matching loc keys, or the
  game shows raw key names.

## Where things go

| Content                        | Folder                              |
|--------------------------------|-------------------------------------|
| Traits                         | `common/traits/`                    |
| Scripted effects               | `common/scripted_effects/`          |
| Scripted triggers              | `common/scripted_triggers/`         |
| Script values (computed nums)  | `common/script_values/`             |
| Decisions                      | `common/decisions/`                 |
| Character interactions         | `common/character_interactions/`    |
| On-actions (hooks)             | `common/on_action/`                 |
| Events                         | `events/`                           |
| Text                           | `localization/english/`             |

## Testing changes

CK3 has no unit-test harness. Validate by:

1. Loading the mod in CK3 with `-debug_mode` enabled (launch option / Steam).
2. Watching `error.log` in the Paradox user `logs/` folder for parse errors —
   this is the single most important check; a clean `error.log` means the mod
   parsed.
3. Using the in-game console (`` ` ``) to test effects, e.g.
   `effect = { aura_begin_martial_training_effect = yes }`,
   `effect = { aura_gain_pressure_effect = { AMOUNT = 200 } }`, `add_trait aura_cultivator`.

A PR should leave `error.log` free of new errors introduced by the change.

## Style

- Tabs for indentation (matches vanilla CK3 scripts).
- One definition per concept; comment non-obvious numbers with intent.
- Prefer reusing `aura_*` scripted effects/triggers over copy-pasting logic.
