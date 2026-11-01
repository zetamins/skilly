#!/usr/bin/env bash
# Football skills installer — installs the 15 football-* skills for any or all of
# Kimi Code, Claude Code, Codex and OpenCode.
#
# What it does:
#   1. Copies this repo to a canonical home: ~/.football-skills (single source of truth)
#   2. Symlinks every football-* skill into the chosen harnesses' skills directories,
#      so one update propagates everywhere
#   3. Verifies the shared scripts resolve (the skills reference ~/.kimi-code/skills/
#      football-match/scripts, which install #2 guarantees exists via the Kimi link —
#      Kimi Code is therefore installed ALWAYS, as the script anchor)
#
# Usage: ./install.sh [all|kimi|claude|codex|opencode]   (default: all)
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)"
CANON="$HOME/.football-skills"
KIMI="$HOME/.kimi-code/skills"
CLAUDE="$HOME/.claude/skills"
CODEX="$HOME/.codex/skills"
OPENCODE="$HOME/.config/opencode/skills"

echo "== installing canonical copy to $CANON"
mkdir -p "$CANON"
for d in "$SRC"/football-*/; do
  name="$(basename "$d")"
  rm -rf "$CANON/$name"
  cp -r "$d" "$CANON/$name"
done

link_all() {  # $1 = target skills dir
  mkdir -p "$1"
  for d in "$CANON"/football-*/; do
    name="$(basename "$d")"
    ln -sfn "$d" "$1/$name"
  done
}

TARGETS="${1:-all}"
case "$TARGETS" in
  all) set -- kimi claude codex opencode;;
  *) set -- "$TARGETS";;
esac

for t in "$@"; do
  case "$t" in
    kimi)     link_all "$KIMI";     echo "kimi:     linked $(ls -d "$KIMI"/football-* | wc -l) skills in $KIMI";;
    claude)   link_all "$CLAUDE";   echo "claude:   linked in $CLAUDE";;
    codex)    link_all "$CODEX";    echo "codex:    linked in $CODEX (or add the dir to your codex skills config)";;
    opencode) link_all "$OPENCODE"; echo "opencode: linked in $OPENCODE";;
    *) echo "unknown target: $t (use kimi|claude|codex|opencode|all)"; exit 2;;
  esac
done

# verify the shared script anchor resolves
if python3 "$KIMI/football-match/scripts/calc.py" --lam 1.5 1.2 --home A --away B >/dev/null 2>&1; then
  echo "== OK: calc.py runs; the skills are installed and the shared scripts resolve"
else
  echo "!! calc.py failed — python3 problem, not a skills problem"; exit 1
fi
echo
echo "Optional (for football-scrape's live runner): python venv with httpx+playwright:"
echo "  python3 -m venv ~/.venvs/football-scrape && ~/.venvs/football-scrape/bin/pip install 'httpx[http2]' playwright"
echo "The council pipeline (run_collection.py) also needs an agent CLI: opencode, claude, or codex."
