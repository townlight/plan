# Private municipal-workflow candidate 0.4.0.dev1

This candidate pairs with private Core1.3.0.dev1. It adds persistent implementation initiatives and amendment lifecycle tracking. It is not installed, signed, published or accepted by a city. Existing historical release receipts are preserved.

## Staff workflow

In the Planning policy library, search adopted sources. Select Track implementation or Propose amendment on the exact cited policy. An initiative records its responsible staff/team, target and unit, due date, milestones, measurements and update reason. Measurements remain in saved history; a correction is new evidence. A saved initiative moves from planned to active and then completed or cancelled. Completed milestones require evidence; completion needs a measurement. Units cannot change after measurements exist.

An amendment starts as a draft, goes into review, and can then be linked to a later retained adopted revision of the same plan or withdrawn. Import the actual adopted source through source administration first. Saving an amendment never changes adopted policy text, issues an entitlement or publishes material. Closed lifecycles are read-only. History shows saved revisions and authenticated actor IDs. In the native bridge those are mapped individual SQL users; direct service-key API calls identify only the trusted service.

The Implementation & amendments tab lists saved work with pagination. Stale revisions return409 and retain edits for reconciliation. Missing sources, bad transitions and incomplete evidence are refused. PostgreSQL stores append-only hashed revisions. New schema0003 must be applied explicitly; requests never create tables. Original source/history/export behavior remains separately governed.

The progress/targets and amendments/history routes now return staff-only municipal workflow data instead of demo targets or source-import history. Existing source history remains under source-plans routes and the native source-history action. This is an intentional API change; clients must pair with this candidate. Public city dashboards are not yet implemented. Required institutional approval and legal policy are not inferred from entered labels.

## Evidence and limits

Actual PostgreSQL migration/lifecycle tests passed. Real native HTTP plus headless Chromium passed policy selection, initiative measurement, amendment review/adoption, role denial, SQL actor attribution, restart persistence and desktop/mobile layout. Browser acceptance used a test-only invoke-to-HTTP adapter; native Rust route tests compiled and passed separately. This is not installed Tauri or city-device acceptance. Existing Planning suite had80 passes and2 intentional database-environment skips; two integration failures were corrected and passed separately. Current metadata and municipal checks then passed11 tests.

Private candidate code is AGPL-3.0-only. Historical exception grants remain in docs/licensing/history. Public CI and installer pins still reference published baselines and require coordinated candidate/release handling before publication; no public-release CI success is claimed. No full P1 beta-city completion claim: public surfaces, external city connectors, accessibility/field acceptance and broader policy/Records journeys remain open.
