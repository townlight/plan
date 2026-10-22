# Planning P3/P4 development workflows — 0.3.0+dev.1

This increment retains P1/P2 original sources and adds migration civicplan_0002.
Back up the database and run `python -m civicplan.migrations` explicitly. Neither
requests nor provider composition runs migrations or seeds municipal policy.

All municipal policy consumers use PolicyService: navigation, exact/topic lookup,
question answering, cross-plan synthesis, consistency and linked product context.
The service selects effective adopted revisions; private policies require staff
auth. Each excerpt identifies its plan, revision, policy, dates, original document
hash and location/anchor. An unsupported question has no fabricated answer.
Differing matching excerpts produce a review task rather than an automatic finding.
This deterministic workflow needs no model or network provider.

## Staff review API

All paths below are under `/api/v1/civicplan`. Staff operations require both
existing role/key headers; the key identifies a trusted service, not a person.
Native individual authentication and desktop integration remain P5.

- `POST /analyses`: project_name, proposal, selected_policies with exact plan_id,
  revision_id and policy_id. Optional considerations name a selected policy and
  supporting/conflicting/uncertain stance. analysis_text and staff_notes are editable.
- `POST /analyses/{id}/revisions`: the same data plus expected_previous_revision.
  A stale update returns 409; saved revisions and Core audit events are append-only.
- `GET /analyses/{id}` and `/history`: persisted revisions and verified audit history.
- `review_state=reviewed` requires staff analysis text, reviewer_label, reviewed_on
  and review_notes. Labels and dates record review evidence; they do not grant roles.
- `POST /analyses/{id}/snapshots`: expected_revision and visibility, default staff_only.
  Public snapshots require audience=public plus a separately edited public_summary.
  The public representation omits private proposal, staff notes, considerations and
  review notes. It includes the selected public explanation, source excerpts/hashes,
  linked public evidence, reviewer/date and informational disclaimer.
- `GET /snapshots/{id}` and `/export`: immutable canonical JSON and SHA256.
  `POST /snapshots/{id}/access-advice` retains those bytes and applies existing Access
  deterministic advice, marked review-required. It is not accessibility certification.

## Trusted connections

Composition code injects `planning_providers` (meetings and zoning callables) and
`planning_access_rewrite` into the Planning app. `POST /connections/search` accepts
provider name and query, never caller URLs/code. linked_sources contains provider,
source_id, expected_sha256 and relation (adoption-evidence, hearing, context or
precedent). A link never proves adoption by itself and grants no additional access.

The paired Townlight runtime's `planning_connections.configure` explicitly composes
the existing Meetings/Zoning public source providers, existing Access rewrite, and
Planning public snapshots. All required modules must be enabled by trusted test or
future profile configuration. Existing profiles are unchanged; this function does
not activate Planning or introduce a planning-beta installer profile.

Meetings supplies its public archive contract. Zoning supplies its immutable cited
question snapshots and rechecks its linked Meetings evidence and Code citations.
Planning policy is advisory adopted policy; Zoning context and enforceable Code
remain distinct. Closed-session evidence, private analyses and restricted policy
sources are not selectable as public snapshots. Provider failure or revocation
blocks read/export; cached text is never substituted. Historical snapshot bytes
remain in the database, even when public retrieval is no longer permitted.

The paired Records extension adds authenticated `/desktop/v1/planning-sources/search`
and `/desktop/v1/requests/{id}/planning-sources`. Explicit staff selection attaches
exact public snapshot bytes and provenance through canonical Records file evidence.
The existing review, release-copy, approval, export and fulfillment controls apply.
Records rechecks the source on retrieval and export preparation/completion and
fulfillment; missing providers fail closed. Attachment never publishes anything.

## Scope and evidence

Tests use explicitly fictional municipal fixtures. API/SQL acceptance does not
prove an installed desktop journey. P5 remains native identity, desktop controls
and profile activation; P6 remains installed acceptance, signing and publication.
Historical Planning releases and signed Townlight 1.4 assets/tags are preserved.
No signature, new tag or release publication belongs to this source increment.
