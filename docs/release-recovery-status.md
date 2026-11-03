# Townlight Planning Release Status

Date: 2026-05-21
Repo: `Townlight/townlight_planning`

## Current Verdict

`v1.0.0` is the active corrective demotion state for Townlight Planning. The
current release pass rechecks the repo with local release gates, browser QA,
documentation truth checks, build artifacts, adversarial integration tests, and
current Townlight Core v1.1.0 dependency alignment. The previous demotion remains
historical context only.

## Recovery Gates

| Gate | Current status | Evidence |
| --- | --- | --- |
| Public claim recovery | Passing locally | README, text README, user manual, docs landing page, changelog, and docs checks now describe the v1.0.0 corrective demotion state without overstating legal advice, official determinations, live vendor behavior, permitting write-back, or elected-body decisions. |
| Native WSL/Linux proof | Historical pass | WSL selected `.venv-wsl/bin/python3`, reported platform `linux`, and completed `VERIFY-RELEASE: PASSED`. |
| Runtime install proof | Historical pass | Fresh WSL editable install succeeded with the published Townlight Core release wheel and Hatch direct references enabled. |
| Security scan | Historical pass | Tracked-file secret scan returned no matches. |
| Docs-source enforcement | Passing locally | `scripts/verify-docs.sh` blocks stale product-release claims. |
| Mock-vs-production labeling | Passing locally | Existing docs distinguish local adversarial mocks, no legal advice, no official planning determinations, and no live external calls by default. |
| Browser/user-flow QA | Passing locally | Playwright checked live `/townlight_planning` at desktop and mobile widths plus `/docs` and `/health`; see `docs/qa/current-townlight_planning-release-qa.md`. |
| Release gate | Passing locally | `scripts/verify-release.sh` passed with version checks, tests, docs gate, placeholder import gate, Ruff, package build, and SHA256 generation. |

## Current Evidence

- Local release gate on Windows: `33 passed`; docs gate, placeholder import
  gate, ruff, build artifacts, and SHA256 generation passed.
- Historical native WSL release gate: `33 passed`; docs gate, placeholder
  import gate, ruff, build artifacts, and SHA256 generation passed.
- WSL fresh install: `python -m pip install -e .[dev]` succeeded in
  `.venv-wsl`.
- Browser QA: live `/townlight_planning` desktop `1440x1000` and mobile `390x844`,
  `/docs` desktop, and `/health` passed with no console messages, no page
  errors, no horizontal overflow, and keyboard focus reaching expected links or
  content.

## Sign-Off Boundary

This release status does not claim official planning determinations, legal
advice, live vendor calls by default, permitting-system write-back, elected-body
decisions, suite-wide city readiness, or macOS lifecycle certification. Remote
PR/CI, release assets, and Townlight installer/module-selection truth are
recorded separately when the release is published and reconciled.
