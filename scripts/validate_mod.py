#!/usr/bin/env python3
"""Offline sanity checker for the Aura Kings CK3 mod.

This is NOT a substitute for loading the mod in CK3 with -debug_mode (only that
catches vanilla-semantic errors). It runs fully offline with no game files and
catches the classes of mistake that are easy to introduce while editing:

  ERRORS (exit 1):
    - Unbalanced { } braces in script files.
    - Missing UTF-8 BOM on localization .yml files (CK3 silently fails to read
      loc files saved without a BOM).
    - References to aura_* scripted effects / triggers / script values that are
      not defined anywhere in the mod (typos, renamed-but-not-updated calls).
    - trigger_event references to aura_kings.* events that don't exist.
    - has_trait/add_trait/remove_trait references to aura_* traits not defined.

  WARNINGS (exit 0):
    - desc/title/selection_tooltip/option-name loc keys with no matching entry
      in any localization .yml.
    - Odd number of quotes on a script line.

Run manually:  python3 scripts/validate_mod.py
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCRIPT_DIRS = ["common", "events"]
LOC_DIR = os.path.join("localization")

errors = []
warnings = []


def rel(path):
    return os.path.relpath(path, ROOT)


def iter_files(subdir, exts):
    base = os.path.join(ROOT, subdir)
    for dirpath, _, files in os.walk(base):
        for f in sorted(files):
            if os.path.splitext(f)[1] in exts:
                yield os.path.join(dirpath, f)


def read_text(path):
    with open(path, encoding="utf-8-sig") as fh:  # utf-8-sig strips any BOM
        return fh.read()


def code_only(text):
    """Strip '#' comments (respecting strings) so comments aren't scanned as
    code references. Strings don't span lines in Paradox script."""
    out = []
    for line in text.splitlines():
        in_string = False
        buf = []
        for c in line:
            if c == '"':
                in_string = not in_string
            elif c == "#" and not in_string:
                break
            buf.append(c)
        out.append("".join(buf))
    return "\n".join(out)


# --- Tokenizer: strip comments/strings, track braces & quotes -----------------

def scan_braces_and_quotes(path):
    """Return (net_brace, went_negative, lines_with_odd_quotes)."""
    text = read_text(path)
    depth = 0
    went_negative = False
    odd_lines = []
    for lineno, line in enumerate(text.splitlines(), 1):
        in_string = False
        quote_count = 0
        i = 0
        while i < len(line):
            c = line[i]
            if c == '"':
                in_string = not in_string
                quote_count += 1
            elif c == "#" and not in_string:
                break  # rest of line is a comment
            elif not in_string:
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth < 0:
                        went_negative = True
            i += 1
        if quote_count % 2 != 0:
            odd_lines.append(lineno)
    return depth, went_negative, odd_lines


# --- Definitions --------------------------------------------------------------

# Top-level "ident = {" (no leading whitespace) = an object definition.
DEF_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_.]*)\s*=\s*\{")

defined_effects = set()
defined_triggers = set()
defined_values = set()
defined_events = set()
defined_traits = set()
defined_loc_keys = set()


def collect_definitions():
    for path in iter_files("common", {".txt"}):
        r = rel(path)
        for line in read_text(path).splitlines():
            m = DEF_RE.match(line)
            if not m:
                continue
            name = m.group(1)
            if "/scripted_effects/" in r or r.endswith("scripted_effects"):
                if "scripted_effects" in r:
                    defined_effects.add(name)
            if "scripted_triggers" in r:
                defined_triggers.add(name)
            if "script_values" in r:
                defined_values.add(name)
            if "/traits/" in r or "\\traits\\" in r:
                defined_traits.add(name)
    for path in iter_files("events", {".txt"}):
        for line in read_text(path).splitlines():
            m = DEF_RE.match(line)
            if m and m.group(1).startswith("aura_kings."):
                defined_events.add(m.group(1))


def collect_loc_keys():
    locbase = os.path.join(ROOT, LOC_DIR)
    if not os.path.isdir(locbase):
        return
    key_re = re.compile(r"^\s*([A-Za-z0-9_.]+):\d")
    for path in iter_files(LOC_DIR, {".yml"}):
        for line in read_text(path).splitlines():
            m = key_re.match(line)
            if m:
                defined_loc_keys.add(m.group(1))


# --- Reference checks ---------------------------------------------------------

EFFECT_REF = re.compile(r"\b(aura_[a-z0-9_]*_effect)\b")
TRIGGER_REF = re.compile(r"\b(aura_[a-z0-9_]*_trigger)\b")
VALUE_REF = re.compile(r"\b(aura_[a-z0-9_]*_value)\b")
EVENT_REF = re.compile(r"trigger_event\s*=\s*(aura_kings\.[0-9]+)")
TRAIT_REF = re.compile(r"\b(?:has_trait|add_trait|remove_trait)\s*=\s*(aura_[a-z0-9_]+)")

LOC_FIELD_REF = re.compile(r"\b(?:desc|title|selection_tooltip|tooltip)\s*=\s*([A-Za-z_][A-Za-z0-9_.]*)\b")
# option/name loc refs only when dotted (variable names never contain a dot)
NAME_LOC_REF = re.compile(r"\bname\s*=\s*([A-Za-z_][A-Za-z0-9_]*\.[A-Za-z0-9_.]+)")


def check_references():
    for sub in SCRIPT_DIRS:
        for path in iter_files(sub, {".txt"}):
            r = rel(path)
            text = code_only(read_text(path))
            for tok in set(EFFECT_REF.findall(text)):
                if tok not in defined_effects:
                    errors.append(f"{r}: undefined scripted effect '{tok}'")
            for tok in set(TRIGGER_REF.findall(text)):
                if tok not in defined_triggers:
                    errors.append(f"{r}: undefined scripted trigger '{tok}'")
            for tok in set(VALUE_REF.findall(text)):
                if tok not in defined_values:
                    errors.append(f"{r}: undefined script value '{tok}'")
            for tok in set(EVENT_REF.findall(text)):
                if tok not in defined_events:
                    errors.append(f"{r}: trigger_event to undefined event '{tok}'")
            for tok in set(TRAIT_REF.findall(text)):
                if tok not in defined_traits:
                    errors.append(f"{r}: reference to undefined trait '{tok}'")
            # loc coverage (warnings)
            for tok in set(LOC_FIELD_REF.findall(text)):
                if tok in ("yes", "no"):
                    continue
                if tok not in defined_loc_keys:
                    warnings.append(f"{r}: desc/title/tooltip loc key '{tok}' has no localization entry")
            for tok in set(NAME_LOC_REF.findall(text)):
                if tok not in defined_loc_keys:
                    warnings.append(f"{r}: option name loc key '{tok}' has no localization entry")


# --- Brace / BOM checks -------------------------------------------------------

def check_braces():
    for sub in SCRIPT_DIRS:
        for path in iter_files(sub, {".txt", ".gui"}):
            net, neg, odd = scan_braces_and_quotes(path)
            r = rel(path)
            if net != 0:
                errors.append(f"{r}: unbalanced braces (net {net:+d})")
            elif neg:
                errors.append(f"{r}: closing brace before matching open")
            for ln in odd:
                warnings.append(f"{r}:{ln}: odd number of quotes on line")


def check_bom():
    locbase = os.path.join(ROOT, LOC_DIR)
    if not os.path.isdir(locbase):
        return
    for path in iter_files(LOC_DIR, {".yml"}):
        with open(path, "rb") as fh:
            head = fh.read(3)
        if head != b"\xef\xbb\xbf":
            errors.append(f"{rel(path)}: missing UTF-8 BOM (CK3 will not read this loc file)")


def main():
    collect_definitions()
    collect_loc_keys()
    check_braces()
    check_bom()
    check_references()

    print("Aura Kings mod validation")
    print(f"  defined: {len(defined_effects)} effects, {len(defined_triggers)} triggers, "
          f"{len(defined_values)} values, {len(defined_events)} events, "
          f"{len(defined_traits)} traits, {len(defined_loc_keys)} loc keys")

    if warnings:
        print(f"\n  {len(warnings)} warning(s):")
        for w in warnings:
            print(f"    ! {w}")

    if errors:
        print(f"\n  {len(errors)} ERROR(s):")
        for e in errors:
            print(f"    X {e}")
        print("\nFAILED")
        return 1

    print("\nOK — no errors.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
