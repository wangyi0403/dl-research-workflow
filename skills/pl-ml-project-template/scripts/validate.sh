#!/usr/bin/env bash
# Validate a scaffolded project: check imports and YAML parsing.
# Usage: bash scripts/validate.sh /path/to/scaffolded/project
set -euo pipefail

PROJECT="${1:?Usage: validate.sh <project_dir>}"

if [ ! -d "$PROJECT" ]; then
  echo "FAIL: directory not found: $PROJECT" >&2
  exit 1
fi

ERRORS=0

# Check required files exist
for f in main.py utils.py model/__init__.py model/model_interface.py data/__init__.py data/data_interface.py configs/default.yaml; do
  if [ ! -f "$PROJECT/$f" ]; then
    echo "FAIL: missing $f" >&2
    ERRORS=$((ERRORS + 1))
  fi
done

# Check YAML parses
PYTHON_CMD=$(command -v python 2>/dev/null || command -v python3 2>/dev/null || echo python)
if ! "$PYTHON_CMD" -c "import yaml; yaml.safe_load(open('$PROJECT/configs/default.yaml'))" 2>/dev/null; then
  echo "FAIL: configs/default.yaml is not valid YAML" >&2
  ERRORS=$((ERRORS + 1))
fi

# Check imports resolve (needs torch installed)
if "$PYTHON_CMD" -c "import torch" 2>/dev/null; then
  if ! (cd "$PROJECT" && "$PYTHON_CMD" -c "from model import MInterface; from data import DInterface" 2>/dev/null); then
    echo "FAIL: import check failed" >&2
    ERRORS=$((ERRORS + 1))
  else
    echo "OK: imports resolve"
  fi
else
  echo "SKIP: torch not installed, skipping import check"
fi

if [ "$ERRORS" -gt 0 ]; then
  echo "FAIL: $ERRORS errors found" >&2
  exit 1
fi

echo "OK: project at $PROJECT passed validation"
