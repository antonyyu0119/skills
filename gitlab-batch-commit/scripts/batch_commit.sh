#!/usr/bin/env bash
# Create a commit via git commit-tree (bypasses Cursor git commit trailer injection).
# Usage: batch_commit.sh -F <msgfile> -- <file1> <file2> ...
set -euo pipefail

MSGFILE=""
FILES=()
PARSE_FILES=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    -F)
      MSGFILE="${2:-}"
      shift 2
      ;;
    --)
      PARSE_FILES=true
      shift
      ;;
    *)
      if [[ "$PARSE_FILES" == true ]]; then
        FILES+=("$1")
      else
        echo "Usage: $0 -F <msgfile> -- <file1> [file2...]" >&2
        exit 1
      fi
      shift
      ;;
  esac
done

if [[ -z "$MSGFILE" || ! -f "$MSGFILE" ]]; then
  echo "Error: message file required (-F <msgfile>)" >&2
  exit 1
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "Error: at least one file path required after --" >&2
  exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: not inside a git repository" >&2
  exit 1
fi

parent=$(git rev-parse HEAD)
branch=$(git symbolic-ref HEAD)

# Load full HEAD tree into index to avoid incomplete commits.
git read-tree -u -m "$parent"
git add -- "${FILES[@]}"

tree=$(git write-tree)
commit=$(git commit-tree "$tree" -p "$parent" -F "$MSGFILE")
git update-ref "$branch" "$commit"
git reset --mixed "$commit" >/dev/null

echo "$commit"
