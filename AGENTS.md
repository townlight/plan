# CivicPlan Agent Contract

## Source Of Truth

- Upstream suite spec: `CivicSuite/civicsuite/docs/CivicSuiteUnifiedSpec.md`, especially the CivicPlan catalog entry and suite-wide non-negotiables.
- Suite ADRs: `CivicSuite/civicsuite/docs/architecture/`.
- CivicPlan supports cited comprehensive-plan, small-area-plan, transportation-plan, parks-plan, and sustainability-plan policy context. It does not replace planners, attorneys, boards, commissions, councils, or permitting systems of record.

## Non-Negotiables

- CivicPlan never makes zoning, land-use, environmental, legal, entitlement, or elected-body determinations.
- Every material answer must cite the adopted plan source used.
- Staff-analysis drafts must be marked review-required.
- Public-facing warnings must be actionable and explain the fix path.
- CivicPlan depends on CivicCore; CivicCore must never depend on CivicPlan.
- CivicPlan may reference CivicZone/CivicClerk concepts only through released contracts or deterministic sample data in v0.1.0.
- Code is AGPL-3.0-only, with the TownLight Public Institution Exception for qualifying deployments. Docs are CC BY 4.0.

## Placeholder Package Warning

Do not import from CivicCore placeholder packages until CivicCore ships real implementations for them: `audit`, `auth`, `catalog`, `connectors`, `exemptions`, `ingest`, `notifications`, `onboarding`, `scaffold`, `search`, `verification`.

## Milestone Rule

Work one milestone at a time. When a milestone is done, report what changed, audit it once, fix findings once, re-audit once, then continue immediately unless there is a true blocker.
