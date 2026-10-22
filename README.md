Opt-in staff beta preparation: **0.3.0** for the Townlight desktop
1.5.0-beta.1 composition. This package identity is prepared and unreleased;
no module release, signed installer or public download is created here. P5/P6
provide native and unsigned installed evidence; final signed-byte acceptance
remains pending. The desktop interface and explicit static sample are unchanged.
Historical v0.2.2 and all other release assets remain preserved.

# Townlight Planning

The opt-in native development integration is described in
[Planning P5](docs/PLANNING-P5.md). Historical releases and installer identity remain unchanged.

Historical development baseline: **0.3.0+dev.1 P3/P4 development workflows**. This is unreleased
source and analysis work, not an installed public beta. Townlight Planning uses
the hash-pinned Townlight Core v1.2.1 release wheel. The previous v1.0.0 release
was published in error; published v0.2.2 remains a corrective demotion state and
is preserved with its original tag and assets.

P1/P2 adds explicit additive migrations and staff-verified local source bundles
for comprehensive, small-area, transportation, parks and sustainability plans.
Original documents and SHA256 hashes, goal/objective/policy structure, source and
adoption dates, adoption evidence, visibility, revisions and chained audit events
are durable. Corrections append a new revision; they never overwrite evidence.

P3 adds a shared versioned policy service and editable, source-pinned staff
analysis revisions. P4 adds reviewed immutable snapshots and permission-checked
Meetings/Zoning providers, a Records source contract and existing Access advice.
This does not make official planning determinations. Native identity, operational
desktop UI and Planning profile activation remain P5; installed acceptance, signing
and publication remain P6. The signed Townlight 1.4 installer
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
current public policy. Deterministic lookup, questions, cross-plan synthesis and
consistency review use these same versioned sources. Unsupported queries return
no supported policy; overlapping excerpts create a staff review task. No model is
required. Source dates, locations, anchors and hashes accompany policy excerpts.

Metadata-only `/policies/ingest` is retained as an actionable transition response;
it cannot create an apparently adopted municipal policy without original files.
Legacy staff analyses remain readable behind the existing staff gate. Municipal
analysis has append-only edits, considerations and reviewer/date records; reviewed
snapshots export actual policy/evidence bytes. Connected evidence is selected
through trusted runtime providers and rechecked on read/export. Links grant no access. Sample helpers are available only when explicitly
setting `CIVICPLAN_DEMO_MODE=1` with no database configured. `/civicplan` remains
an explicitly labeled static sample page.

See [the source-bundle contract and P1/P2 evidence](docs/PLANNING-P1-P2.md) and
[the operator manual](USER-MANUAL.md). No signing, publication or historical
release modification is part of P3/P4. See [the P3/P4 workflow contract](docs/PLANNING-P3-P4.md) for API composition and scope.

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
