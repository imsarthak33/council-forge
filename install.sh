#!/usr/bin/env bash
#
# Council Forge — installer
#
# Installs the council-forge skill into Claude Code (personal or project scope).
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/<org>/council-forge/main/install.sh | bash
#   curl -fsSL .../install.sh | bash -s -- --project
#   ./install.sh                 # run locally from a cloned repo
#   ./install.sh --uninstall
#
# Flags:
#   --personal      Install to ~/.claude/skills/council-forge (default, all projects)
#   --project       Install to ./.claude/skills/council-forge (this repo only)
#   --force         Overwrite an existing install without prompting
#   --uninstall     Remove an existing install
#   --repo <url>    Override the source repository (default: env COUNCIL_FORGE_REPO or upstream)
#   --branch <name> Override the branch/tag to install (default: env COUNCIL_FORGE_BRANCH or "main")
#   -h, --help      Show this help and exit
#
# Env overrides: COUNCIL_FORGE_REPO, COUNCIL_FORGE_BRANCH

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SKILL_NAME="council-forge"
REPO_URL="${COUNCIL_FORGE_REPO:-https://github.com/council-forge/council-forge.git}"
REPO_BRANCH="${COUNCIL_FORGE_BRANCH:-main}"

SCOPE="personal"
FORCE=0
UNINSTALL=0
DRY_RUN=0

# ---------------------------------------------------------------------------
# Output helpers (degrade gracefully when not a TTY, e.g. piped from curl)
# ---------------------------------------------------------------------------

if [ -t 1 ]; then
  C_BOLD="$(printf '\033[1m')"; C_GREEN="$(printf '\033[32m')"
  C_RED="$(printf '\033[31m')"; C_YELLOW="$(printf '\033[33m')"
  C_DIM="$(printf '\033[2m')"; C_RESET="$(printf '\033[0m')"
else
  C_BOLD=""; C_GREEN=""; C_RED=""; C_YELLOW=""; C_DIM=""; C_RESET=""
fi

info()  { printf '%s\n' "${C_DIM}==>${C_RESET} $*"; }
ok()    { printf '%s\n' "${C_GREEN}✔${C_RESET} $*"; }
warn()  { printf '%s\n' "${C_YELLOW}!${C_RESET} $*" >&2; }
fail()  { printf '%s\n' "${C_RED}✘ $*${C_RESET}" >&2; exit 1; }

# ---------------------------------------------------------------------------
# Arg parsing
# ---------------------------------------------------------------------------

print_help() {
  cat <<'HELP'
Council Forge — installer

Installs the council-forge skill into Claude Code (personal or project scope).

Usage:
  curl -fsSL https://raw.githubusercontent.com/<org>/council-forge/main/install.sh | bash
  curl -fsSL .../install.sh | bash -s -- --project
  ./install.sh                 # run locally from a cloned repo
  ./install.sh --uninstall

Flags:
  --personal      Install to ~/.claude/skills/council-forge (default, all projects)
  --project       Install to ./.claude/skills/council-forge (this repo only)
  --force         Overwrite an existing install without prompting
  --uninstall     Remove an existing install
  --repo <url>    Override the source repository (default: env COUNCIL_FORGE_REPO or upstream)
  --branch <name> Override the branch/tag to install (default: env COUNCIL_FORGE_BRANCH or "main")
  -h, --help      Show this help and exit

Env overrides: COUNCIL_FORGE_REPO, COUNCIL_FORGE_BRANCH
HELP
}

while [ $# -gt 0 ]; do
  case "$1" in
    --personal) SCOPE="personal"; shift ;;
    --project)  SCOPE="project"; shift ;;
    --force)    FORCE=1; shift ;;
    --uninstall) UNINSTALL=1; shift ;;
    --dry-run)  DRY_RUN=1; shift ;;
    --repo)     REPO_URL="${2:?--repo requires a URL}"; shift 2 ;;
    --branch)   REPO_BRANCH="${2:?--branch requires a name}"; shift 2 ;;
    -h|--help)  print_help; exit 0 ;;
    *) fail "Unknown argument: $1 (see --help)" ;;
  esac
done

# ---------------------------------------------------------------------------
# Resolve target directory
# ---------------------------------------------------------------------------

if [ "$SCOPE" = "personal" ]; then
  TARGET_DIR="${HOME}/.claude/skills/${SKILL_NAME}"
else
  TARGET_DIR="$(pwd)/.claude/skills/${SKILL_NAME}"
fi

# ---------------------------------------------------------------------------
# Uninstall
# ---------------------------------------------------------------------------

if [ "$UNINSTALL" -eq 1 ]; then
  if [ ! -d "$TARGET_DIR" ]; then
    warn "Nothing installed at ${TARGET_DIR}"
    exit 0
  fi
  if [ "$DRY_RUN" -eq 1 ]; then
    info "Would remove ${TARGET_DIR}"
    exit 0
  fi
  rm -rf "$TARGET_DIR"
  ok "Removed ${TARGET_DIR}"
  exit 0
fi

# ---------------------------------------------------------------------------
# Preflight
# ---------------------------------------------------------------------------

command -v git >/dev/null 2>&1 || fail "git is required but was not found on PATH."

if [ -d "$TARGET_DIR" ] && [ "$FORCE" -ne 1 ]; then
  BACKUP_DIR="${TARGET_DIR}.bak.$(date +%Y%m%d%H%M%S)"
  warn "An install already exists at ${TARGET_DIR}"
  if [ -t 0 ]; then
    printf '  Back it up and reinstall? [y/N] '
    read -r REPLY
    case "$REPLY" in
      y|Y) ;;
      *) fail "Aborted. Re-run with --force to overwrite without asking." ;;
    esac
  else
    fail "Re-run with --force to overwrite, or --uninstall first. (no TTY to prompt)"
  fi
  [ "$DRY_RUN" -eq 1 ] || mv "$TARGET_DIR" "$BACKUP_DIR"
  ok "Backed up existing install to ${BACKUP_DIR}"
elif [ -d "$TARGET_DIR" ] && [ "$FORCE" -eq 1 ]; then
  info "Overwriting existing install at ${TARGET_DIR} (--force)"
  [ "$DRY_RUN" -eq 1 ] || rm -rf "$TARGET_DIR"
fi

mkdir -p "$(dirname "$TARGET_DIR")"

# ---------------------------------------------------------------------------
# Acquire skill source
#   - If this script is sitting inside a clone that already contains SKILL.md,
#     install directly from there (no network needed).
#   - Otherwise (e.g. curl | bash), shallow-clone the repo into a temp dir.
# ---------------------------------------------------------------------------

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]:-$0}")" >/dev/null 2>&1 && pwd -P || true)"

TMP_DIR=""
cleanup() { [ -n "$TMP_DIR" ] && rm -rf "$TMP_DIR"; }
trap cleanup EXIT

if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/SKILL.md" ]; then
  SOURCE_DIR="$SCRIPT_DIR"
  info "Installing from local checkout: ${SOURCE_DIR}"
else
  info "Fetching ${REPO_URL} (${REPO_BRANCH})"
  TMP_DIR="$(mktemp -d)"
  if [ "$DRY_RUN" -eq 1 ]; then
    info "Would clone ${REPO_URL}#${REPO_BRANCH} into ${TARGET_DIR}"
    exit 0
  fi
  git clone --quiet --depth 1 --branch "$REPO_BRANCH" "$REPO_URL" "$TMP_DIR/src" \
    || fail "Could not clone ${REPO_URL}#${REPO_BRANCH}. Check the URL/branch, or pass --repo / --branch."
  rm -rf "$TMP_DIR/src/.git"
  SOURCE_DIR="$TMP_DIR/src"
fi

[ -f "$SOURCE_DIR/SKILL.md" ] || fail "SKILL.md not found in source — installer or repo layout may have changed."

# ---------------------------------------------------------------------------
# Install
# ---------------------------------------------------------------------------

if [ "$DRY_RUN" -eq 1 ]; then
  info "Would copy ${SOURCE_DIR} -> ${TARGET_DIR}"
  exit 0
fi

mkdir -p "$TARGET_DIR"
cp -R "$SOURCE_DIR"/. "$TARGET_DIR"/
rm -f "$TARGET_DIR/install.sh"   # the installer itself isn't part of the skill payload

# ---------------------------------------------------------------------------
# Validate
# ---------------------------------------------------------------------------

SKILL_MD="$TARGET_DIR/SKILL.md"
[ -f "$SKILL_MD" ] || fail "Install failed: ${SKILL_MD} is missing."
head -n1 "$SKILL_MD" | grep -q '^---$' || fail "Install failed: ${SKILL_MD} has no YAML frontmatter."
grep -q '^name:' "$SKILL_MD"        || fail "Install failed: SKILL.md frontmatter has no 'name'."
grep -q '^description:' "$SKILL_MD" || fail "Install failed: SKILL.md frontmatter has no 'description'."

NESTED_COUNT="$(find "$TARGET_DIR" -name SKILL.md | wc -l | tr -d ' ')"
[ "$NESTED_COUNT" -eq 1 ] || fail "Install failed: expected exactly one SKILL.md, found ${NESTED_COUNT}."

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------

ok "Council Forge installed to ${TARGET_DIR}"
echo
echo "${C_BOLD}Next steps${C_RESET}"
if [ "$SCOPE" = "personal" ]; then
  echo "  Start (or restart) Claude Code — the skill is available in every project."
else
  echo "  Start Claude Code inside this project — the skill is committed to .claude/skills/."
fi
echo "  Try:  ${C_DIM}/council-forge${C_RESET}  or just ask:"
echo "        \"give me a council on whether to launch this fintech product in India\""
echo
echo "  Pre-built panels live in examples/ — cybersecurity, fintech-india, biotech-startup, climate-tech."
echo "  Uninstall any time:  ${C_DIM}curl -fsSL <install-url> | bash -s -- --uninstall$([ "$SCOPE" = "project" ] && printf ' --project')${C_RESET}"
