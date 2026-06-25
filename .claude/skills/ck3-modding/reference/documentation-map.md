# CK3 Documentation Map

Complete index of the bundled wiki (`wiki_pages/`, paths relative to the
ck3-modding-wiki repository root) grouped by what you're trying to do. Sizes
are a rough guide to whether to **read the page** (small/medium) or **`Grep`
it** (the large list pages). For full section anchors, see the repo-root
`TABLE_OF_CONTENTS.md`.

Legend: 📖 read in full · 🔎 grep for the keyword you need · ⚙️ skim relevant section

## Foundations (read early on any task)

| Page | Size | Use |
| --- | --- | --- |
| `Modding.md` | ~5.3k 📖 | Big-picture intro, launch options, **load order & override rules**, uploading, troubleshooting overview |
| `Mod_structure.md` | ~1.2k 📖 | `.mod` + descriptor files, folder layout, getting a mod recognized |
| `Scripting.md` | ~4k 📖 | The scripting language: syntax, scopes, chaining, prefixes, operators, saved scopes, `if`/`switch`/`while`, lists, iterators, scripted effects/triggers, script values |
| `Mod_troubleshooting.md` | ~1.7k 📖 | Debug mode, developer console, `error.log`/Error Dog, `script_docs`, scope debugging, hot-reload, run scripts |
| `Modding_tools.md` | ~0.8k 📖 | Community tooling table — **ck3-tiger** validator, CWTools, converters, etc. |

## The scripting core

| Page | Size | Use |
| --- | --- | --- |
| `Scopes.md` | ~2.8k ⚙️ | What scopes are, scope types, transitions, saved scopes, event targets |
| `Scopes_list.md` | ~2k 🔎 | Every scope transition and which scope it goes from→to |
| `Effects.md` | ~44k 🔎 | Conceptual guide to effects with categorized examples |
| `Effects_list.md` | ~42k 🔎 | Exhaustive alphabetical effect reference — **grep the effect name** |
| `Triggers.md` | ~2.4k ⚙️ | How conditions/`limit`/`trigger_if` work |
| `Triggers_list.md` | ~30k 🔎 | Exhaustive trigger reference — **grep the trigger name** |
| `Modifier_list.md` | ~5.4k 🔎 | All static modifiers (stats the game tracks) |
| `Scripted_effects.md` | ~0.2k 📖 | Reusable effect macros |
| `Variables.md` | ~0.9k 📖 | `set_variable`/`var:`/`global_var:`, variable lists |
| `Lists.md` | ~0.6k 📖 | Script lists/arrays, add/remove/iterate |
| `Weight_modifier.md` | ~0.5k 📖 | Weighted random / `ai_chance` / MTTH `modifier` blocks |
| `Data_types.md` | ~14k 🔎 | GUI data types, global promotes & functions (for interface + dynamic loc) — **grep the type/function** |

## Content systems

### Characters, dynasties, traits
| Page | Use |
| --- | --- |
| `Characters_modding.md` | Scripting/creating characters, appearance, outfit tags, calling characters from other scripts |
| `History_modding.md` | The `history/` static system: characters, titles, provinces over dates |
| `Dynasties_modding.md` | Dynasties, houses, dynasty legacies |
| `Trait_modding.md` | Creating/modifying traits, flags, tracks |

### Realm, rule, faith, culture
| Page | Use |
| --- | --- |
| `Governments_modding.md` | Government types |
| `Title_modding.md` | Titles, de jure/de facto, ranks, succession |
| `Council_modding.md` | Council positions and tasks |
| `Holdings_modding.md` | Holding types and buildings |
| `Culture_modding.md` | Culture groups, cultures, traditions, ethos, IDs |
| `Religions_modding.md` | Religions, faiths, doctrines, tenets |
| `Flavorization.md` | Culture/faith-specific title & name flavor |

### Interactive content
| Page | Use |
| --- | --- |
| `Event_modding.md` | Events, options, `immediate`, triggered events, on_actions, event chains, portraits |
| `Decisions_modding.md` | Major/minor decisions, `is_shown`/`is_valid`/`effect` |
| `Interactions_modding.md` | Character interactions |
| `Struggle_modding.md` | Struggle phases, catalysts, involvement |
| `Story_cycles_modding.md` | Story cycles (background scripted state machines) |
| `Artifact_modding.md` | Artifacts: templates, visuals, creation effects |
| `Regiments_modding.md` | Men-at-arms / regiment types |

### World & start
| Page | Use |
| --- | --- |
| `Map_modding.md` | Provinces, definition.csv, heightmap, rivers, terrain masks, adjacencies |
| `Terrain_modding.md` | Terrain types and assignment |
| `Bookmarks_modding.md` | Bookmarks, start dates, bookmark screen & portraits |

## Presentation layer

| Page | Use |
| --- | --- |
| `Localization.md` | YAML loc format, UTF-8 BOM, dynamic loc, data functions, custom loc, debugging loc |
| `Interface.md` | GUI system: widgets, templates, scripted GUIs, datacontext |
| `Coat_of_arms_modding.md` | CoA script keywords, inheritance, dynamic CoA, emblem `.dds` modding |
| `3D_models.md` | Modeling pipeline, Maya/Blender, textures, getting models on the map |
| `Exporters.md` | Paradox Clausewitz exporters |
| `Graphical_assets.md` | Asset formats overview |
| `Fonts.md` | Adding/replacing fonts |
| `Sound_modding.md` | Sound effects, fmod banks |
| `Music_modding.md` | Adding music |

## Tuning, compatibility, reference

| Page | Use |
| --- | --- |
| `Defines.md` | `common/defines` tunables (and how to override only what you need) |
| `Mod_compatibility.md` | Writing mods that coexist: additive content, single-object overrides, load order |
| `Console_commands.md` | Console/cheat commands for testing (`~5.5k 🔎`) |
| `Commands.md` | Command reference (`~8.4k 🔎`) |

## Lookup recipes

- **"Is there an effect/trigger for X?"** → `Grep "<keyword>" wiki_pages/Effects_list.md`
  or `wiki_pages/Triggers_list.md`. Try synonyms; names are verb-like
  (`add_`, `set_`, `remove_`, `change_`, `is_`, `has_`, `can_`).
- **"Which scopes can do this?"** → check the command's entry, then confirm the
  transition in `wiki_pages/Scopes_list.md`.
- **"What modifier raises stat Y?"** → `Grep "<stat>" wiki_pages/Modifier_list.md`.
- **"How do I test it?"** → `wiki_pages/Console_commands.md`; in-game `script_docs`
  dumps the authoritative list for the installed version.
- **"What does data function/promote Z return?"** → `Grep "Z" wiki_pages/Data_types.md`.
