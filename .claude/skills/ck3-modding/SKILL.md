---
name: ck3-modding
description: >-
  Expert assistance for creating, editing, debugging, and reviewing Crusader
  Kings 3 (CK3 / Crusader Kings III) mods. Use whenever the task involves CK3
  mod content — events, decisions, traits, cultures, religions, faiths,
  governments, titles, dynasties, men-at-arms/regiments, struggles, story
  cycles, activities, the map, the interface/GUI, localization, coats of arms,
  3D models, sound/music, or the Paradox/Jomini scripting language itself
  (scopes, effects, triggers, modifiers, scripted effects/triggers, script
  values, on_actions). Backed by the full official CK3 modding documentation
  bundled in this repository's `wiki_pages/` directory.
---

# CK3 Modding

You are helping build **high-quality Crusader Kings 3 mods**. This skill turns
the bundled official wiki (`wiki_pages/`, 51 reference pages) into a working
toolkit: a documentation router so you read the right page before writing
script, plus a workflow and quality bar that separate a "works on my machine"
mod from a polished, compatible, validated one.

## How to use this skill

The reference docs are **large** (the effects and triggers lists alone are
~75k words). Do **not** read them all. Instead:

1. **Identify the system** the task touches (event? trait? culture? map?).
2. **Open only the matching page(s)** from the routing table below. Read the
   full page for the system you are modding — these pages are self-contained
   tutorials with working examples.
3. **Look up exact API** (a specific effect, trigger, scope, or modifier) in
   the big list pages using `Grep` rather than reading them top to bottom.
4. **Apply the quality bar** in `reference/quality-checklist.md` before
   considering the work done.

> Paths like `wiki_pages/Event_modding.md` are relative to the
> **ck3-modding-wiki repository root**. Paths like
> `reference/quality-checklist.md` are relative to **this skill directory**
> (`.claude/skills/ck3-modding/`). When in doubt, locate the file with `Glob`.

## Documentation router (read before writing)

**Always-relevant foundations** — skim these for any non-trivial task:

| Need | Read |
| --- | --- |
| Where files go, `.mod`/descriptor, folder layout | `wiki_pages/Mod_structure.md` |
| Scripting language: syntax, scopes, chaining, prefixes, `if`/`while`, lists, scripted effects/triggers, script values | `wiki_pages/Scripting.md` |
| How scopes work + the scope transition list | `wiki_pages/Scopes.md`, `wiki_pages/Scopes_list.md` |
| Load order & override rules (full-file vs single-object) | `wiki_pages/Modding.md` |
| Debugging, error.log, `script_docs`, hot-reload | `wiki_pages/Mod_troubleshooting.md` |
| Validators & community tooling (ck3-tiger etc.) | `wiki_pages/Modding_tools.md` |

**API lookup pages** — `Grep` these for an exact keyword, don't read whole:

| Looking for | Grep in |
| --- | --- |
| An effect (does something: `add_gold`, `set_variable`) | `wiki_pages/Effects_list.md`, concepts in `wiki_pages/Effects.md` |
| A trigger (a condition: `is_ruler`, `gold >= 100`) | `wiki_pages/Triggers_list.md`, concepts in `wiki_pages/Triggers.md` |
| A modifier (`monthly_income`, `martial`) | `wiki_pages/Modifier_list.md` |
| A data type / GUI promote or function | `wiki_pages/Data_types.md` |
| A console/cheat command for testing | `wiki_pages/Console_commands.md`, `wiki_pages/Commands.md` |
| List/array builders & iterators | `wiki_pages/Lists.md`, `wiki_pages/Variables.md` |

**System-specific pages** — open the one(s) matching the feature:

| Building… | Read |
| --- | --- |
| Events, event chains, options, on_actions | `wiki_pages/Event_modding.md` |
| Decisions (major/minor) | `wiki_pages/Decisions_modding.md` |
| Character interactions | `wiki_pages/Interactions_modding.md` |
| Traits | `wiki_pages/Trait_modding.md` |
| **Leveled / multi-track traits** (lifestyle/blademaster-style: `track`/`tracks`, `add_trait_xp`, `has_trait_xp`) | `reference/leveled-traits.md` — **fills a gap the wiki page omits**, with verified vanilla examples |
| Characters / history / appearance | `wiki_pages/Characters_modding.md`, `wiki_pages/History_modding.md` |
| Dynasties & houses, dynasty legacies | `wiki_pages/Dynasties_modding.md` |
| Cultures, traditions, ethos | `wiki_pages/Culture_modding.md` |
| Religions & faiths, doctrines, tenets | `wiki_pages/Religions_modding.md` |
| Governments | `wiki_pages/Governments_modding.md` |
| Titles, de jure, succession | `wiki_pages/Title_modding.md` |
| Council positions & tasks | `wiki_pages/Council_modding.md` |
| Holdings & buildings | `wiki_pages/Holdings_modding.md` |
| Men-at-arms / regiments | `wiki_pages/Regiments_modding.md` |
| Struggles | `wiki_pages/Struggle_modding.md` |
| Story cycles | `wiki_pages/Story_cycles_modding.md` |
| Artifacts | `wiki_pages/Artifact_modding.md` |
| Bookmarks & start dates | `wiki_pages/Bookmarks_modding.md` |
| Flavorization (titles/names by culture) | `wiki_pages/Flavorization.md` |
| Map: provinces, terrain, heightmap, rivers | `wiki_pages/Map_modding.md`, `wiki_pages/Terrain_modding.md` |
| GUI / interface, scripted GUIs, widgets | `wiki_pages/Interface.md` |
| Coats of arms (script + emblems) | `wiki_pages/Coat_of_arms_modding.md` |
| 3D models, exporters, graphical assets | `wiki_pages/3D_models.md`, `wiki_pages/Exporters.md`, `wiki_pages/Graphical_assets.md` |
| Fonts | `wiki_pages/Fonts.md` |
| Sound / music | `wiki_pages/Sound_modding.md`, `wiki_pages/Music_modding.md` |
| Localization, dynamic loc, `[ ]` data functions | `wiki_pages/Localization.md` |
| `defines` tuning | `wiki_pages/Defines.md` |
| Making the mod compatible with others | `wiki_pages/Mod_compatibility.md` |

A complete task→page map (including section anchors) lives in
`reference/documentation-map.md`. `wiki_pages/TABLE_OF_CONTENTS.md` (at repo
root: `TABLE_OF_CONTENTS.md`) indexes every section of every page.

## Scripting essentials (so you don't repeat beginner mistakes)

These are the load-bearing rules; the full treatment is in
`wiki_pages/Scripting.md`.

- **Scopes are everything.** Script executes *in* a scope (usually a
  character, but also title, province, faith, etc.). An effect or trigger is
  only valid in the scopes it supports — using a faith trigger on a character
  scope is a classic error ck3-tiger catches. Change scope with transitions
  (`liege = { ... }`, `capital_province = { ... }`) and iterate with
  `every_`/`random_`/`ordered_` list iterators. Save a scope with
  `save_scope_as = name` and re-enter it with `scope:name`.
- **Prefixes matter:** `scope:`, `event_target:`, `root`, `this`, `prev`,
  `var:`, `global_var:`, `local_var:`. Know which one resolves what.
- **Effects vs triggers vs modifiers** are different namespaces. Effects
  *change* state (only in effect blocks), triggers *test* state (only in
  `limit`/`trigger`/condition blocks), modifiers are static stat changes.
  Don't put a trigger where an effect goes or vice-versa.
- **Reuse via** `scripted_effect`, `scripted_trigger`, and script values
  (`script_value`) instead of copy-pasting. Use `scripted_modifier` and
  `scripted_gui` where appropriate.
- **Weighted choice** (event options, AI, MTTH) uses `weight_modifier` /
  `ai_chance` blocks — see `wiki_pages/Weight_modifier.md`.
- **Formatting:** tabs for nesting, `#` comments, `{ }` blocks. Match the
  vanilla style of whatever folder you're editing.

## Build workflow

1. **Set up the mod skeleton** correctly first (`Mod_structure.md`): a
   `descriptor.mod`, a matching outer `.mod` file in the `mod/` directory,
   `version`/`supported_version`/`tags`/`path`, and mirror vanilla's folder
   layout (`common/`, `events/`, `gui/`, `localization/`, `history/`, etc.).
2. **Find the vanilla example.** The single best source of truth is the game's
   own files. Tell the user to look in their CK3 install (`game/common/...`)
   for an existing example of the thing they're adding, and mirror its
   structure. The wiki explains *why*; vanilla shows the current *how*.
3. **Write the script** in the right folder, reading the matching system page
   first. Keep IDs unique and namespaced to the mod (e.g. `mymod_` prefix) to
   avoid collisions.
4. **Localize everything.** Every key the game shows the player needs a
   `l_english` entry (and ideally other languages). Missing loc is the #1
   visible bug. See `wiki_pages/Localization.md`.
5. **Validate with ck3-tiger** (`wiki_pages/Modding_tools.md`) — it catches
   wrong-scope usage, typos, missing loc, and dangling references before you
   ever launch the game.
6. **Test in-game** with `-debug_mode` launch option: open console (`` ` ``),
   use `error.log` / Error Dog, `script_docs` to dump valid keywords, and
   hot-reload for fast iteration. See `wiki_pages/Mod_troubleshooting.md`.
7. **Make it compatible** (`wiki_pages/Mod_compatibility.md`): prefer adding
   *new* files and single-object overrides over full-file overrides of vanilla;
   the latter break on every patch and conflict with other mods.

## The "high tier" bar

Before declaring a mod feature done, check it against
`reference/quality-checklist.md`. The short version: it loads with **zero
ck3-tiger errors and a clean error.log**, everything visible is **localized**,
it uses **correct scopes**, it **doesn't needlessly override vanilla files**,
it has **icons/tooltips** where the UI expects them, and it **degrades
gracefully** (guarded with `exists`/`is_alive`/scope checks so it can't spam
errors). Aim for content that feels like it belongs in the base game.

## Important notes

- **Verify against the player's actual game version.** This wiki tracks the
  live game but specific effects/triggers can change between patches. When an
  exact keyword matters, cross-check the player's local `game/` files or the
  `script_docs` dump.
- This skill **navigates and applies** the docs; it does not replace reading
  the page for the system you're modding. When unsure, read the page.
- For deep API recall on the giant list pages, **`Grep` for the keyword** —
  e.g. `Grep "add_trait" wiki_pages/Effects_list.md` — rather than loading the
  whole file into context.
