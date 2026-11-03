  Prepared naming, Access and Notice candidate — 2 November 2026. Build, signing, installed acceptance and publication remain pending. Earlier signed releases and receipts apply only to their identified artifacts.

Townlight Planning

Townlight Beta 1 · Naming candidate; component versions advanced · AGPL-3.0-only

Planning retains adopted policy imports and neighborhood applicability, saved staff analyses, reviewed snapshots, municipal initiatives and amendment history. An analysis or amendment draft does not adopt policy.

Start here

Staff should use the operating manual. Administrators should read first-run, configuration and recovery before changing a deployment. Developers should read the exact API/schema reference and matching source companion. This edition describes the prepared source candidate; obtain its installer only after signing and installed acceptance identify the exact artifact.

- Operating manual · Printable PDF · Editable Word manual
- API and data dictionary · OpenAPI JSON
- Product and suite directory · Terms and full license

Exact version and candidate

  Identity                        Value
  ------------------------------- ------------------------------------------------------
  Documentation                   Townlight Beta 1 naming, Access and Notice candidate
  Intended installer version      1.7.0.1; build and acceptance pending
  Native desktop source version   1.7.0-1
  Product component               townlight-planning 0.4.0.dev2
  Principal import package        townlight_planning
  Candidate hashes                Pending build, signing and installed acceptance
  License                         AGPL-3.0-only

Use a fresh profile and empty database. Existing unmarked city data is refused before initialization; no in-place upgrade is supported. Preserve the existing %LOCALAPPDATA%\CivicSuite profile, data and recovery material. Historical releases retain their original identities.

What staff can do

- Import adopted policy: Open Policy library. Preview jurisdiction, adoption/source dates, policy IDs, neighborhood applicability and originals, then confirm the complete source bundle. Retain the previous revision.
- Create or reopen an analysis: Open Analyses and select the project. Use Next page when the loaded page does not contain the saved work. Enter the proposal, analysis and private staff notes.
- Select policies and evidence: In Policies & evidence select exact policy revisions and applicable neighborhood context. Record supporting, conflicting or uncertain considerations. Select permitted Meetings or Zoning evidence with its expected hash.
- Save and reconcile: Use Save draft before navigating or signing out. When another revision exists, reopen it and reconcile your edits. Do not resubmit against a guessed revision identifier.
- Review the saved revision: In Review & export check the audience, public summary and review notes. Save, then Record review of saved draft. The trusted staff path derives identity/date. Editing later produces a new revision requiring review.
- Create and export a snapshot: Preview the reviewed saved revision, inspect the returned content, then create the snapshot. Public copies exclude staff notes and full staff analysis under the public contract. Export verifies the expected SHA256.
- Track initiatives and amendments: Create and revise municipal initiative status, responsibility, targets, milestones and measurements using the existing controls. Retain history. Draft and review amendments separately; adoption must identify the actual adopted source revision.
- Share deliberately: Select a permitted snapshot in Records. Creating a snapshot does not publish it, release a request or adopt policy.

Operating procedures and examples

The operating manual now includes these existing procedures, with synthetic inputs, readback and limits. Follow the actual app boundary identified there; a standalone source capability is not automatically a desktop screen.

- Exploration initiatives and amendments.
- Explore adopted plans.
- Track a municipal initiative.
- Retain an amendment lifecycle.

Architecture and data

Runtime and storage

This prepared source candidate targets Windows x64 fresh installation. Its native shell uses Rust 2021, Tauri 2 and Microsoft WebView2; browser assets are JavaScript built with Vite 8.1.6. This describes the native desktop frontend; Station has a separate React operator, specified below or in its product manual. Canonical business workflows use bundled CPython 3.13.5, FastAPI, Pydantic, SQLAlchemy and Alembic, with PostgreSQL 17 / PostGIS and managed original files. The prior accepted runtime contained FastAPI 0.162.0; this changed candidate requires its own installed dependency verification. Package minimum Python requirements can differ from the bundled executable; the metadata reference preserves both. No stack rewrite is implied by the beta label.

The native transport is fixed to loopback 127.0.0.1:15480; PostgreSQL uses the configured local runtime port (default 15432). Optional local model service defaults to 127.0.0.1:15434. Those are deployment defaults, not internet endpoints. The runtime has health, module and readiness endpoints; readiness is stronger than process existence. The task queue is the existing local Core task infrastructure, not an assertion that a separate Redis service is required for this desktop composition.

The default native profile is %LOCALAPPDATA%\CivicSuite; the historical directory name remains part of compatibility. Do not rename it to Townlight. A configured TOWNLIGHT_PROFILE_ROOT must be absolute. Local configuration and secrets live under that profile; protected managed files and database state must be backed up coherently. Source/runtime identity is distinct from a product’s display label.

Data and consistency

Plan bundles and revisions; original documents; versioned policy selections and neighborhood applicability; analysis revisions; reviews and snapshots; initiatives, milestones and measurements; amendment revisions.

Versioned saves use expected prior revision identifiers where defined. Reopen and reconcile on conflict. Exact exports and handoffs use source IDs, current visibility, revision and SHA256. Review belongs to the saved revision and does not transfer silently to edited text. Database changes use the owning product’s migrations; a request or readiness check is not an authorization to mutate schema.

Capacity and platform statements

This beta has synthetic single-profile workflow evidence. It does not have a published benchmark for concurrent staff capacity, minimum RAM/CPU, large-source limits or a field SLA. Do not turn a developer machine’s specification into a supported minimum. The new installer size remains pending its build; allow additional disk for extracted runtime, database, originals, exports, media and backups. Select equipment/storage after sizing those actual workloads.

The exact runtime payload lock records pinned files, sizes and hashes. The component metadata records shipped dependency declarations. These references are more precise than a manually copied dependency list. Third-party and historical license notices must accompany their matching payloads.

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Data contract                       Description
  ----------------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Input                               Complete adopted policy source bundles, proposal context, versioned policy selections, permitted Meetings/Zoning evidence and staff progress updates.

  Retained records                    Plan bundles and revisions; original documents; versioned policy selections and neighborhood applicability; analysis revisions; reviews and snapshots; initiatives, milestones and measurements; amendment revisions.

  Output                              Cited analyses, audience-specific reviewed snapshots, durable initiative/history records and amendment lifecycle records.

  Connections                         Selects Meetings and Zoning evidence. Provides permitted reviewed snapshots to Records. Source selection is permission- and hash-checked and is not automatic writeback.
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Setup and operation

1.  Obtain the identified signed private candidate and its corresponding-source companion from the beta coordinator. The landing pages in this documentation are not an installer download service.
2.  On the intended fresh Windows test installation, verify the MSI hash and publisher signature before installing. Preserve unrelated profiles and recovery material. Installed acceptance for this source candidate remains pending; no in-place legacy upgrade is supported.
3.  Launch Townlight under the intended named Windows account. Choose the storage folders. Select Townlight Inspections candidate (inspections-preview) for the bounded desktop composition, including Access and Notice. A narrower default selection will not expose all workspaces.
4.  Enter the city profile, time zone and contacts. Create the first named local administrator, sign in and choose protected backup storage. Continue without local AI is valid for the deterministic workflows.
5.  Run Health Check and wait for readiness. Open Townlight. In System Health select Finish Records Migration to activate the canonical Python/PostgreSQL runtime. Do not fabricate migration receipts or seed accounts.
6.  Create named staff through Settings. Import authorized sources using each product’s source library. All examples in this package are synthetic; they are not municipal authority.
7.  Provision Station separately if it is part of the beta exercise. Selecting the desktop composition does not start or configure Station. Configure vision explicitly only if automatic photo drafting is selected.

Configuration

Native deployment configuration

Use Setup, Settings and System Health for supported staff operation. Administrators provision folders, backup storage, named accounts and the city profile. Select inspections-preview for the bounded desktop composition, including Access and Notice. Station remains a separate service boundary. Do not use a standalone product’s demo server as a substitute for the installed workspace.

Technical deployments use TOWNLIGHT_PRODUCT_PROFILE, TOWNLIGHT_PROFILE_ROOT, DATABASE_URL, TOWNLIGHT_RUNTIME_PORT, PORTAL_MODE and the runtime-managed secret files. Treat database URLs and native session proofs as secrets. The installed native domain runtime explicitly refuses non-loopback binding. PORTAL_MODE=private is the accepted posture; changing it does not by itself commission an internet portal, authentication provider or reverse proxy.

The isolated documentation exporter sets a fictional profile and unusable synthetic database origin only to read schemas; those values are not deployment configuration. Keep deployment values in the intended process/account scope. An already-running process does not automatically inherit later environment edits.

API usage

Native command example

The following JavaScript belongs in the existing trusted Townlight frontend/development environment with invoke imported from @tauri-apps/api/core. It is not a command for an arbitrary web page or an instruction for nontechnical staff. IDs must come from records created in an isolated synthetic exercise.

    import { invoke } from '@tauri-apps/api/core';
    const result = await invoke('planning_domain_request', {request: {operation: 'sources', offset: 0}});
    console.log(result);

Trusted local HTTP example

An administrator/developer can inspect an already-configured isolated runtime from a trusted local process. This PowerShell example reads the signed-in synthetic profile’s existing proof into memory; it does not create a user, seed a session, reveal the proof in output or bypass a permission check. Do not use real city data in development examples. A read response does not prove approval or publication.

    $profilePath = Join-Path $env:LOCALAPPDATA 'CivicSuite'
    $sessionPath = Join-Path $profilePath 'config\local-session.json'
    $session = Get-Content -LiteralPath $sessionPath -Raw | ConvertFrom-Json
    $headers = @{ 'X-Townlight-Session' = $session.session_hash }
    Invoke-RestMethod -Uri 'http://127.0.0.1:15480/desktop/v1/planning/sources' -Headers $headers
    Remove-Variable session, headers

Complete synthetic source bundle

The synthetic Planning bundle is the retained fixture used by the beta staff exercise. It includes the complete supported source envelope rather than a shortened pseudo-payload. Keep its fictional source labels. For Planning, wrap it as {"bundle": BUNDLE, "expected_previous_revision": null}; for Permitting use {"bundle": BUNDLE, "expected_revision": null}. Code and Zoning take their own complete import envelopes. Replace null with the current expected revision when revising an existing source, as the applicable schema requires. These are import examples, not legal authority or permission to load them into a live city profile.

A synthetic write with subsequent readback

This example demonstrates the existing Meetings HTTP contract in an isolated exercise. It is intentionally fictional. It does not start a service. Its authentication setup is included so it can be run independently under the signed-in synthetic account. If a write times out, inspect current records before repeating it.

    $profilePath = Join-Path $env:LOCALAPPDATA 'CivicSuite'
    $sessionPath = Join-Path $profilePath 'config/local-session.json'
    $session = Get-Content -LiteralPath $sessionPath -Raw | ConvertFrom-Json
    $headers = @{ 'X-Townlight-Session' = $session.session_hash }
    $body = @{
      title = 'Synthetic documentation exercise'
      scheduled_start = '2026-11-05T18:00:00-07:00'
      location = 'Synthetic room'
      meeting_type = 'regular'
    } | ConvertTo-Json
    $meeting = Invoke-RestMethod -Method Post `
      -Uri 'http://127.0.0.1:15480/desktop/v1/meetings/meetings' `
      -Headers $headers -ContentType 'application/json' -Body $body
    Invoke-RestMethod `
      -Uri ('http://127.0.0.1:15480/desktop/v1/meetings/meetings/' + $meeting.id) `
      -Headers $headers
    Remove-Variable session, headers

This write requires Meetings to be enabled and the signed-in staff role to permit it. It is a cross-suite integration example; for this product’s request models, use the complete technical reference below.

MCP status

No direct product MCP server is exposed by the accepted Townlight desktop or Station boundary. Do not configure an invented townlight mcp command or assume an AI client has staff permissions. The integration surfaces for this beta are native IPC, the documented HTTP APIs, source bundle imports, exact exports and the existing Station CLI.

The bundled transcription code includes a TextFlowKit MCP adapter as a separate source capability. It offers job-based transcribe_media, get_transcript, list_jobs, get_job_status and export_transcript, and additional tools declared in that adapter. It uses stdio first and optional Streamable HTTP, with the MCP SDK as an optional extra. It is not automatically launched, authenticated as Townlight staff or accepted as a Townlight product MCP deployment. This documentation does not add such a service.

For a transcription client already provisioned separately, an illustrative tool call is:

    {"name":"get_job_status","arguments":{"job_id":"synthetic-existing-job-id"}}

Use a job ID returned by that transcription service. This example does not create a Townlight record or bypass its review/Records handoff. The exact optional adapter tool signatures are supplied in the MCP source reference. Station meeting capture does not become live speech recognition because this optional donor adapter exists.

Verification and known limits

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Product                 Recorded result         Precisely exercised
  ----------------------- ----------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Planning                PASS                    Adopted source import with neighborhood, saved/reviewed analysis and snapshot, persisted initiative/history and draft amendment, public explorer neighborhood readback and native workspace.

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

These results come from the identified signed candidate’s fresh normal-profile Sandbox exercise: real native IPC/HTTP/PostgreSQL and selected headless controls. All accounts, source bundles and media were synthetic. The guest install/uninstall and recovery passed, and the owned Sandbox stopped. No host installed application or standalone CivicCast was changed. This documentation task reuses those receipts; it does not claim a new software acceptance run.

The workflow matrix identifies raw receipt filenames. The evidence index retains their original hashes; raw receipts remain in the private beta handoff rather than being silently republished with the documentation site.

The limits remain: actual city field acceptance and equipment/network commissioning; Station automatic provisioning/SCM commissioning; every UI/role combination; field recognition accuracy; and historical in-place upgrades are not certified. They are not five invented feature requirements. Fresh-install controlled beta handoff remains the accepted scope. This package makes no city-deployment, publication or general-availability claim.

Existing initiative/amendment persistence is included. A draft amendment does not change an adopted source revision. Historical standalone sample pages are not the installed staff workspace. Analysis lists and project filters operate on loaded pages; use pagination to reach additional records.

Development and repository map

Use the corresponding source for the candidate rather than assuming the public default branch matches it. The source companion contains installed-owned-source, product build inputs, desktop Rust/browser sources, locks and BUILD.md. It excludes credentials and third-party binary/model payloads. Use the recorded runtime lock when reproducing packaging.

Relevant source contracts:

- townlight_planning/source_bundle.py
- townlight_planning/workflow_models.py
- townlight_planning/workflow_store.py
- townlight_planning/municipal.py
- townlight_runtime/planning_bridge.py

The desktop package defines npm run build, npm test, npm run test:browser and its Tauri command. Python products retain their own pyproject.toml, tests and migrations; use the matching checkout’s declared dependencies and test configuration. Do not run a sample server against a production profile. This documentation build validates documentation only and reuses the separately identified installed acceptance; it does not claim a new complete application CI run.

Recovery and support

Save work and use Core’s canonical Backup Now before maintenance. That operation stops writers. Preserve the coherent profile/database/document backup and its receipt, then use Start to resume. A source export is not a full backup.

Use Restore Latest Backup through the supported controls. If the result says Restore needs service start, use Start, then Check, and reopen a known record. Do not repeat restore merely because services need to start. The fresh-profile acceptance verified that a fulfilled request survived restore and a post-backup marker did not.

Keep Station’s dedicated database and media evidence together in its own backup. Core’s native-profile backup must not be assumed to include an external Station data directory. Stop writers during a coordinated backup. Preserve failed media attempts and logs.

On failure, record the time, selected composition, component/installer versions and exact message. Check System Health for stopped, starting, ready or failed dependencies. Use the existing Retry control after readiness; do not create duplicate business records to refresh a stale view. Share only a redacted diagnostic bundle. Preserve secrets, original evidence, recovery material and unrelated installations.

Prepared package installation

The renamed distributions are not yet published on a package index. Use the matching verified candidate wheel directory, not a renamed historical release URL. Installation of these Python packages is a developer/package check; the signed Windows MSI and its installed acceptance remain separate.

In a new Windows virtual environment, replace the example wheel-directory path with the directory accompanying this candidate and verify its SHA256 manifest:

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    $candidateWheels = (Resolve-Path 'C:\path\to\candidate-wheels').Path
    python -m pip install (Join-Path $candidateWheels 'townlight_core-1.3.0.dev2-py3-none-any.whl')
    python -m pip install (Join-Path $candidateWheels 'townlight_planning-0.4.0.dev2-py3-none-any.whl')
    python -c "import townlight_planning; from importlib.metadata import version; print(version('townlight-planning'))"

Expected principal import: townlight_planning; expected distribution version: 0.4.0.dev2. Use a fresh empty database/profile for workflow testing. Existing city data and the previous release remain untouched; no in-place upgrade or old-import compatibility shim is supplied.

License and responsible use

Current owned code is AGPL-3.0-only. Preserve full license, matching corresponding source, dependency notices and historical grants. Terms of use do not remove license rights. Source imports do not confer permission to publish third-party material. Review all automatic drafts and use the separate owning-product decision before official action. CivicCast remains independent.

Earlier documentation

Previous editions are retained under docs/history/pre-townlight-beta-1/. They describe their original software and license grants. Use the current Townlight Beta 1 manual for this candidate.
