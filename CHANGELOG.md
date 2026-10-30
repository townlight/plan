Townlight Beta 1 source component: **0.4.0.dev1**, paired with Core **1.3.0.dev1**. Use the signed suite MSI and current manual for beta installation; earlier entries below retain their original scope.

# Changelog

## [0.3.0] - Unreleased staff beta preparation

- Assign a distinct bundled package identity to the opt-in Townlight Planning
  desktop 1.5.0-beta.1 preparation. This is not a module publication or a stable
  public-readiness claim. Core remains hash-pinned to 1.2.1.
- P5 native integration and P6 unsigned installer acceptance provide supporting
  evidence. Final signed-byte acceptance and delivery remain pending. The desktop
  interface and explicit static sample are unchanged.
- Preserve every historical release, source record, compatibility identifier and
  the signed Townlight 1.4 installer. No signing, tags or publication in this step.

## [0.3.0+dev.1] - Unreleased

- P3: one versioned policy service for navigation, deterministic cited lookup, questions, cross-plan context and consistency review; durable editable staff-analysis revisions with source pins, considerations and recorded review.
- P4: permission-checked injected Meetings/Zoning providers, immutable reviewed snapshots with actual evidence and source hashes, public-summary selection, Records provider contract and existing Access advice.
- Additive workflow migration preserves P1/P2 and legacy evidence. Native identity/UI/profile activation remains P5; signing/publication remains P6. Historical releases and signed 1.4 installer unchanged.

## [0.3.0+dev.0] - Unreleased

- P1/P2 source foundation: Core 1.2.1 hash-pinned compatibility, explicit Planning migrations, original source bundles, immutable revisions, adoption evidence, visibility and Core hash-chained audit.
- Preserve legacy policies/analyses without automatically promoting them or loading sample policies. Municipal analysis/context/export stubs remain unavailable until P3/P4.
- No installer, signing or publication. Historical releases and signed Townlight 1.4 remain unchanged.

## [0.2.2] - 2026-05-23

- Narrow truth-repair release. No functional upgrade.
- Exists solely to supersede the false v1.0.0 release from 2026-05-21 in
  GitHub's Latest impression.
- CivicCore pin unchanged.

## [1.0.0] - 2026-05-21

### Changed

- Promoted CivicPlan from the demoted recovery label to a v1.0.0 public-use module release candidate.
- Synchronized package, runtime, docs, tests, and release verifier surfaces around CivicCore v1.1.0.
- Preserved the planning-safety boundary: CivicPlan provides cited planning support and staff-analysis context, not official planning determinations, legal advice, live vendor calls by default, permitting write-back, or elected-body decisions.

## [0.2.0] - 2026-05-11

### Changed

- feat(deps): bump civiccore pin to v1.1.0 and use shared `staff_key_gate` for timing-safe persisted staff-analysis auth.

## [0.2.0] - 2026-05-10

- Demoted the false v1.0.0 release label after the external CivicSuite audit found this module is a recovery/foundation module, not a canonical spec-complete v1 product.
- Preserved the useful recovery work while resetting the public package version to 0.2.0.
- Kept the CivicCore v1.0.0 wheel dependency and pinned it with SHA256 for release integrity.
- Supersedes the prior public v1.0.0 posture; do not treat v1.0.0 as production-ready or spec-complete.

All notable changes to CivicPlan will be documented in this file.

The format follows Keep a Changelog, and this project follows Semantic Versioning.

## [Unreleased]

## [0.2.1] - 2026-05-21

### Corrected

- Corrected the false v1.0.0 release label after the independent CivicSuite release-integrity audit found CivicPlan does not meet the Section 2 FINISHED and SHIPPING bar.
- Set the honest current label to v0.2.1 and superseded the mistaken v1.0.0 posture without deleting the historical record.
- Current classification: deterministic scaffold; no real AI layer, full frontend, real municipal data/search, migrations, or public-use gate.
- CivicPlan must not be described as finished, shipping, city-ready, product-ready, or public-use ready until a future independent audit signs off against the full Section 2 gate.

## [1.0.0] - 2026-05-07

### Recovery note

- The `1.0.0` label was checked through the suite release-recovery pass with a
  fresh local release gate and live browser QA. Treat the original release date
  as historical; the recovery evidence is recorded in
  `docs/release-recovery-status.md`.

### Added

- Staff-only local plan-policy ingestion through configured `CIVICPLAN_POLICY_DB_URL`.
- Goal/objective/policy navigator, cited plan Q&A, cross-plan synthesis, amendment history, and progress-target evidence APIs.
- CivicClerk staff-report context contract and local adversarial integration mocks for CivicZone, CivicClerk, GeoJSON area boundaries, and plan document import fixtures.
- Public UI copy for v1 navigator/progress/staff-analysis boundaries.

### Changed

- Published CivicPlan release surfaces at `1.0.0`; the later suite
  release-recovery pass records fresh verification evidence.
- Updated product/docs boundaries to avoid official determinations, legal advice, and live external-call claims.

## [0.1.2] - 2026-05-07

### Added

- Production-depth policy persistence slice with `CIVICPLAN_POLICY_DB_URL`, persisted plan-policy records, persisted staff-analysis outlines, and retrieval by `analysis_id`.
- CivicZone-facing `POST /api/v1/civicplan/context/zoning` contract that returns cited, review-required plan-policy context without making zoning determinations.
- Staff-role gate for persisted staff-analysis create/read routes when policy persistence is configured.

### Changed

- Aligned CivicPlan's release gate, CI install path, docs, and health-contract test with the published CivicCore v1.0.0 wheel before the CivicZone policy-context contract sprint.
- Updated public UI copy to v0.1.2 and removed static no-op/editable controls from the sample lookup.
- Documented the CivicCore v1.0 wheel prerequisite for clean local installs.

## [0.1.1] - 2026-04-28

### Changed

- Aligned CivicPlan to `civiccore==0.3.0` while preserving the v0.1 planning policy foundation behavior.
- Updated release gates, CI wheel install, docs, tests, and browser-visible version copy for the v0.1.1 compatibility release.

## [0.1.0] - 2026-04-27

### Added

- Professional repository scaffold, documentation, issue templates, PR template, and release gates.
- FastAPI runtime foundation with root, health, and public UI endpoints.
- Deterministic cited plan-policy lookup helper.
- Policy-consistency support helper with planner-review boundary.
- Staff-analysis outline helper with citations and human-review requirement.
- Records-ready plan-policy export checklist.
- Accessible public sample UI at `/civicplan` with browser QA coverage.
