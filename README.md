# Aura Kings

A **Crusader Kings 3** mod that brings the cultivation mechanics and power system
of the **Aura Clash** CYOA / interactive-fiction into the world of CK3.

In *Aura Clash*, powerless mortals rise above their station by absorbing **Chi**
from the world and refining it into a personal **Aura**. They cultivate four
cores — **Power, Agility, Fortitude, Soul** — master **elements** and **martial
arts styles**, learn **techniques**, join **sects**, and prove themselves in
ritual **Aura Clashes**. *Aura Kings* recreates that progression as a layer on
top of CK3's character and realm simulation: your rulers no longer just inherit
land, they cultivate power.

> **Status: Groundwork / pre-alpha.** This repository currently contains the
> mod scaffold — a loadable skeleton with the core data structures (Chi, realms,
> cores, elements, styles), foundational scripted logic, and the design docs
> that the rest of the mod will be built against. Numbers and content are
> placeholders meant to be iterated on.

## What's here

```
descriptor.mod          Mod descriptor read by CK3 (in-mod copy)
AuraKings.mod           Launcher descriptor (copy/symlink into Paradox mod/ folder)
common/                 Game-data scripts (traits, effects, triggers, decisions, ...)
events/                 Event scripts
gui/                    UI definitions (placeholder)
gfx/                    Art / interface assets (placeholder)
localization/english/   English text for everything defined in common/ & events/
docs/                   Design documentation and the Aura Clash -> CK3 mapping
```

See [`docs/DESIGN.md`](docs/DESIGN.md) for the design vision, and
[`docs/MECHANICS_MAPPING.md`](docs/MECHANICS_MAPPING.md) for how each Aura Clash
mechanic is represented in CK3 terms.

## Quick install (scripts)

If you just want to play it, clone or download this repo, then run the installer
for your OS — it registers the mod with the CK3 launcher (pointing at this folder,
so a later `git pull` updates it in place):

- **Windows:** double-click **`install.bat`**.
- **Linux / macOS:** run **`./install.sh`** (`chmod +x install.sh` first if needed;
  set `CK3_USER_DIR=...` to override a non-standard CK3 location).

Then open the CK3 launcher, add **Aura Kings** to a playset, enable it, and play.
There's no compiled `.exe` on purpose — a readable script you can inspect is safer
and won't trip antivirus.

## Installing for development

1. Locate your Paradox CK3 user directory:
   - Windows: `Documents/Paradox Interactive/Crusader Kings III/`
   - Linux: `~/.local/share/Paradox Interactive/Crusader Kings III/`
   - macOS: `~/Documents/Paradox Interactive/Crusader Kings III/`
2. Clone this repository somewhere convenient.
3. Copy `AuraKings.mod` into the `mod/` subfolder of the directory above and set
   its `path=` line to point at your clone (or, on Linux/macOS, symlink the clone
   into `mod/AuraKings` and leave the default path).
4. Launch CK3, enable **Aura Kings** in the launcher, and play.

`supported_version` in the descriptors is set to a recent CK3 build — update it to
match your installed game version if the launcher flags a mismatch.

## Contributing

Read [`docs/MODDING_GUIDE.md`](docs/MODDING_GUIDE.md) for conventions (file
naming, namespaces, localization-with-BOM rules) before opening a PR.

## Credits

*Aura Clash* is created by its respective authors; this is an unofficial,
non-commercial fan adaptation of its mechanics for Crusader Kings 3. Crusader
Kings III is a trademark of Paradox Interactive.
