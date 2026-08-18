#!/usr/bin/env bash
# Remove Cursor-injected Co-authored-by email trailer from recent commits.
# Usage:
#   strip_cursor_coauthor.sh <commit_count>
#   strip_cursor_coauthor.sh --since <start_ref>
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

RANGE=""
if [[ $# -eq 1 && "$1" =~ ^[0-9]+$ ]]; then
  COUNT="$1"
  git rev-parse "HEAD~${COUNT}" >/dev/null 2>&1 || {
    echo "Error: not enough commits (need at least ${COUNT})" >&2
    exit 1
  }
  RANGE="HEAD~${COUNT}..HEAD"
elif [[ $# -eq 2 && "$1" == "--since" ]]; then
  start_ref="$2"
  git rev-parse "$start_ref" >/dev/null 2>&1 || {
    echo "Error: invalid ref: $start_ref" >&2
    exit 1
  }
  RANGE="${start_ref}..HEAD"
else
  echo "Usage: $0 <commit_count>" >&2
  echo "   or: $0 --since <start_ref>" >&2
  echo "Example: $0 9" >&2
  echo "Example: $0 --since abc1234" >&2
  exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: not inside a git repository" >&2
  exit 1
fi

if ! git log "$RANGE" --format=%B | grep -qi 'cursoragent@cursor.com'; then
  echo "OK: no Cursor email Co-authored-by in commits (${RANGE})"
  exit 0
fi

export FILTER_BRANCH_SQUELCH_WARNING=1
git filter-branch -f --msg-filter \
  'sed -E "/^[Cc][Oo]-[Aa]uthored-[Bb]y: Cursor <cursoragent@cursor.com>$/d"' \
  "$RANGE"

if ! bash "$SCRIPT_DIR/verify_batch_messages.sh" --since "${RANGE%..HEAD}"; then
  echo "Error: cleanup failed; Cursor email Co-authored-by still present" >&2
  exit 1
fi

echo "OK: removed Cursor email Co-authored-by from commits (${RANGE})"
