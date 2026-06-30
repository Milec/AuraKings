# Leveled & multi-track traits (verified from vanilla)

The bundled `wiki_pages/Trait_modding.md` documents trait *categories* and flags
but **not** the leveled-trait (`track` / `tracks`) machinery, and the live
Paradox wiki is often Cloudflare-blocked. This page fills that gap with syntax
**verified against vanilla 1.19 files** (read from a public mirror —
`Warcraft-GoA-Development-Team/Warcraft-Guardians-of-Azeroth-2`, which carries
copies of vanilla `lifestyle_hunter`, `lifestyle_blademaster`, etc.).

> When the wiki is missing or blocked, the authoritative source is vanilla:
> `game/common/traits/00_traits.txt` and `…/00_lifestyle_traits.txt`. A quick way
> to read one without a local install is GitHub code search for a known trait id
> (e.g. `tourney_participant tracks`) and fetch the raw file.

## Key facts

- A leveled trait is `category = lifestyle`.
- **Base modifiers** in the trait body apply at level 0 (always on).
- A **single-track** trait uses `track = { <xp> = { <modifiers> } ... }`.
- A **multi-track** trait uses `tracks = { <trackname> = { <xp> = { <modifiers> } ... } ... }`.
  The overall trait level is the sum of the track levels.
- The numeric keys are **XP thresholds**; reaching that XP grants that level.
- **Track-level modifiers STACK cumulatively**: a character gets the base
  modifiers PLUS every reached level's modifiers. (Verified: vanilla blademaster
  is base `prowess = 3`, `50 = { prowess = 3 }`, `100 = { prowess = 6 }` → the
  documented totals of **+3 / +6 / +12**.) So each level block is the *increment*.
- Grant XP: `add_trait_xp = { trait = <trait> track = <track> value = <n> }`
  (omit `track` for single-track traits).
- Read level: `has_trait_xp = { trait = <trait> track = <track> value >= <n> }`
  (omit `track` for single-track; in `value=` trigger strings the form is
  `has_trait_xp(<trait>|<track>)`).
- Add the trait first with `add_trait`, then `add_trait_xp` (a `lifestyle`
  category trait can be granted and XP'd entirely from script).
- Dynamic `name`/`desc` per level via `first_valid` + `triggered_desc` whose
  trigger is `has_trait_xp` (see the reveler example below).

## Verified example — single-track (vanilla blademaster, trimmed)

```paradox
lifestyle_blademaster = {
    category = lifestyle
    icon = blademaster.dds

    negate_health_penalty_add = 0.25   # base (level 0)
    prowess = 3

    track = {
        50  = { negate_health_penalty_add = 0.25  prowess = 3 }   # -> total prowess 6
        100 = { negate_health_penalty_add = 0.5   prowess = 6 }   # -> total prowess 12
    }
}
```

## Verified example — multi-track (vanilla lifestyle_hunter, trimmed)

```paradox
lifestyle_hunter = {
    category = lifestyle
    icon = hunter.dds
    prowess = 1                # base
    stress_loss_mult = 0.05

    tracks = {
        hunter = {
            50  = { prowess = 1  health = 0.05  learning = 1 }
            100 = { prowess = 2  health = 0.15  learning = 1 }
        }
        falconer = {
            50  = { stewardship = 1  learning = 1  monthly_prestige = 0.25 }
            100 = { ... }
        }
    }
}
```

## Dynamic level name/desc (vanilla reveler pattern)

```paradox
name = {
    first_valid = {
        triggered_desc = {
            trigger = { exists = this  has_trait_xp = { trait = lifestyle_reveler  value >= 100 } }
            desc = trait_reveler_3
        }
        triggered_desc = {
            trigger = { exists = this  has_trait_xp = { trait = lifestyle_reveler  value >= 50 } }
            desc = trait_reveler_2
        }
        desc = trait_reveler_1
    }
}
```

## How Aura Kings uses this

`aura_martial_artist` and `aura_cultivator` are multi-track traits whose four
tracks are the cores (`power`/`fortitude`/`agility`/`soul`). A core is **100
track XP** (the XP scale equals Aura Pressure: 100 AP condensed = 1 immortal
core). Cultivator realm tiers sit at 100/1000/3000/7500/15000 XP (= 1/10/30/75/150
cores). Forging/condensing a core calls `add_trait_xp ... value = 100`; the
"50-Fortitude-cores → ageless" check is `has_trait_xp = { trait = aura_cultivator
track = fortitude value >= 5000 }`. Passive benefits are the track-level
modifiers themselves (no recalculation effect needed).

## Caveats to verify in-game (`-debug_mode` `error.log`)

- Whether a track needs explicit display localization (track label keys); if
  missing, the UI may show raw keys (non-fatal).
- Exact behavior of `has_trait_xp` inside `limit`/`trigger` blocks vs the
  `value=`-string form.
