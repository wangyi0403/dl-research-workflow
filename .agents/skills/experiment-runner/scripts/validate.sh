#!/usr/bin/env bash
# Validate a generated monitor script before launch.
# Usage: bash scripts/validate.sh /path/to/generated_script.sh
set -euo pipefail

SCRIPT="${1:?Usage: validate.sh <script_path>}"

if [ ! -f "$SCRIPT" ]; then
  echo "FAIL: file not found: $SCRIPT" >&2
  exit 1
fi

# Syntax check
if ! bash -n "$SCRIPT" 2>/dev/null; then
  echo "FAIL: bash syntax error in $SCRIPT" >&2
  bash -n "$SCRIPT"
  exit 1
fi

# Required patterns
REQUIRED=(
  "MAX_CHECKS="
  "DONE_PATTERN="
  "ERROR_PATTERN="
  "INTERVALS="
  "run_check"
  "MONITOR_DONE"
)

MISSING=0
for pat in "${REQUIRED[@]}"; do
  if ! grep -q "$pat" "$SCRIPT"; then
    echo "FAIL: missing required pattern: $pat" >&2
    MISSING=$((MISSING + 1))
  fi
done

# Dangerous patterns
if grep -qE "^[[:space:]]*(error|fail|done)'" "$SCRIPT" 2>/dev/null; then
  echo "WARN: possible overly broad pattern (bare error/fail/done)" >&2
fi

if [ "$MISSING" -gt 0 ]; then
  echo "FAIL: $MISSING required patterns missing" >&2
  exit 1
fi

echo "OK: $SCRIPT passed validation"
