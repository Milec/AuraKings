# Aura Clash — Source Mechanics & Lore Reference

A distilled reference for the **Aura Clash** interactive-fiction game, derived from
the game's source (`auraclash.html`, a SugarCube/Twine 2 story, ~3,065 passages,
~8.5M chars). This exists so the mod can be designed faithfully **without
re-reading the 10 MB HTML each time**. Variable names from the source are kept
(in `code`) because they are the most precise description of each mechanic and
map cleanly onto CK3 script.

> The source HTML is **not committed** to this repo (size + copyright). It lives
> outside the repo as reference only; we translate mechanics, not ship its text.
> Canonical mechanics live in the `menu-*` (stats/cultivation) passages and the
> SugarCube `<<widget>>` definitions.

---

## 1. Premise & tone

High-fantasy Eastern **martial-arts cultivation** (wuxia / xianxia). The player
starts as a near-powerless youth and rises by absorbing the world's natural
energy (**chi**) and refining it into a personal **Aura**, growing in raw power,
mastering elements and a martial style, learning techniques, joining sects, and
winning duels and trials up to **Immortality / Heavenly Ascension**.

The world is divided into five great martial nations, each with a signature
style, color, and chi-flavor (see §6). There are also sects, clans, spirit
beasts, demonic Gates, and assorted races.

---

## 2. The two resources (do not conflate)

These are different things and the mod must keep them distinct:

| Game term | Variable(s) | What it is |
|---|---|---|
| **Aura Pressure (AP)** | `$aurapressure`, `$allocatedap` | The **cultivation meter** — total spiritual capacity earned over a lifetime. The long-term progression currency. |
| **Chi** | `$chipool`, `$chispent`, `$maxchi` | **Combat stamina** spent during fights to power attacks. Refills between fights. |

- **AP** starts at `0`; `$allocatedap` starts at `100`.
  - **Free/unspent AP** = `$aurapressure - $allocatedap` (`$freeap`). This is what
    you spend to permanently grow.
  - "Allocating" AP locks it into a core permanently (it raises `$allocatedap`).
- **Chi**: `maxchi = $chipool + floor($soul / 2)`. Spending a core in combat is
  "spending chi" (see §5). Combat shows chi as filled/empty pips `●`/`○`.

You gain **AP** from: winning combat checks (`<<apboost N>>`), story choices,
and **Shard Cycling** (dissolving `$shards` into raw AP via `menu-cultivation-cycle`).

**AP cap (author clarification):** Aura Pressure tops out around **20,000**, a
figure that is *extremely rare and nigh unobtainable*. At 100 AP per immortal
core (see §3) that is the ceiling on cultivation, and the mod should treat ~20k
as the practical maximum when scaling benefits.

---

## 3. The four Combat Cores

The heart of the power system. Cores exist in **four stats**, and there are **two
kinds of core** within each stat — *mortal* and *immortal*. The `$power`,
`$fortitude`, `$agility`, `$soul` variables hold the **combined** core rating
(mortal + immortal) used in checks; all start at `1`.

| Core | Var | Combat role |
|---|---|---|
| **Power** | `$power` | Raw offense / striking |
| **Fortitude** | `$fortitude` | Toughness; raises max health |
| **Agility** | `$agility` | Speed / finesse / precision |
| **Soul** | `$soul` | Willpower / energy; raises max chi |

### Mortal cores vs Immortal cores (important — author clarification)

These are two distinct tiers of core, not in the raw source variables but
central to the lore/system:

- **Mortal cores** — gained through ordinary **physical training**. A *mortal*
  (someone who has **not** begun cultivation) can earn these; no Aura Pressure
  required.
  - There are at most **8 mortal cores total**, distributed across the four
    stats.
  - Everyone **starts with 1 in each stat** (4 spent), leaving **4 free** mortal
    cores to place wherever the character trains (e.g. 3 Power / 1 Agility, or
    spread evenly, etc.). This is the baseline `start at 1` seen in the source.
- **Immortal cores** — gained by **condensing Aura Pressure into a core**. This
  is true cultivation: the technique must be **learned/figured out** before a
  martial artist can do it at all. These are the **Immortal Core Advancements**
  the source spends AP on (below), stacked on top of the mortal cores in the
  same four stats.
- **Awakening immortal cores** (forming your *first* immortal core) also grants a
  **Foundation** — one you have either **inherited** or **trained up** to be
  ready for (see §10).
- **Order:** mortal cores do **not** all have to be filled before forming an
  immortal core — but maxing your 8 mortal cores first is the **usual/optimal
  route**, since it builds the body before condensing aura.
- **Equal value:** an immortal core counts exactly the **same as a mortal core**
  toward a stat's effective rating — immortal cores are simply how you push a
  stat past the 8-mortal-core ceiling, not a stronger kind of core.

**Core economy & ceiling (author clarification):**
- Each immortal core costs a flat **100 free AP** to condense. With the ~20,000
  AP cap (§2), that is **~200 immortal cores** maximum.
- Plus the **8 mortal cores** → a practical ceiling of **~208 cores total** per
  character (spread across the four stats however the player builds). Rare,
  non-AP ways to gain extra cores exist, but 208 is the number to scale against.
- **Power scaling / "leaving humanity":** a high cultivator is *no longer in the
  realm of humans.* An **Archon** (~**10,000 AP**, ~100 immortal cores) can live
  for **centuries** and slay **massive spirit beasts**. Benefits should ramp so
  that this tier feels flatly superhuman, with ~208 cores as the demigod ceiling.

> Modeling note: keep a per-stat split — `mortal_<stat>` (0–8 across stats,
> trainable by anyone) and `immortal_<stat>` (AP-condensed, gated behind
> awakening) — and present the sum (equally weighted) as the effective core
> rating.

Supporting per-core variables:
- `$powspent / $forspent / $agispent / $solspent` — chi of that core spent (in-combat).
- `$powexp / $forexp / $agiexp / $solexp` — **Advancement progress** toward the
  next +1 (0→100). Each combat check using a core grants `+1` exp.
- `$powsurge / …` — **Surge** value (starts `1`): how far *above* your raw core
  rating a check can still be passed by spending chi (see §5).
- `$powdiscount / …` — situational cost reductions.

### Immortal Core Advancement (permanent core growth)
Defined in `menu-cultivation-core` / `ch2-immortalcorecheck`:
- Advancing a core by **+1** costs **`100 - <core>exp` free AP** (i.e. accrued exp
  acts as a discount; a core with `powexp = 40` costs `60` AP).
- On advance: `$allocatedap += (100 - exp)`, that core's exp resets to 0, and the
  core rating `+1`.
- Story milestones call dramatic versions of this an **"Immortal Core
  Advancement"** (e.g. the 1st and 2nd Advancements are major plot beats; a
  high-stakes one in ch8 sacrifices and recycles your whole aura).

> **Derived stats:** `maxchi = chipool + floor(soul/2)`,
> `maxhealth = health + floor(fortitude/2)`. `$wounds` subtract from current health.

---

## 4. Ranks (universal 0–5 ladder)

Elements and Styles use a shared rank ladder (`$element1rank`, `$stylerank`, …):

| Value | Label |
|---|---|
| 0 | Untrained / None |
| 1 | Novice |
| 2 | Adept |
| 3 | Expert |
| 4 | Master |
| 5+ | Sage |

---

## 5. Combat — the "Aura Clash" check (the signature system)

Combat is resolved by the `<<combatcheck DIFFICULTY>>` widget. A check picks a
core (`$combatstat`, optionally a second `$combatstat2`), optionally adds a skill
(`$combatskill`) and a temporary modifier (`$cmod`), and compares against a
difficulty number:

1. **Free pass:** if `core (+ skill) + cmod >= difficulty` → **Passed**, no cost.
2. **Spend chi to reach it:** if the shortfall is within your **Surge** range
   *and* you have enough unspent core chi to cover the gap, you spend
   `difficulty - (core + skill + cmod)` chi of that core → **Passed**
   ("N Cores Spent"). This is the "burn your aura to win" fantasy.
3. **Fail:** not enough reach or not enough chi → **Failed**.

Other facts:
- Every check grants **`+1` exp** to the core used (feeds §3 Advancement).
- **Weapons** can substitute a quality bonus for the skill term
  (`$weaponbonus`, `$weaponbonus2`, dual-wield supported).
- **Mortal Limits** difficulty mode randomizes the difficulty *upward*
  (`<<rand diff diff diff+1>>`) — checks get harder.
- `<<woundcheck>>` / `<<deathcheck>>` handle taking damage and dying;
  `$guardtech` provides "Guard Points" that absorb hits.
- `<<replenish>>` / `<<spendall>>` reset or dump chi between encounters.
- `<<statcheck>>` prints the combat status block (health/chi/cores).

---

## 6. The five Styles (martial nations)

`$style` (default `"Freestyle"`), ranked by `$stylerank` (0–5). Each maps to a
nation, an aura color / chi-flavor, and synergy conditions (`$elementalsync` in
the `apboost` widget scales `0.01–0.025 × rank` based on race/morality/skills):

| Style | Nation | Chi flavor / color | Synergy hook (examples) |
|---|---|---|---|
| **Akakiru** | Aka (Red) | "Bladed Chi" — scarlet | Humans / `honor ≥ 70` |
| **Aoyusumu** | Aoyu (Blue) | "Sacred Chi" — cerulean | Saintly (`ruthless ≤ 30`) or Fallen Saint |
| **Kiihakai** | Kii (Yellow) | "Mystic Chi" — gold | High `lore + handseals` (sorcery) |
| **Kurokonton** | Kuro (Black) | "Cursed Chi" — purple | High `stealth` |
| **Midorikatai** | Mido (Green) | "Wild Chi" — green | Yokai / muscular bodytypes |

Plus **Freestyle** (untrained baseline). Style can be swapped
(`menu-cultivation-styleswapper`).

---

## 7. The eight Elements

Two primary slots: `$element1` (+`$element1rank`) and `$element2`
(+`$element2rank`); a rare third (`$element3`, "Yin Weaving") via special
training. Per-element rank vars also exist (`$firerank`, `$icerank`, …). You
normally **master up to two**. Each element has a signature aura color and
sync/affinity conditions (e.g. Darkness, Ice, Water, Earth, Fire give strong
`$elementalsync`):

| Element | Aura color | Aura-mix adjective |
|---|---|---|
| Fire | red | burning |
| Water | blue | swirling |
| Earth | amber | dense |
| Wind | emerald | howling |
| Storm | violet | crackling |
| Ice | arctic blue | misty |
| Light | yellow | shining |
| Darkness | black | dark |

Elements are learned at places like the **Temple** (`ch3-temple-element-*`),
the mountain/storm/woods sites, and the water-elemental path.

### Aura color (`$auracolor`, default "grey-white")
Cosmetic identity derived from your dominant element and/or style; can be
**mixed** (`menu-cultivation-auramix`) to e.g. "burning scarlet". Kitsune unlock
pink "Foxfire" at `≥2 tails`.

---

## 8. Skills (12, rated 0–5)

`$alchemy $athletics $craft $deception $handseals $insight $lore $perception
$persuasion $stealth $survival $thievery`. Skills can be added to combat checks
(`$combatskill`) and gate many story options. `Handseals` and `Lore` specifically
feed sorcerous (Kiihakai) power; `Stealth` feeds Kurokonton; etc.

---

## 9. Techniques

A slotted ability system (`menu-cultivation-techs`, `menu-cultivation-techdisplay`):
- **Known techniques:** `$knowntechname` / `$knowntechcode`.
- **Equipped slots:** `$techslotname[1..4]` / `$techslotcode[1..4]` — up to **4**
  active techniques; codes are packed digit-fields read via `dig(code, n)`
  (encoding attack type, element/style scaling, etc.).
- **Attack types** (`$stylement`): *Melee*, *Energy Melee*, *Ranged*; techniques
  scale off an element (`attack-elemcheck`) or off style rank (`attack-stylerun`).
- **Core Surging:** spend to temporarily boost a core's surge in a fight.
- **Transformations:** e.g. *Asura* (four-armed flurry, `+stylerank` prowess),
  *Soul Domain* (`$souldomain`).
- Sect-specific tech trees: `ch4-{aka,aoyu,kii,kuro,mido}-techs`.
- **Handseals** (`menu-cultivation-handseals*`) — a casting/combo subsystem.
- **Soul Treasure** (`menu-cultivation-soultreasure`) — a signature artifact/power.

---

## 10. Foundations

The **Foundation** (`$foundation`) is the defining basis of your **awakened
immortal cultivation**. A character gains a Foundation **when they awaken their
immortal cores** (form their first immortal core, §3) — it is something the
character has either **inherited** or **trained themselves up to be ready for**.
It anchors which path their condensed aura will follow.

In the source, the Foundation is *selected* late (around chapter 9.9,
`ch9-afternake5-pickfoundation`) as an alchemically-stabilized "path" keyed to
your element, granting a permanent **+1 core** and **element mastery**, plus
path-specific boons — but conceptually it represents the awakening of immortal
cultivation, not just a late-game pick. Example sets (each tied to your chosen
element):

- Burning Red (Fire): `+1 Power` or `+1 Soul`, +Fire Mastery
- Crackling Violet (Storm): `+1 Agility`/`+1 Soul`, +Storm Mastery
- Dark Black (Darkness): `+1 Fortitude`/`+1 Agility`, +Darkness Mastery
- Dense Amber (Earth): `+1 Fortitude`/`+1 Power`, +Earth Mastery
- Howling Emerald (Wind): `+1 Agility`/`+1 Power`, +Wind Mastery
- Misty Arctic Blue (Ice): `+1 Fortitude`/`+1 Soul`, +Ice Mastery
- Shining Yellow (Light): `+1 Soul`/`+1 Agility`, +Light Mastery
- Swirling Dark Blue (Water): `+1 Fortitude`/`+1 Power`, +Water Mastery
- Enchanting Pink (Kitsune): Soul/Agility + a Surge + Deception/Persuasion
- Bloody Crimson (corrupted): +core, +1 Chi, +500 Inner Hellscape Capacity
- Resolute Grey (elementless): `+1 Health`, `+1 Chi`

A full Foundation is **two parts**, combined into its name
(`$foundation = yangftxt1 + yangftxt2`):

1. **Elemental color base** (above) — the core boost + element mastery (or the
   Fox / Bloody / Resolute special bases). Becomes an adjective: *Burning*,
   *Crackling*, *Dark*, *Dense*, *Howling*, *Misty*, *Shining*, *Swirling*,
   *Enchanting*, *Bloody*, *Resolute*.
2. **Zodiac animal symbol** (`pickfoundation2`/`3`) — one of **twelve**: Boar
   (+Survival), Crane (+Perception), Dragon (+Handseals), Monkey (+Thievery), Ox
   (+Craft), Rabbit (+Alchemy), Ram (+Lore), Rat (+Stealth), Serpent (+Deception),
   Stallion (+Athletics), Tiger (+Persuasion), Wolf (+Insight). Matching your
   subrace grants a second skill. The skills here are *Aura Clash* skills (§8).

So a Foundation reads like **"Swirling Wolf"** or **"Burning Tiger."** Above all,
any Foundation grants **stability**: a cultivator with one never has their cores
break or their Advancement bottleneck — "good all the way to Ascension."

> **Mod note:** Aura Kings implements the **12 Zodiac animals** as the Foundation
> traits (`aura_foundation_*`), each mapped to a distinct CK3 benefit, chosen or
> inherited at awakening. The elemental color-base layer (core lean + element
> mastery) will be added when the element system exists.

---

## 11. Races

Chosen at creation (`ch1-raceselect`):
- **Human** — most common; synergizes with Akakiru / honor.
- **Oni** — red-skinned demon-descendants; affinity for Fire/Ice, ruthlessness.
- **Yokai** — animals who "Advanced" into human form; subrace **Kitsune**
  (`$tails`, Foxfire); synergizes with Midorikatai.
- **Lunargoth** — pale, round-eyed humans.
- (**Water Elemental** is a distinct elemental path, `ch1-waterelemental*`.)
`$subrace`, `$bodytype`, `$clan`, `$patriarch` further specialize a character.
Yokai gain a **Spirit Brand** (`ch6-spiritbrand*`) — cosmetic/power markings.

---

## 12. Morality axes

Two independent 0–100 scales (shown as opposed bars on the stats screen):
- **Honor** ↔ Dishonor (`$honor`; dishonor = `100 - honor`).
- **Compassion** ↔ **Ruthlessness** (`$ruthless`).

These gate style synergy (e.g. Aoyusumu rewards low ruthlessness; Akakiru rewards
high honor) and many story branches.

---

## 13. Demonic Corruption

A shadow progression for characters who touch Demonic Gates:
- **Inner Hellscape Capacity** (`$hellscape`, in "Demonic AP") — your capacity to
  hold demonic power.
- **Corruption / Taint** (`$taint`) — how corrupted you are.
- Corruption is **Hidden** while `hellscape > taint`, otherwise **Exposed**.
- Demonic Gates are boss encounters (`ch5-bossfight-darkgate/demongate`).

---

## 14. Social / "realm" layer (clans, sects, connections)

Beyond personal power there's a political layer — the natural bridge to CK3:
- **Clan status** (shown ch5.7+): `$prestige`, `$infamy`, `$commerce`,
  Retainer Strength (`$retainer_strength + $martial_retainers`),
  `$retainer_morale`, `$shipcount`, civilian/martial retainers.
- **Sects:** per-nation orgs each with a reputation value (`$sect_*`, ~0–100) and
  **Boon Writs** (`$boon_*`) you spend to call favors. Examples: Thousand
  Lantern, Haunted Fist, Four Clover, Choral Line, Devanic, Waverunner,
  Thunderfall, Dream River, Hidden Coil, New Dawn (Light), Wind Rising, etc.
- **Connections:** many named NPCs each tracked with `*combat`, `*romance`,
  `*rep` (best friend `$bff*`, siblings, mentors like Zhao Yang / Kaito / Eldra,
  rivals, companions). A "Best Friend" and family are central.

### Currencies
`$silver`, `$gold` (money), `$shards` (cultivation fuel → AP via cycling),
`$prestige` (clan standing).

---

## 15. Difficulty modes

- **Jade Dragon Foundation** (`$jadedragonfoundation`, default false) — easy /
  "reincarnation" mode (a powerful head-start, shown as a Reincarnation line).
- **Mortal Limits** (`$mortallimits`, default false) — hard mode: AP gains are
  routed through `<<apboost>>` (reduced) and combat difficulty is randomized
  upward.
- Default is neither.

---

## 16. Trials & end-game (heavy narrative content)

- **Heavenly Ascension Trials** / Rin Trial (`$rintrial`, `ch2-trialannouncement*`).
- **Sibling / Tiger / Rabbit / Dragon trials** (ch8 `*-siblingtrial-*`,
  `ch8-tigertrial*`, `ch8-rabbit-*`, `ch8dragon-*`).
- **Meditation** (`ch3-meditate*`, `menu-cultivation`), **Spirit Beast hunts**
  (roc, drake, "spirit of the well"), **Rune/Seal rituals** (`$runesealritual`).
- A **Trial Chart** (`<<trialchart>>`) tracks standings from ch8.

---

## 17. Story spine (chapter map)

Chapters drive `$chapter` (fractional sub-steps like 1.4, 8.9, 9.9 gate features):
1. **Ch1** — birth, race, clan, starting style (character creation).
2. **Ch2** — first conflict, first **Advancement**, immortality milestone, trial announcement.
3. **Ch3** — learn **Elements** (Temple/mountain/storm/woods), library/styles, meditation.
4. **Ch4** — sect **Technique** trees.
5. **Ch5** — Demonic **Gate** boss fights.
6. **Ch6** — **Spirit Brand** (Yokai).
7. **Ch7** — the **Daichi** duel (large branching fight).
8. **Ch8** — **Sibling / Tiger / Dragon trials**, big aura sacrifices.
9. **Ch9** — **Foundation** choice, teaching others, late-game cultivation.

---

## 18. Glossary of key source variables (for CK3 mapping)

| Variable | Meaning |
|---|---|
| `$aurapressure` / `$allocatedap` / `$freeap` | total / locked / spendable cultivation meter |
| `$chipool` / `$chispent` / `$maxchi` | combat chi pool / spent / max (`chipool+floor(soul/2)`) |
| `$power $fortitude $agility $soul` | the four cores (start 1) |
| `$powexp …` | core Advancement progress (0→100) |
| `$powsurge …` | surge reach (start 1) |
| `$powspent …` | core chi spent in combat |
| `$health` / `$maxhealth` / `$wounds` | base health / max (`health+floor(fortitude/2)`) / damage |
| `$style` / `$stylerank` | martial style and its 0–5 rank |
| `$element1/2/3` / `$elementNrank` | mastered elements and their ranks |
| `$auracolor` | cosmetic aura color (element+style) |
| `$foundation` | Foundation — path gained on immortal-core awakening |
| `$knowntech* / $techslot*` | known and equipped (max 4) techniques |
| `$handseals $lore $stealth …` | skills (0–5) |
| `$honor $ruthless` | morality axes (0–100) |
| `$hellscape $taint` | demonic capacity / corruption |
| `$prestige $infamy $commerce $retainer_* $shipcount` | clan/realm standing |
| `$silver $gold $shards` | currencies |
| `$sect_* $boon_*` | sect reputations / favor writs |
| `$jadedragonfoundation $mortallimits` | difficulty flags |
| `$race $subrace $clan $patriarch $bodytype` | identity |
| `$chapter` | story progress gate |

---

## 19. Implications for the CK3 mod (quick notes)

- **Aura Pressure ≠ Chi.** Model AP as the long-term cultivation track (XP-style),
  and Chi as a short-term combat/stamina pool. *(Done: the scaffold now tracks
  `aura_pressure_total` + `aura_pressure_free`; a separate Chi combat pool is
  still to be added.)*
- **Two core tiers per stat.** Model **mortal cores** (trainable by anyone,
  capped at 8 total across the four stats, 1 each at start) separately from
  **immortal cores** (AP-condensed, gated behind awakening). This gives a clean
  CK3 distinction: *anyone* (even non-cultivator rulers) can be a trained
  warrior via mortal cores, while immortal cores require awakening — a natural
  "mortal vs cultivator" divide that fits CK3's character roster.
- **Cores as growable stats** with an XP-to-advance curve (100-exp cost) map
  naturally to CK3 tracked traits / script values.
- **Combat checks** (pick a core, optionally spend chi up to surge to pass a
  difficulty) are the template for the **Aura Clash** interaction resolution.
- **Realms** in *Aura Clash* are not a fixed named ladder — progression is the
  Core/AP/Advancement loop plus milestone "Advancements" (and Immortality). The
  scaffold's fixed realm-trait ladder is a reasonable CK3 abstraction but should
  be re-anchored to AP/Advancements, with **Immortal-core awakening + a
  Foundation** as the pivotal "becoming a cultivator" step.
- **Styles (5)** and **Elements (8, pick 2)** already align with the scaffold's
  trait stubs — keep, and add the rank ladder (Novice→Sage) and synergy hooks.
- The **sect / clan / connection** layer is the obvious hook into CK3's native
  vassal/faction/relation systems.
