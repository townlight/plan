# Planning P1/P2 source foundation

Status: 0.3.0+dev.0 development work; no Planning release or installed acceptance.
Scope: baseline/Core alignment and durable source administration only.

## Baseline and compatibility

Base main: 7911107d04a6918462dac336a61a760c23255cdc.
Historical v0.2.2: f4f15da00ae7f751e12d5434f75a8105ac386fe9.
GitHub reports main four commits ahead and one behind the tag. Inspection of the
tag-only corrective commit shows version/claim repair, not a missing functional
implementation. Those 0.2.2 corrections are represented on main; preserve both
ancestries, all historical releases/assets and the false-v1 retraction.

Core: the published v1.2.1 wheel from townlight/core, SHA256
8dde29408e206048bde63ec14156a8e6329382af4d16b12710d12aa5c27f3f59.
Use its implemented staff-key and persisted-audit primitives. Core never imports
Planning. No shared runtime binaries or signed 1.4 installer inputs are replaced.
The local +dev.0 version distinguishes this source foundation from published
0.2.2 without claiming a public beta. Future release version selection is P6 work.

## Import contract

POST /api/v1/civicplan/source-imports accepts:

```json
{
  "expected_previous_revision": null,
  "bundle": {
    "schema_version": 1,
    "plan_id": "city-comprehensive-plan",
    "title": "Adopted Comprehensive Plan",
    "jurisdiction": "Your municipality",
    "plan_type": "comprehensive",
    "status": "adopted",
    "visibility": "staff",
    "dataset_kind": "municipal",
    "source_date": "2026-01-01",
    "adopted_on": "2026-02-01",
    "effective_on": "2026-03-01",
    "change_note": "Initial staff-verified import",
    "reviewer_label": "Planner of record",
    "documents": [
      {
        "document_id": "plan",
        "filename": "plan.txt",
        "media_type": "text/plain",
        "sha256": "REPLACE_WITH_64_LOWERCASE_HEX_DIGITS",
        "content_base64": "REPLACE_WITH_BASE64_OF_ORIGINAL_FILE"
      }
    ],
    "policies": [
      {
        "policy_id": "H-1",
        "document_id": "plan",
        "goal": "Housing choice",
        "objective": "Access to services",
        "topic_key": "housing",
        "title": "Housing policy",
        "citation": "Comprehensive Plan, H-1",
        "anchor": "page 10, policy H-1",
        "excerpt": "REPLACE_WITH_EXACT_SOURCE_EXCERPT",
        "relevance": "Staff confirm applicability.",
        "staff_verified": true
      }
    ],
    "adoption_evidence": [
      {
        "kind": "manual-record",
        "reference": "Recorded resolution or other adoption evidence",
        "document_id": "plan",
        "note": "Staff verified the adopted source."
      }
    ]
  }
}
```

The example is a template, not a valid ready-to-submit municipal record. Replace
all placeholders and dates with verified source facts. No real municipal content
or implicit fictional dataset is bundled by P1/P2.

Plan/document IDs start with an ASCII letter or digit and contain only ASCII
letters, digits, periods, underscores, colons or hyphens. Document IDs are
stable route identifiers, not filenames or filesystem paths.

Allowed plan types: comprehensive, small-area, transportation, parks,
sustainability. Status: pending/adopted/superseded. Visibility defaults to staff.
Each original file is 1–10,000,000 bytes; up to 20 files and 25,000,000 total
bytes per bundle. Up to 1,000 unique policy IDs. Paths, mismatched file types,
invalid hashes, unresolved references, unverified policies and invalid adoption
metadata are rejected before writing. UTF-8 excerpts must occur in their source;
PDF/DOCX originals are preserved and staff provide verified anchors/excerpts.
No OCR, network retrieval, archive extraction or file execution occurs.

An adopted revision requires adoption/effective dates and evidence. A manual
record is sufficient; minutes, motions or a live Meetings connection are not
mandatory prerequisites. A meeting-reference record is not live verification.
Corrections/amendments submit a complete replacement bundle with the latest
revision ID as expected_previous_revision. Old bytes and citations remain
immutable. Duplicate identical content returns the original revision and does
not move the plan head backward. Stale edits receive 409 and must be reconciled.

## Persistence, migration and permission contracts

Run python -m civicplan.migrations explicitly against a backed-up database.
Planning owns its civicplan_0001 Alembic chain and new source tables in civicplan.
The migration is additive/idempotent and leaves legacy policy/analysis rows
unchanged. Legacy data is not silently certified as adopted, public or current;
reimport with originals/evidence is required. No request implicitly runs DDL for
the new store. Destructive downgrade is unsupported; use verified recovery.

Imports are transactional. PostgreSQL serializes each plan's imports with a
transaction-scoped lock. Revision, source, policy, evidence and audit tables
reject UPDATE/DELETE. The small plan-head pointer is mutable; it cannot rewrite
old evidence. Every revision records the service actor separately from the
supplied reviewer label. Core hash-chain verification and independent bundle
reconstruction verify the stored source bytes, metadata and history.

Current public projection selects effective, adopted, public municipal records.
Pending amendments never replace adopted text; future changes do not apply
early. A superseding evidenced revision removes current applicability while
preserving history. Private/demo versions are excluded. This is not a public
publication/revocation manager or a new legal policy engine.

Source administration requires the existing trusted staff role/key gate. There
is no browser credential, payload actor override or new unauthenticated localhost
admin route. Native individual identity and full product permission integration
remain later work. Staff keys identify services, not people.

## Scope and acceptance

P1: exact main/tag/version distinction, hash-pinned installed Core 1.2.1,
required package gate and explicit development versus release/installer state.
P2: all five types import, exact original-byte/hash readback, structured status
and evidence, pending/adopted/superseded history, idempotence, conflict protection,
rollback, private/demo/future exclusion, database-level immutability, legacy
preservation, PostgreSQL persistence and actual restart readback.

Tests cover these contracts with explicitly fictional fixtures. Required verify
CI supplies PostgreSQL; CI without that database fails instead of silently
skipping PostgreSQL acceptance. Package verification also inspects wheel/sdist
migration inclusion. No independent review, installed beta acceptance or signed
Planning artifact is implied by those tests.

P3 analysis/search depth, P4 product connections, P5 desktop/profile work and P6
installed/signing/publication remain out of scope. Historical releases and the
signed Records/Meetings/Code/Zoning 1.4 beta remain unchanged.
