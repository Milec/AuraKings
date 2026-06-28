#!/usr/bin/env bash
# =============================================================================
#  Aura Kings - Crusader Kings III mod installer (Linux / macOS)
#
#  Run:  ./install.sh        (chmod +x install.sh first if needed)
#
#  Registers the mod with the CK3 launcher by writing a small descriptor into
#  your Paradox "mod" folder that points back to this repo. Nothing is copied,
#  so "git pull" here updates the mod in place.
#
#  Override the CK3 location if non-standard:  CK3_USER_DIR=/path ./install.sh
# =============================================================================
set -euo pipefail

echo
echo "  Aura Kings - CK3 mod installer"
echo "  =============================="
echo

# Repo location = directory containing this script
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default CK3 user folder per OS
case "$(uname -s)" in
    Darwin) DEFAULT_DIR="$HOME/Documents/Paradox Interactive/Crusader Kings III" ;;
    *)      DEFAULT_DIR="$HOME/.local/share/Paradox Interactive/Crusader Kings III" ;;
esac
CK3DIR="${CK3_USER_DIR:-$DEFAULT_DIR}"
MODDIR="$CK3DIR/mod"

if [ ! -d "$CK3DIR" ]; then
    echo "  ERROR: Could not find your CK3 user folder at:"
    echo "    $CK3DIR"
    echo "  Run Crusader Kings III once, or set CK3_USER_DIR=... and re-run."
    exit 1
fi

mkdir -p "$MODDIR"

DESC="$MODDIR/AuraKings.mod"
cat > "$DESC" <<EOF
version="0.1.0"
name="Aura Kings"
supported_version="1.19.*"
path="$REPO"
EOF

echo "  Installed!"
echo "    Mod source : $REPO"
echo "    Descriptor : $DESC"
echo
echo "  Next: open the CK3 launcher, add 'Aura Kings' to a playset, enable it, and play."
echo "  (If the launcher warns about the game version, edit supported_version in"
echo "   descriptor.mod and AuraKings.mod to match your CK3 version.)"
echo
