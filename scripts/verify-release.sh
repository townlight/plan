#!/usr/bin/env bash
set -euo pipefail

VERSION="0.3.0"

find_python() {
  local candidates=()
  if [[ -n "${CIVICPLAN_RELEASE_PYTHON:-}" ]]; then
    candidates+=("${CIVICPLAN_RELEASE_PYTHON}")
  fi
  command -v python3 >/dev/null 2>&1 && candidates+=("$(command -v python3)")
  command -v python >/dev/null 2>&1 && candidates+=("$(command -v python)")
  command -v py >/dev/null 2>&1 && candidates+=("py -3")
  [[ -x "/c/Windows/py.exe" ]] && candidates+=("/c/Windows/py.exe -3")
  [[ -x "/mnt/c/Windows/py.exe" ]] && candidates+=("/mnt/c/Windows/py.exe -3")
  if command -v powershell.exe >/dev/null 2>&1 && command -v wslpath >/dev/null 2>&1; then
    local win_python
    win_python="$(powershell.exe -NoProfile -Command "(Get-Command python -ErrorAction SilentlyContinue).Source" 2>/dev/null | tr -d '\r' | head -n 1)"
    if [[ -n "$win_python" ]]; then
      candidates+=("$(wslpath -u "$win_python")")
    fi
  fi

  for candidate in "${candidates[@]}"; do
    if ${candidate} -c "import pytest, ruff, build" >/dev/null 2>&1; then
      echo "$candidate"
      return 0
    fi
  done
  return 1
}

PYTHON_BIN="$(find_python)" || {
  echo "FAIL: Python launcher not found. Install Python or add python/python3/py to PATH." >&2
  exit 1
}

echo "==> Version surface check"
${PYTHON_BIN} - <<'PY'
from pathlib import Path
import tomllib

version = "0.3.0"
root = Path(".")
pyproject = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
assert pyproject["project"]["version"] == version, pyproject["project"]["version"]
namespace: dict[str, str] = {}
exec((root / "civicplan" / "__init__.py").read_text(encoding="utf-8"), namespace)
assert namespace["__version__"] == version, namespace["__version__"]
for path in [
    "README.md",
    "README.txt",
    "USER-MANUAL.md",
    "CHANGELOG.md",
    "SECURITY.md",
]:
    text = (root / path).read_text(encoding="utf-8")
    assert "0.3.0" in text, f"missing release version in {path}"
    assert "0.1.1.dev0" not in text, f"stale dev version in {path}"
print("PASS: version surfaces synchronized")
PY

echo "==> Test suite"
${PYTHON_BIN} -m pytest -q

echo "==> Documentation gate"
bash scripts/verify-docs.sh

echo "==> Placeholder import gate"
${PYTHON_BIN} scripts/check-civiccore-placeholder-imports.py

echo "==> Ruff"
${PYTHON_BIN} -m ruff check .

echo "==> Build artifacts"
rm -rf dist
${PYTHON_BIN} -m build
${PYTHON_BIN} - <<'PY'
from pathlib import Path
import hashlib

dist = Path("dist")
wheel = dist / "civicplan-0.3.0-py3-none-any.whl"
sdist = dist / "civicplan-0.3.0.tar.gz"
assert wheel.exists(), f"missing {wheel}"
assert sdist.exists(), f"missing {sdist}"
lines = []
for path in [wheel, sdist]:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    lines.append(f"{digest}  {path.name}\n")
(dist / "SHA256SUMS.txt").write_text("".join(lines), encoding="utf-8")
import tarfile
import zipfile
required = (
    "civicplan/migrations/env.py",
    "civicplan/migrations/versions/civicplan_0001_sources.py",
    "civicplan/source_schema.py",
    "civicplan/source_bundle.py",
    "civicplan/source_store.py",
    "civicplan/migrations/versions/civicplan_0002_workflows.py",
    "civicplan/workflow_store.py",
    "civicplan/workflow_api.py",
)
with zipfile.ZipFile(wheel) as archive:
    assert all(path in archive.namelist() for path in required)
with tarfile.open(sdist) as archive:
    names = archive.getnames()
    assert all(any(name.endswith("/" + path) for name in names) for path in required)
print("PASS: build artifacts, migration resources and SHA256SUMS.txt created")
PY

echo "VERIFY-RELEASE: PASSED"
