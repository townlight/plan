# Townlight Planning

Current state: **0.3.0+dev.0 P1/P2 development foundation**. This is unreleased
source-administration work, not an installed public beta. Townlight Planning uses
the hash-pinned Townlight Core v1.2.1 release wheel. The previous v1.0.0 release
was published in error; published v0.2.2 remains a corrective demotion state and
is preserved with its original tag and assets.

P1/P2 adds explicit additive migrations and staff-verified local source bundles
for comprehensive, small-area, transportation, parks and sustainability plans.
Original documents and SHA256 hashes, goal/objective/policy structure, source and
adoption dates, adoption evidence, visibility, revisions and chained audit events
are durable. Corrections append a new revision; they never overwrite evidence.

This does not make official planning determinations. Cited staff analysis,
connected Zoning/Meetings/Records workflows, an operational desktop UI and a
Planning installer profile remain P3-P6 work. The signed Townlight 1.4 installer
is unchanged and does not enable Planning.

## Development and source administration

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
$env:CIVICPLAN_POLICY_DB_URL = "postgresql+psycopg2://USER:PASSWORD@127.0.0.1:PORT/DATABASE"
# Back up the intended database before migration; never use a production DSN for tests.
python -m civicplan.migrations
# Set CIVICPLAN_STAFF_API_KEY through the existing trusted local configuration.
python -m uvicorn civicplan.main:app --host 127.0.0.1 --port 8040
```

The migration command only owns Planning's schema and preserves legacy policies
and analyses. Import handlers require migrations already applied; they do not
initialize schemas or load samples. PostgreSQL is the municipal runtime;
SQLite is supported for isolated development tests.

- `POST /api/v1/civicplan/source-imports`: import a complete local bundle and an
  optional `expected_previous_revision` for amendments/corrections.
- `GET /api/v1/civicplan/source-plans/{plan_id}/history`: revision and audit history.
- `GET /api/v1/civicplan/source-revisions/{revision_id}`: versioned policy/source metadata.
- `GET /api/v1/civicplan/source-revisions/{revision_id}/documents/{document_id}`:
  download exact original bytes with a SHA256 header.

All source-administration routes require both `X-CivicPlan-Role: staff` and a
matching `X-CivicPlan-Staff-Key`. This is the existing trusted-service boundary,
not individual municipal identity. Audits record `trusted-staff-key` as the
service actor and retain the supplied reviewer label separately. P5 must reuse
native authenticated identity; browser clients must never receive this key.

Public foundation lookup/navigation includes only adopted, effective, explicitly
public municipal policies. Private, pending, future and demo records are not
current public policy. Exact policy-ID lookup has no sample fallback. Broader
question interpretation and conflict review remain P3 work.

Metadata-only `/policies/ingest` is retained as an actionable transition response;
it cannot create an apparently adopted municipal policy without original files.
Legacy staff analyses remain readable behind the existing staff gate. Municipal
analysis/export/Meetings/Zoning context stubs return actionable unavailable
responses until implemented. Sample helpers are available only when explicitly
setting `CIVICPLAN_DEMO_MODE=1` with no database configured. `/civicplan` remains
an explicitly labeled static sample page.

See [the source-bundle contract and P1/P2 evidence](docs/PLANNING-P1-P2.md) and
[the operator manual](USER-MANUAL.md). No signing, publication or historical
release modification is part of P1/P2.

## Verification

```powershell
# Point this only at a disposable Planning test database.
$env:PLANNING_TEST_DATABASE_URL = "postgresql+psycopg2://USER:PASSWORD@127.0.0.1:PORT/TEST_DATABASE"
python -m pytest -q
bash scripts/verify-release.sh
```

The required `verify` job supplies PostgreSQL and runs the full gate. The source
and wheel must retain the Planning migration files. A green foundation gate does
not prove installed Planning acceptance.

## License

Code: AGPL-3.0-only, with the TownLight Public Institution Exception for qualifying
deployments. See LICENSE and LICENSE-EXCEPTION.md. Documentation: CC BY 4.0.
