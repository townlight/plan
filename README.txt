Townlight Planning
=========

Townlight Planning is the Townlight module for comprehensive-plan policy lookup and cited planning analysis support.

Current state: v0.2.2 corrective demotion state. The previous v1.0.0 release was published in error. This narrow truth-repair release is no functional upgrade; it exists solely to supersede the false v1.0.0 release from 2026-05-21 in GitHub's Latest impression, with the Townlight Core pin unchanged. This repo contains a deterministic scaffold aligned to the Townlight Core v1.1.0 release wheel, health/root endpoints, documentation gates, cited plan-policy lookup, staff-only local policy ingestion via CIVICPLAN_POLICY_DB_URL, goal/objective/policy navigation, cited plan Q&A, cross-plan synthesis, amendment history, progress tracking, Townlight Zoning and Townlight Meetings context contracts, policy-consistency support, staff-analysis outline support, records-ready export checklist, local adversarial integration mocks, and accessible public UI at /civicplan.

It does not ship official planning determinations, legal advice, live external vendor calls by default, permitting-system write-back, or elected-body decisions.

Core API:
- GET /
- GET /health
- GET /civicplan
- POST /api/v1/civicplan/policies/lookup
- POST /api/v1/civicplan/context/zoning
- POST /api/v1/civicplan/consistency/check
- POST /api/v1/civicplan/staff-analysis/draft; persisted records require X-CivicPlan-Role: staff when CIVICPLAN_POLICY_DB_URL is configured
- GET /api/v1/civicplan/staff-analysis/{analysis_id} when CIVICPLAN_POLICY_DB_URL is configured and X-CivicPlan-Role: staff is present
- POST /api/v1/civicplan/export

Quickstart: install Townlight Core first with python -m pip install https://github.com/CivicSuite/civiccore/releases/download/v1.1.0/civiccore-1.1.0-py3-none-any.whl, then run python -m pip install -e ".[dev]".

Set CIVICPLAN_POLICY_DB_URL to enable persistent plan-policy and staff-analysis records. Persisted staff-analysis create/read routes are staff-only and require X-CivicPlan-Role: staff from a trusted staff or service workflow. When unset, Townlight Planning continues to use deterministic in-memory sample data.

Code license: AGPL-3.0-only, with the TownLight Public Institution Exception for qualifying deployments. See LICENSE and LICENSE-EXCEPTION.md. Documentation license: CC BY 4.0 (LICENSE-DOCS).
