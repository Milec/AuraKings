# High-Tier CK3 Mod Quality Checklist

Use this as the acceptance bar for any CK3 mod feature. A "high tier" mod is
indistinguishable in polish from base-game content: it loads clean, is fully
localized, scopes correctly, and plays nicely with other mods and future
patches.

## 1. Correctness

- [ ] **Right scope for every effect/trigger.** Each command runs in a scope
      that supports it (character / title / province / faith / culture / …).
      Wrong-scope usage is the most common error and ck3-tiger flags it.
      Cross-check in `wiki_pages/Scopes_list.md` and the per-command notes in
      `Effects_list.md` / `Triggers_list.md`.
- [ ] **Effects in effect blocks, triggers in trigger blocks.** Don't put a
      condition where a command belongs (or vice versa). `limit = { }`,
      `trigger = { }`, and `is_shown`/`is_valid` take triggers; the body of an
      event `immediate`/`option` takes effects.
- [ ] **Guarded against null/invalid state.** Before acting on a scope, confirm
      it exists and is valid: `exists = scope:target`, `is_alive = yes`,
      `is_landed`, etc. Unguarded access spams `error.log` and can break saves.
- [ ] **Unique, namespaced IDs.** Prefix every new key (events, decisions,
      traits, modifiers, scripted effects, on_action entries) with a short mod
      tag (`mymod_`). Reusing a vanilla ID silently overrides it.
- [ ] **References resolve.** Every trait/modifier/event/title/loc key you
      point at actually exists. ck3-tiger reports dangling references.

## 2. Localization

- [ ] **Every player-facing key has loc.** Names, descriptions, tooltips,
      option text, custom triggers/effects' tooltips — all need an entry in
      `localization/english/*.yml` (and other languages where possible).
- [ ] **Correct YAML loc format**: `l_english:` header, ` key:0 "text"` lines,
      UTF-8 **with BOM**. See `wiki_pages/Localization.md`.
- [ ] **Dynamic loc / data functions** (`[Character.GetName]`, `$VAR$`, scopes
      in brackets) resolve in the right scope and don't error.
- [ ] **No raw keys shown in game.** If the UI shows `mymod_trait_name` instead
      of a real name, the loc is missing or misnamed.

## 3. Compatibility & load order

- [ ] **Prefer additive content.** Add *new* files rather than overriding
      vanilla ones whenever possible.
- [ ] **Single-object override > full-file override.** For `defines`,
      `on_actions`, scripted GUIs, and other mergeable types, override only the
      object you need, not the whole file. Full-file overrides break on patches
      and conflict with other mods. See `wiki_pages/Mod_compatibility.md` and
      the override-rules section of `wiki_pages/Modding.md`.
- [ ] **on_actions are extended, not replaced.** Append your events to the
      relevant on_action via a single-object override; don't clobber vanilla's
      list.
- [ ] **No accidental vanilla overrides.** Check you haven't named a file or ID
      identically to a base-game one unless that override is intentional.

## 4. UX polish

- [ ] **Icons/textures present** where the UI expects them (traits, decisions,
      modifiers, etc.); no missing-texture placeholders.
- [ ] **Tooltips are informative** — custom effects/triggers expose readable
      `custom_tooltip` / `custom_description` instead of dumping raw script.
- [ ] **AI behaves sensibly** — decisions/interactions have reasonable
      `ai_will_do` / `ai_chance`; events have sane MTTH or trigger conditions so
      they neither never fire nor spam.
- [ ] **Balanced numbers** — costs, modifiers, and weights are in line with
      vanilla scale (sanity-check against `wiki_pages/Modifier_list.md` and
      vanilla values).

## 5. Validation & testing (the gate)

- [ ] **ck3-tiger run is clean** (no errors; warnings reviewed). This is
      non-negotiable for high-tier work. See `wiki_pages/Modding_tools.md`.
- [ ] **`error.log` is clean** after launching with `-debug_mode` and loading
      the mod. Open the console with `` ` `` and check Error Dog.
      (`wiki_pages/Mod_troubleshooting.md`)
- [ ] **Feature tested live** — fired the event / took the decision / applied
      the trait via console and confirmed it does what it should. Use
      `wiki_pages/Console_commands.md` for test commands; `script_docs` dumps
      the list of valid keywords for the installed version.
- [ ] **Hot-reload used for iteration, full restart for final verification** —
      hot-reloading can mask startup errors, so confirm a clean cold load.

## 6. Version safety

- [ ] **Checked against the installed game version.** Effects/triggers can be
      renamed or removed between patches. When an exact keyword matters, verify
      it exists in the player's local `game/` files or `script_docs` dump rather
      than trusting recall.
- [ ] **`supported_version` in the descriptor** matches the version you tested.

## Common pitfalls (recognize these fast)

| Symptom | Likely cause |
| --- | --- |
| Raw key text shown in UI | Missing/misnamed localization key |
| `error.log` flooded on load | Wrong-scope command, or unguarded scope access |
| Effect "does nothing" | It's a trigger used as an effect, or wrong scope |
| Mod breaks after a game patch | Full-file override of a vanilla file that changed |
| Conflicts with another mod | Both full-file-override the same vanilla file / ID |
| Event never fires | Failing trigger, zero MTTH weight, or not hooked to an on_action |
| Loc shows mojibake / blank | YAML not saved UTF-8 **with BOM**, or bad `key:0` syntax |
| Saved scope is empty later | Re-saved after hot-reload, or scope wasn't valid when saved |
