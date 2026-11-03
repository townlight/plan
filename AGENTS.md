<a id="townlight_planning-agent-contract"></a>

# Townlight Planning Agent Contract

## Governing contract and candidate identity

Scott's bounded completion contract governs. Legacy skills, automatic delegation,
milestone/review loops and generic extra gates require explicit invocation.
Preserve actual product requirements, required CI/release checks, security/data
safeguards and installed acceptance. Reuse unaffected evidence with its limits.

Current distribution: `townlight-planning` 0.4.0.dev2; principal import:
`townlight_planning`. Shared dependency: `townlight-core==1.3.0.dev2`. Use the exact
coordinated source pins and local candidate wheels in the README; never fabricate
renamed historical release URLs. Source tests do not establish installed acceptance
or publication. The original [agent contract](docs/history/pre-naming-2026-11/AGENTS.md)
is retained as history, not current session authorization.

The candidate supports fresh branded databases and fresh profiles only. Preserve
existing data and refuse unmarked legacy initialization; no in-place upgrade or
old import shim is provided. The sole approved old active identifier is
`%LOCALAPPDATA%\CivicSuite` for that profile path only. Other retained old active
identifiers require Scott's approval in the single exception registry. Preserve
historical identities, third-party attribution and standalone CivicCast.

## Source Of Truth

- Upstream suite spec: `townlight/townlight/docs/TownlightUnifiedSpec.md`, especially the Townlight Planning catalog entry and suite-wide non-negotiables.
- Suite ADRs: `townlight/townlight/docs/architecture/`.
- Townlight Planning supports cited comprehensive-plan, small-area-plan, transportation-plan, parks-plan, and sustainability-plan policy context. It does not replace planners, attorneys, boards, commissions, councils, or permitting systems of record.

## Non-Negotiables

- Townlight Planning never makes zoning, land-use, environmental, legal, entitlement, or elected-body determinations.
- Every material answer must cite the adopted plan source used.
- Staff-analysis drafts must be marked review-required.
- Public-facing warnings must be actionable and explain the fix path.
- Townlight Planning depends on Townlight Core; Townlight Core must never depend on Townlight Planning.
- Townlight Planning may reference Townlight Zoning/Townlight Meetings concepts only through the pinned candidate contracts or deterministic sample data; preserve the documented deployment boundary.
- Code is AGPL-3.0-only. Docs are CC BY 4.0.

## Core dependency boundary

Core auth, audit, catalog, connector, ingestion, exemption, search, scaffold and
verification contracts must be assessed against the pinned implementation.
Historical placeholder ADRs do not establish current absence. Keep the owning
product's dependency-boundary checks; this correction does not add consumers or
authorize importing an unused capability.

## Verification

Run meaningful affected checks and the repository-required release checks.
Report database, Docker and installed-workflow evidence separately; never turn
skips or historical results into current acceptance. Follow the bounded contract
for completion and continuation rather than an automatic audit/re-audit loop.
