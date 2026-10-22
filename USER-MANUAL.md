# Townlight Planning operator manual

Current state: **0.3.0+dev.1 P3/P4 development workflows**. The previous v1.0.0 release
was published in error. Published v0.2.2 and its historical evidence are preserved.
This does not make official planning determinations and is not an installed public beta.
The signed Townlight 1.4 installer remains unchanged.

Source and analysis administration use the existing trusted staff service boundary.
This is an unreleased API increment; a native municipal workflow remains P5.

1. Back up the intended database. Configure CIVICPLAN_POLICY_DB_URL for the
   existing local PostgreSQL service and run `python -m civicplan.migrations`.
   Keep credentials out of logs and source files. No source request runs migrations.
2. Prepare a version-1 JSON bundle using the contract in docs/PLANNING-P1-P2.md.
   Include original document bytes as base64 and independently computed SHA256s,
   staff-verified policy excerpts/anchors, source dates and explicit visibility.
3. For adopted plans, record adoption/effective dates and supporting evidence.
   A manually recorded source is valid; meeting minutes are not a mandatory
   prerequisite. A meeting reference is preserved evidence, not a verified live link.
4. Submit it to POST /api/v1/civicplan/source-imports from the trusted staff workflow.
   Include the existing staff role/key headers. Do not put the key into a browser.
5. Read the returned revision and download its original source. Check its hash
   against the file you imported. Inspect the history/audit endpoint.
6. For an amendment or correction, read the latest history and include its revision
   ID as expected_previous_revision. Explain the change. A stale revision returns
   409; refresh and reconcile rather than retrying a blind overwrite.

Each revision preserves its original bytes, policies, adoption state/evidence,
visibility, actor and reviewer label. A repeated identical bundle returns the
same revision without duplicating history or resetting the current revision.
Pending amendments do not replace adopted policy. Future-effective revisions do
not apply early. Supersession is a separate evidenced revision; old citations
remain available in history. A new visibility value applies to that revision;
a later effective staff-only revision also excludes earlier snapshots from the
public provider. Historical bytes remain preserved for authorized staff. Pending
private revisions do not revoke an adopted public revision.

Only explicitly public, effective, adopted municipal policies appear in public
foundation lookup/navigation. Demo records and private/pending versions do not.
No configured database implicitly loads fictional policies. Legacy records are
preserved but require staff reimport with original sources and evidence before
becoming authoritative municipal policies.

PDF and DOCX files are preserved without executing or extracting them. Staff
provide verified excerpts and anchors. UTF-8 text/Markdown excerpts must occur
in their referenced original source. OCR, automatic interpretation and live
vendor imports are deferred. Invalid hashes, paths, references or adoption
metadata are rejected; no partial import is committed.

For explicit isolated sample evaluation only, unset CIVICPLAN_POLICY_DB_URL and
set CIVICPLAN_DEMO_MODE=1. The /civicplan page remains a labeled static sample.
Use POST /analyses to select exact plan/revision/policy IDs and save a model-free
draft. Add supporting/conflicting/uncertain considerations and staff edits. Read
the latest revision, then submit POST /analyses/{id}/revisions with
expected_previous_revision. A reviewed revision requires analysis text, reviewer
label, review date and review notes. These labels are recorded evidence, not
authenticated individual identity.

Select public Meetings/Zoning evidence with POST /connections/search; attach its
source ID, hash and relation in linked_sources. Providers are trusted composition
code, never URLs supplied in a request. No provider means unavailable, not sample
content. Zoning and enforceable Code remain distinct from adopted planning policy.

POST /analyses/{id}/snapshots pins the reviewed revision. Public snapshots require
audience=public plus a separately edited public_summary; private proposal, staff
notes and internal review notes are omitted. GET /snapshots/{id}/export downloads
the actual canonical JSON with X-Content-SHA256. Later edits/amendments preserve
existing snapshots. Current source permissions are checked again on every read
and export. /snapshots/{id}/access-advice uses existing deterministic Access
advice without replacing the original or claiming accessibility certification.

In the explicit development composition, Records staff select the public snapshot
through its existing human-controlled attachment/review/approval/export workflow.
Records rechecks Planning evidence on retrieval, export preparation/completion and
fulfillment. No Planning profile, desktop controls or installer activation is
provided in P3/P4. See docs/PLANNING-P3-P4.md.
No source attachment automatically approves or publishes a municipal decision.
