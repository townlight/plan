<a id="civicplan-user-manual"></a>

# Townlight Planning User Manual

## For Residents And Municipal Decision-Makers

Townlight Planning helps cities connect planning proposals to adopted plan policies. It can show sample cited policy context, highlight consistency factors for staff review, and produce records-ready plan-policy exports.

Current state: v0.2.2 corrective demotion state. The previous v1.0.0 release was published in error. This narrow truth-repair release is no functional upgrade; it exists solely to supersede the false v1.0.0 release from 2026-05-21 in GitHub's Latest impression, with the Townlight Core pin unchanged. The module includes deterministic cited plan-policy lookup, staff-only local policy ingestion, optional database-backed policy and staff-analysis records, a goal/objective/policy navigator, cited plan Q&A, cross-plan synthesis, amendment history, progress tracking, a cited zoning policy-context endpoint for Townlight Zoning, a draft staff-report context endpoint for Townlight Meetings, local adversarial integration mocks, Townlight Core v1.1.0 release-wheel alignment, and a public UI at `/civicplan`. It does not provide legal advice, official planning determinations, live external calls by default, permitting-system write-back, or final staff-report approval.

## For IT And Technical Staff

Townlight Planning is a FastAPI Python package pinned to the published Townlight Core v1.1.0 release wheel. The current runtime exposes:

- `GET /`
- `GET /health`
- `GET /civicplan`
- `POST /api/v1/civicplan/policies/lookup`
- `POST /api/v1/civicplan/policies/ingest`
- `GET /api/v1/civicplan/plans/navigator`
- `POST /api/v1/civicplan/questions/answer`
- `POST /api/v1/civicplan/plans/synthesis`
- `GET /api/v1/civicplan/amendments/history`
- `GET /api/v1/civicplan/progress/targets`
- `POST /api/v1/civicplan/context/zoning`
- `POST /api/v1/civicplan/context/civicclerk`
- `POST /api/v1/civicplan/integrations/mock`
- `POST /api/v1/civicplan/consistency/check`
- `POST /api/v1/civicplan/staff-analysis/draft`; persisted records require `X-CivicPlan-Role: staff` and `X-CivicPlan-Staff-Key` when `CIVICPLAN_POLICY_DB_URL` is configured
- `GET /api/v1/civicplan/staff-analysis/{analysis_id}` when `CIVICPLAN_POLICY_DB_URL` is configured and both staff headers are present
- `POST /api/v1/civicplan/export`

Set `CIVICPLAN_POLICY_DB_URL` to persist plan-policy records and staff-analysis outlines. Persisted staff-analysis create/read routes are staff-only and require `CIVICPLAN_STAFF_API_KEY`, `X-CivicPlan-Role: staff`, and matching `X-CivicPlan-Staff-Key`. Townlight Planning uses Townlight Core `staff_key_gate` for timing-safe key comparison. Leave it unset for deterministic sample behavior.

Run local verification with:

```powershell
python -m pip install https://github.com/CivicSuite/civiccore/releases/download/v1.1.0/civiccore-1.1.0-py3-none-any.whl
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## Architecture

```mermaid
flowchart LR
  PublicUser["Resident or staff planner"] --> CivicPlan["CivicPlan"]
  CivicPlan --> CivicCore["CivicCore v1.1.0"]
CivicPlan -. policy-context API .-> CivicZone["CivicZone context"]
CivicPlan -. staff-report context .-> CivicClerk["CivicClerk context"]
```

Townlight Planning depends on Townlight Core. Townlight Core does not depend on Townlight Planning. Townlight Planning v0.2.2 exposes deterministic, review-required context contracts for Townlight Zoning and Townlight Meetings; live vendor calls and official decisions remain outside Townlight Planning.
