#!/usr/bin/env bash
set -euo pipefail

required=(
  "README.md"
  "README.txt"
  "CHANGELOG.md"
  "CONTRIBUTING.md"
  "LICENSE"
  "LICENSE-CODE"
  "LICENSE-DOCS"
  ".gitignore"
  "AGENTS.md"
  "USER-MANUAL.md"
  "SECURITY.md"
  "SUPPORT.md"
  "CODE_OF_CONDUCT.md"
  ".github/PULL_REQUEST_TEMPLATE.md"
  ".github/ISSUE_TEMPLATE/bug_report.md"
  ".github/ISSUE_TEMPLATE/feature_request.md"
  ".github/ISSUE_TEMPLATE/config.yml"
  "docs/RECONCILIATION.md"
  "docs/MILESTONES.md"
  "docs/IMPLEMENTATION_PLAN.md"
  "docs/github-discussions-seed.md"
  "MILESTONE_0_7_DONE.md"
  "docs/index.html"
  "docs/browser-qa-civicplan-v0.1.2-zone-context-summary.md"
  "PRODUCTION_DEPTH_POLICY_PERSISTENCE_DONE.md"
  "PRODUCTION_DEPTH_ZONE_CONTEXT_CONTRACT_DONE.md"
  "pyproject.toml"
  "civicplan/__init__.py"
  "civicplan/main.py"
  "civicplan/policy_lookup.py"
  "civicplan/consistency.py"
  "civicplan/staff_analysis.py"
  "civicplan/plan_workflows.py"
  "civicplan/integration_mocks.py"
  "civicplan/records_export.py"
  "civicplan/public_ui.py"
)

echo "==> Required-artifact check"
for file in "${required[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "FAIL: missing required artifact: $file" >&2
    exit 1
  fi
done

echo "==> Current-facing shipped/planned truth check"
current_files=("README.md" "README.txt" "USER-MANUAL.md" "docs/index.html")
bad_markers=(
  "official planning determinations are available"
  "legal advice is available"
  "live GIS is available"
  "live LLM calls are available"
  "plan document ingestion is available"
  "permitting-system integrations are available"
  "production staff-review queues are available"
  "v0.2.0 recovery release"
  "0.2.0 recovery release"
  "current product release"
  "published v0.2.0 recovery label"
  "demoted recovery label"
)

for file in "${current_files[@]}"; do
  for marker in "${bad_markers[@]}"; do
    if grep -Fqi "$marker" "$file"; then
      echo "FAIL: stale/planned-as-shipped marker '$marker' found in $file" >&2
      exit 1
    fi
  done
done

required_markers=(
  "Townlight Beta 1"
  "0.4.0.dev1"
)

for marker in "${required_markers[@]}"; do
  if ! grep -Fq "$marker" README.md; then
    echo "FAIL: required current release marker '$marker' missing from README.md" >&2
    exit 1
  fi
done

echo "VERIFY-DOCS: PASSED"
