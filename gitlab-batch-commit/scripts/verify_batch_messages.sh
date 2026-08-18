#!/usr/bin/env bash
# Verify commit messages contain no Cursor-injected email Co-authored-by trailer.
# Usage:
#   verify_batch_messages.sh <commit_count>
#   verify_batch_messages.sh --since <start_ref>
set -euo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: not inside a git repository" >&2
  exit 1
fi

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
  exit 1
fi

if git log "$RANGE" --format=%B | grep -qi 'cursoragent@cursor.com'; then
  echo "FAIL: Cursor email Co-authored-by found in commits (${RANGE})" >&2
  exit 1
fi

echo "OK: no cursoragent injection in commits (${RANGE})"
