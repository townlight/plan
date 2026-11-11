Windows x64 Beta 1 · MSI 1.8.1.1

Windows 1.8.1.1 adds shared meeting imports for 31 source families, with 34 supported source/format pairs. Installed Windows Sandbox checks exercised preview, save and durable readback using public captures and fixtures, plus the documented Townlight handoffs. These checks do not establish automatic discovery on every live portal or a complete retest of every module.

- <a href="https://townlight.github.io/manuals/planning.html#townlight-planning-manual" id="toc-townlight-planning-manual">Townlight Planning Manual</a>
  - <a href="https://townlight.github.io/manuals/planning.html#contents" id="toc-contents">Contents</a>
  - <a href="https://townlight.github.io/manuals/planning.html#using-this-manual" id="toc-using-this-manual">Using this manual</a>
  - <a href="https://townlight.github.io/manuals/planning.html#beta-identity" id="toc-beta-identity">Beta identity</a>
  - <a href="https://townlight.github.io/manuals/planning.html#first-run" id="toc-first-run">First run</a>
  - <a href="https://townlight.github.io/manuals/planning.html#daily-workflow" id="toc-daily-workflow">Daily workflow</a>
  - <a href="https://townlight.github.io/manuals/planning.html#connected-workflows" id="toc-connected-workflows">Connected workflows</a>
  - <a href="https://townlight.github.io/manuals/planning.html#architecture" id="toc-architecture">Architecture</a>
  - <a href="https://townlight.github.io/manuals/planning.html#exploration-initiatives-and-amendments" id="toc-exploration-initiatives-and-amendments">Exploration initiatives and amendments</a>
  - <a href="https://townlight.github.io/manuals/planning.html#technical-specifications" id="toc-technical-specifications">Technical specifications</a>
  - <a href="https://townlight.github.io/manuals/planning.html#configuration-and-administration" id="toc-configuration-and-administration">Configuration and administration</a>
  - <a href="https://townlight.github.io/manuals/planning.html#api-and-integration-examples" id="toc-api-and-integration-examples">API and integration examples</a>
  - <a href="https://townlight.github.io/manuals/planning.html#mcp-and-automation-boundary" id="toc-mcp-and-automation-boundary">MCP and automation boundary</a>
  - <a href="https://townlight.github.io/manuals/planning.html#security-and-permissions" id="toc-security-and-permissions">Security and permissions</a>
  - <a href="https://townlight.github.io/manuals/planning.html#backup-recovery-and-maintenance" id="toc-backup-recovery-and-maintenance">Backup recovery and maintenance</a>
  - <a href="https://townlight.github.io/manuals/planning.html#troubleshooting" id="toc-troubleshooting">Troubleshooting</a>
  - <a href="https://townlight.github.io/manuals/planning.html#verified-workflows-and-limits" id="toc-verified-workflows-and-limits">Verified workflows and limits</a>
  - <a href="https://townlight.github.io/manuals/planning.html#terms-of-service-and-license" id="toc-terms-of-service-and-license">Terms of service and license</a>
  - <a href="https://townlight.github.io/manuals/planning.html#glossary" id="toc-glossary">Glossary</a>
  - <a href="https://townlight.github.io/manuals/planning.html#alphabetical-subject-index" id="toc-alphabetical-subject-index">Alphabetical subject index</a>
  - <a href="https://townlight.github.io/manuals/planning.html#source-and-document-control" id="toc-source-and-document-control">Source and document control</a>

# Townlight Planning Manual

## Shared meeting imports · Windows 1.8.1.1

Windows 1.8.1.1 adds shared meeting imports for 31 source families, with 34 supported source/format pairs. Installed Windows Sandbox checks exercised preview, save and durable readback using public captures and fixtures, plus the documented Townlight handoffs. These checks do not establish automatic discovery on every live portal or a complete retest of every module.

[All 31 sources, formats and handoffs](https://townlight.github.io/manuals/meeting-imports.html) · [Installed acceptance](https://github.com/townlight/townlight/releases/download/townlight-windows-v1.8.1.1/ACCEPTANCE-Windows-1.8.1.1.md).

Windows 1.8.1.1 has fresh-install acceptance. An in-place upgrade to 1.8.1.1 was not exercised. The previous Windows 1.8.0.1 release tested upgrade from 1.7.2.1; that result applies to 1.8.0.1. Before an existing-city evaluation, back up city data and settings, close Townlight, keep the existing %LOCALAPPDATA%\CivicSuite profile, and use the same Windows account. Keep the prior installer and a restore path. Station continues to use its separately configured service.

The accepted MSI contains Townlight Runtime 0.3.1 and Meetings 1.0.6 distributions. Its health version strings still report Runtime 0.3.0 and Meetings 1.0.5. Default-branch source corrects those display strings; the signed MSI and its exact build source remain unchanged.


**Townlight Beta 1** · Naming candidate documentation edition 2 November 2026

## Contents

- [Using this manual](https://townlight.github.io/manuals/planning.html#using-this-manual)
- [Beta identity](https://townlight.github.io/manuals/planning.html#beta-identity)
- [First run](https://townlight.github.io/manuals/planning.html#first-run)
- [Daily workflow](https://townlight.github.io/manuals/planning.html#daily-workflow)
- [Connected workflows](https://townlight.github.io/manuals/planning.html#connected-workflows)
- [Architecture](https://townlight.github.io/manuals/planning.html#architecture)
- [Exploration initiatives and amendments](https://townlight.github.io/manuals/planning.html#exploration-initiatives-and-amendments)
- [Technical specifications](https://townlight.github.io/manuals/planning.html#technical-specifications)
- [Configuration and administration](https://townlight.github.io/manuals/planning.html#configuration-and-administration)
- [API and integration examples](https://townlight.github.io/manuals/planning.html#api-and-integration-examples)
- [MCP and automation boundary](https://townlight.github.io/manuals/planning.html#mcp-and-automation-boundary)
- [Security and permissions](https://townlight.github.io/manuals/planning.html#security-and-permissions)
- [Backup recovery and maintenance](https://townlight.github.io/manuals/planning.html#backup-recovery-and-maintenance)
- [Troubleshooting](https://townlight.github.io/manuals/planning.html#troubleshooting)
- [Verified workflows and limits](https://townlight.github.io/manuals/planning.html#verified-workflows-and-limits)
- [Terms of service and license](https://townlight.github.io/manuals/planning.html#terms-of-service-and-license)
- [Glossary](https://townlight.github.io/manuals/planning.html#glossary)
- [Alphabetical subject index](https://townlight.github.io/manuals/planning.html#alphabetical-subject-index)
- [Source and document control](https://townlight.github.io/manuals/planning.html#source-and-document-control)

## Using this manual

Townlight Planning helps planning staff, municipal policy reviewers and authorized administrators. Planning retains adopted policy imports and neighborhood applicability, saved staff analyses, reviewed snapshots, municipal initiatives and amendment history. An analysis or amendment draft does not adopt policy.

Staff should begin with First run and Daily workflow. Administrators should also read Architecture, Technical specifications, Configuration, Security and Recovery. Developers should use the exact API/data dictionary and examples. The table of contents and alphabetical subject index link to the relevant sections in the HTML edition; the PDF preserves headings and searchable text. An editable Word edition is included with the same documentation companion.

## Beta identity

| Identity | Value |
|----|----|
| Documentation | Townlight Beta 1 naming, Access and Notice candidate |
| Windows MSI version | 1.8.1.1 |
| Product component | townlight-planning 0.4.0.dev2 |
| Principal import package | townlight_planning |
| Native desktop source version | 1.8.1-1 |
| Candidate hashes | [SHA-256 checksums](https://github.com/townlight/townlight/releases/download/townlight-windows-v1.8.1.1/SHA256SUMS-Windows-1.8.1.1.txt) and [Windows acceptance summary](https://github.com/townlight/townlight/releases/download/townlight-windows-v1.8.1.1/ACCEPTANCE-Windows-1.8.1.1.md) |
| Current owned software license | AGPL-3.0-only |
| Acceptance composition | Windows x64 fresh install and upgrade from 1.7.2.1. Select the full profile. Station uses separate configuration. |

Start a new installation with an empty database and fresh Windows profile. For an upgrade from Windows 1.7.2.1, keep the existing profile. The approved profile path is `%LOCALAPPDATA%\CivicSuite`. Keep existing profiles and backups.

## First run

Windows 1.8.1.1 has fresh-install acceptance. An in-place upgrade to 1.8.1.1 was not exercised. The previous Windows 1.8.0.1 release tested upgrade from 1.7.2.1; that result applies to 1.8.0.1. Before an existing-city evaluation, back up city data and settings, close Townlight, keep the existing %LOCALAPPDATA%\CivicSuite profile, and use the same Windows account. Keep the prior installer and a restore path. Station continues to use its separately configured service.

### Fresh installation

Run the signed Windows 1.8.1.1 MSI and use an empty database and a new Townlight profile for first run.

1.  Download the signed MSI, matching source companion and checksums from the [public Windows release](https://github.com/townlight/townlight/releases/tag/townlight-windows-v1.8.1.1).
2.  Verify the MSI hash and Authenticode publisher before installation. See the [Windows acceptance summary](https://github.com/townlight/townlight/releases/download/townlight-windows-v1.8.1.1/ACCEPTANCE-Windows-1.8.1.1.md) for the tested setup.
3.  Launch Townlight under the intended named Windows account. Choose the storage folders. Select **Townlight Inspections candidate** (`inspections-preview`) for the bounded desktop composition, including Access and Notice. A narrower default selection will not expose all workspaces.
4.  Enter the city profile, time zone and contacts. Create the first named local administrator, sign in and choose protected backup storage. **Continue without local AI** is valid for the deterministic workflows.
5.  Run Health Check and wait for readiness. Open Townlight. In System Health select **Finish Records Migration** to activate the canonical Python/PostgreSQL runtime. Do not fabricate migration receipts or seed accounts.
6.  Create named staff through Settings. Import authorized sources using each product’s source library. All examples in this package are synthetic; they are not municipal authority.
7.  Provision Station separately if it is part of the beta exercise. Selecting the desktop composition does not start or configure Station. Configure vision explicitly only if automatic photo drafting is selected.

## Daily workflow

<span id="workflow-1"></span>

### 1. Import adopted policy

Open Policy library. Preview jurisdiction, adoption/source dates, policy IDs, neighborhood applicability and originals, then confirm the complete source bundle. Retain the previous revision.

<span id="workflow-2"></span>

### 2. Create or reopen an analysis

Open Analyses and select the project. Use Next page when the loaded page does not contain the saved work. Enter the proposal, analysis and private staff notes.

<span id="workflow-3"></span>

### 3. Select policies and evidence

In Policies & evidence select exact policy revisions and applicable neighborhood context. Record supporting, conflicting or uncertain considerations. Select permitted Meetings or Zoning evidence with its expected hash.

<span id="workflow-4"></span>

### 4. Save and reconcile

Use Save draft before navigating or signing out. When another revision exists, reopen it and reconcile your edits. Do not resubmit against a guessed revision identifier.

<span id="workflow-5"></span>

### 5. Review the saved revision

In Review & export check the audience, public summary and review notes. Save, then Record review of saved draft. The trusted staff path derives identity/date. Editing later produces a new revision requiring review.

<span id="workflow-6"></span>

### 6. Create and export a snapshot

Preview the reviewed saved revision, inspect the returned content, then create the snapshot. Public copies exclude staff notes and full staff analysis under the public contract. Export verifies the expected SHA256.

<span id="workflow-7"></span>

### 7. Track initiatives and amendments

Create and revise municipal initiative status, responsibility, targets, milestones and measurements using the existing controls. Retain history. Draft and review amendments separately; adoption must identify the actual adopted source revision.

<span id="workflow-8"></span>

### 8. Share deliberately

Select a permitted snapshot in Records. Creating a snapshot does not publish it, release a request or adopt policy.

### Working safely

Use your own named account and save before leaving a screen. A saved draft is durable; unsaved form text may not be. If a write has an unknown result, reopen its record before repeating it.

Read source jurisdiction, dates, citation, version and visibility. A copied source hash identifies exact bytes, not their legal applicability. If a source changes or permission is removed, resolve the source problem rather than substituting stale cached content.

Keep originals and derivatives separate. Review the intended audience before export. A public summary excludes private fields only through the applicable copy contract and your review. A renamed private packet is still private content.

Drafting, review, approval, attachment, export, fulfillment and publication are separate operations. A Townlight workpaper does not itself adopt law, issue a permit, impose a fine or release a records response. The responsible staff member records the applicable decision.

## Connected workflows

Selects Meetings and Zoning evidence. Provides permitted reviewed snapshots to Records. Source selection is permission- and hash-checked and is not automatic writeback.

| Direction | Material |
|----|----|
| Input | Complete adopted policy source bundles, proposal context, versioned policy selections, permitted Meetings/Zoning evidence and staff progress updates. |
| Output | Cited analyses, audience-specific reviewed snapshots, durable initiative/history records and amendment lifecycle records. |

### Product boundary

Existing initiative/amendment persistence is included. A draft amendment does not change an adopted source revision. Historical standalone sample pages are not the installed staff workspace. Analysis lists and project filters operate on loaded pages; use pagination to reach additional records.

## Architecture

<figure>
<img src="https://townlight.github.io/assets/planning-architecture.svg" alt="Townlight Planning architecture and evidence flow" />
<figcaption aria-hidden="true">Townlight Planning architecture and evidence flow</figcaption>
</figure>

The drawing shows the principal staff/evidence path. Native commands carry trusted identity to Python business services; PostgreSQL and retained original files hold durable state. A downstream copy does not silently transfer decision authority. Station has its own configured authority/media boundary, database and mutable files. The connected-workflow text supplies the drawing’s reading order and accessibility alternative.

## Exploration initiatives and amendments

### Explore adopted plans

Open **Policy library** and find **Explore adopted plans**. Enter a topic and/or choose the supplied goal, neighborhood and plan-type filters. These are separate facets; keyword search is not a substitute for neighborhood applicability. Run exploration and inspect each returned plan, adopted/source dates, exact policy references and permitted original material. Empty results can mean no matching permitted adopted source, not an error or an invented plan.

The existing public exploration transport is `planning_public_request`, separate from staff `planning_domain_request`. Technical clients use its documented `plan-explore` operation or the mounted public route in the API companion. A native operation fragment is:

``` json
{"operation":"plan-explore","payload":{"topic":"synthetic mobility","neighborhood":"Synthetic North","goal":"","plan_type":""}}
```

Only public-permitted adopted sources belong in this result. Private staff analyses, selected restricted evidence and staff notes do not become public through exploration. The output includes matching plans/facets and an informational disclaimer; no cross-plan AI synthesis or internet portal commissioning is implied.

### Track a municipal initiative

Open **Implementation & amendments**. Choose an actual retained policy selection, title, responsible staff, target, unit, due date and explanatory note. Save a planned/active initiative and reopen its current revision/history. Add milestones and measurements with their dates and evidence. Each change uses the latest `expected_revision`; reconcile a conflict by reopening the current state rather than guessing a revision.

The initiative statuses are `planned`, `active`, `completed` and `cancelled`. A completed initiative requires measurement evidence and every supplied milestone completed. A milestone completion needs supporting evidence and a completion date that is not in the future. Numerical progress without its source/evidence is not a completed municipal outcome.

For a synthetic exercise, create an active initiative with a fictional policy selection, target `3`, unit `synthetic reviews`, an intended future due date and a note explaining the test. Add one evidence-backed measurement, then complete each milestone before requesting completed status. Read the saved initiative/history after every accepted revision. No external project system is updated by this save.

### Retain an amendment lifecycle

An amendment has its own proposal and history; changing an analysis does not adopt an amendment. In **Implementation & amendments**, select the actual policy, enter proposal text, title, responsible staff and a note, then save `draft`. The allowed amendment statuses are `draft`, `review`, `adopted` and `withdrawn`.

Moving to `review` or `adopted` requires a recorded `review_note`. Before recording `adopted`, import and verify the actual adopted policy revision, then supply its `adoption_revision` identity. Only an adopted amendment may carry that field; draft/review/withdrawn records must omit it or use null. The proposal’s existing policy reference and newly imported adoption revision have distinct roles. Staff record the authorized decision; a status choice does not itself enact policy.

Use the latest `expected_revision` when revising. Reopen the amendment and municipal history, confirm status, review note and adoption link, and retain prior revisions. Public exploration changes only when its permitted adopted sources actually change, not merely because staff created a proposal.

Source contracts: `townlight_planning/public_explore.py`, `municipal.py`, `townlight_runtime/planning_bridge.py` and the Planning view. The API dictionary carries `InitiativeInput`, `Milestone`, `Measurement`, `AmendmentInput` and the exact policy-selection fields; conditional completion/adoption checks above also apply beyond simple field validation.

## Technical specifications

### Runtime and storage

The accepted package supports Windows x64 fresh installation and upgrade from 1.7.2.1. Its native shell uses **Rust 2021, Tauri 2 and Microsoft WebView2**; browser assets are JavaScript built with **Vite 8.1.6**. This describes the native desktop frontend; Station has a separate React operator, specified below or in its product manual. Canonical business workflows use bundled **CPython 3.13.5, FastAPI, Pydantic, SQLAlchemy and Alembic**, with **PostgreSQL 17 / PostGIS** and managed original files. The installed runtime tested here contains FastAPI 0.162.0. Package minimum Python requirements can differ from the bundled executable; the metadata reference preserves both. No stack rewrite is implied by the beta label.

The native transport is fixed to loopback `127.0.0.1:15480`; PostgreSQL uses the configured local runtime port (default `15432`). Optional local model service defaults to `127.0.0.1:15434`. Those are deployment defaults, not internet endpoints. The runtime has health, module and readiness endpoints; readiness is stronger than process existence. The task queue is the existing local Core task infrastructure, not an assertion that a separate Redis service is required for this desktop composition.

The default native profile is `%LOCALAPPDATA%\CivicSuite`; the historical directory name remains part of compatibility. Do not rename it to Townlight. A configured `TOWNLIGHT_PROFILE_ROOT` must be absolute. Local configuration and secrets live under that profile; protected managed files and database state must be backed up coherently. Source/runtime identity is distinct from a product’s display label.

### Data and consistency

Plan bundles and revisions; original documents; versioned policy selections and neighborhood applicability; analysis revisions; reviews and snapshots; initiatives, milestones and measurements; amendment revisions.

Versioned saves use expected prior revision identifiers where defined. Reopen and reconcile on conflict. Exact exports and handoffs use source IDs, current visibility, revision and SHA256. Review belongs to the saved revision and does not transfer silently to edited text. Database changes use the owning product’s migrations; a request or readiness check is not an authorization to mutate schema.

### Capacity and platform statements

This beta has synthetic single-profile workflow evidence. It does not have a published benchmark for concurrent staff capacity, minimum RAM/CPU, large-source limits or a field SLA. Do not turn a developer machine’s specification into a supported minimum. The signed MSI is 2,081,316,864 bytes; allow additional disk for extracted runtime, database, originals, exports, media and backups. Select equipment/storage after sizing those actual workloads.

The exact [runtime payload lock](https://townlight.github.io/reference/runtime-payload-lock.json) records pinned files, sizes and hashes. The [component metadata](https://townlight.github.io/reference/component-metadata.json) records shipped dependency declarations. These references are more precise than a manually copied dependency list. Third-party and historical license notices must accompany their matching payloads.

## Configuration and administration

### Native deployment configuration

Use Setup, Settings and System Health for supported staff operation. Administrators provision folders, backup storage, named accounts and the city profile. Select `inspections-preview` for the bounded desktop composition, including Access and Notice. Station remains a separate service boundary. Do not use a standalone product’s demo server as a substitute for the installed workspace.

Technical deployments use `TOWNLIGHT_PRODUCT_PROFILE`, `TOWNLIGHT_PROFILE_ROOT`, `DATABASE_URL`, `TOWNLIGHT_RUNTIME_PORT`, `PORTAL_MODE` and the runtime-managed secret files. Treat database URLs and native session proofs as secrets. The installed native domain runtime explicitly refuses non-loopback binding. `PORTAL_MODE=private` is the accepted posture; changing it does not by itself commission an internet portal, authentication provider or reverse proxy.

The isolated documentation exporter sets a fictional profile and unusable synthetic database origin only to read schemas; those values are not deployment configuration. Keep deployment values in the intended process/account scope. An already-running process does not automatically inherit later environment edits.

## API and integration examples

### Native command example

The following JavaScript belongs in the existing trusted Townlight frontend/development environment with `invoke` imported from `@tauri-apps/api/core`. It is not a command for an arbitrary web page or an instruction for nontechnical staff. IDs must come from records created in an isolated synthetic exercise.

``` javascript
import { invoke } from '@tauri-apps/api/core';
const result = await invoke('planning_domain_request', {request: {operation: 'sources', offset: 0}});
console.log(result);
```

### Trusted local HTTP example

An administrator/developer can inspect an already-configured isolated runtime from a trusted local process. This PowerShell example reads the signed-in synthetic profile’s existing proof into memory; it does not create a user, seed a session, reveal the proof in output or bypass a permission check. Do not use real city data in development examples. A read response does not prove approval or publication.

``` powershell
$profilePath = Join-Path $env:LOCALAPPDATA 'CivicSuite'
$sessionPath = Join-Path $profilePath 'config\local-session.json'
$session = Get-Content -LiteralPath $sessionPath -Raw | ConvertFrom-Json
$headers = @{ 'X-Townlight-Session' = $session.session_hash }
Invoke-RestMethod -Uri 'http://127.0.0.1:15480/desktop/v1/planning/sources' -Headers $headers
Remove-Variable session, headers
```

### Complete synthetic source bundle

The [synthetic Planning bundle](https://townlight.github.io/reference/examples/synthetic-plan-bundle.json) is the retained fixture used by the beta staff exercise. It includes the complete supported source envelope rather than a shortened pseudo-payload. Keep its fictional source labels. For Planning, wrap it as `{"bundle": BUNDLE, "expected_previous_revision": null}`; for Permitting use `{"bundle": BUNDLE, "expected_revision": null}`. Code and Zoning take their own complete import envelopes. Replace null with the current expected revision when revising an existing source, as the applicable schema requires. These are import examples, not legal authority or permission to load them into a live city profile.

### A synthetic write with subsequent readback

This example demonstrates the existing Meetings HTTP contract in an isolated exercise. It is intentionally fictional. It does not start a service. Its authentication setup is included so it can be run independently under the signed-in synthetic account. If a write times out, inspect current records before repeating it.

``` powershell
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
```

This write requires Meetings to be enabled and the signed-in staff role to permit it. It is a cross-suite integration example; for this product’s request models, use the complete technical reference below.

### Complete technical contract

Read the [Planning API reference](https://townlight.github.io/api/planning.html) for every documented operation, request field, constraint, response declaration and source supplement. Download the [OpenAPI JSON](https://townlight.github.io/api/planning-openapi.json) for tools. For Station this is the suite-side schema only; its separate service contract is documented in the API supplement. The [reference directory](https://townlight.github.io/reference/index.html) includes configuration/source inventories, dependency declarations, native command contracts, MCP signatures and candidate evidence.

## MCP and automation boundary

No direct product MCP server is exposed by the accepted Townlight desktop or Station boundary. Do not configure an invented `townlight mcp` command or assume an AI client has staff permissions. The integration surfaces for this beta are native IPC, the documented HTTP APIs, source bundle imports, exact exports and the existing Station CLI.

The bundled transcription code includes a **TextFlowKit MCP adapter** as a separate source capability. It offers job-based `transcribe_media`, `get_transcript`, `list_jobs`, `get_job_status` and `export_transcript`, and additional tools declared in that adapter. It uses stdio first and optional Streamable HTTP, with the MCP SDK as an optional extra. It is not automatically launched, authenticated as Townlight staff or accepted as a Townlight product MCP deployment. This documentation does not add such a service.

For a transcription client already provisioned separately, an illustrative tool call is:

``` json
{"name":"get_job_status","arguments":{"job_id":"synthetic-existing-job-id"}}
```

Use a job ID returned by that transcription service. This example does not create a Townlight record or bypass its review/Records handoff. The exact optional adapter tool signatures are supplied in the [MCP source reference](https://townlight.github.io/reference/mcp.html). Station meeting capture does not become live speech recognition because this optional donor adapter exists.

## Security and permissions

Use your own named account and save before leaving a screen. A saved draft is durable; unsaved form text may not be. If a write has an unknown result, reopen its record before repeating it.

Read source jurisdiction, dates, citation, version and visibility. A copied source hash identifies exact bytes, not their legal applicability. If a source changes or permission is removed, resolve the source problem rather than substituting stale cached content.

Keep originals and derivatives separate. Review the intended audience before export. A public summary excludes private fields only through the applicable copy contract and your review. A renamed private packet is still private content.

Drafting, review, approval, attachment, export, fulfillment and publication are separate operations. A Townlight workpaper does not itself adopt law, issue a permit, impose a fine or release a records response. The responsible staff member records the applicable decision.

The native session is validated and mapped to a persisted SQL identity. An editable actor/reviewer label is not authentication. Product/module permissions and source visibility apply at the server boundary. Revoked/unavailable authority fails closed for new Station operations; a previous permission result is not a perpetual authorization.

Use protected local folders, account permissions and credential storage. Never include the native session file, database passwords, provider keys or unredacted support bundles in a public issue or generated public documentation. A local public view is not automatically a secured internet deployment. Keep network exposure and real equipment acceptance specific to the chosen beta site.

## Backup recovery and maintenance

Save work and use Core’s canonical **Backup Now** before maintenance. That operation stops writers. Preserve the coherent profile/database/document backup and its receipt, then use **Start** to resume. A source export is not a full backup.

Use **Restore Latest Backup** through the supported controls. If the result says **Restore needs service start**, use **Start**, then **Check**, and reopen a known record. Do not repeat restore merely because services need to start. The [Windows 1.6.0.1 Beta 1 fresh-install acceptance](https://github.com/townlight/townlight/releases/tag/townlight-beta-1) verified that a fulfilled request survived restore and a post-backup marker did not.

Keep Station’s dedicated database and media evidence together in its own backup. Core’s native-profile backup must not be assumed to include an external Station data directory. Stop writers during a coordinated backup. Preserve failed media attempts and logs.

On failure, record the time, selected composition, component/installer versions and exact message. Check System Health for stopped, starting, ready or failed dependencies. Use the existing Retry control after readiness; do not create duplicate business records to refresh a stale view. Share only a redacted diagnostic bundle. Preserve secrets, original evidence, recovery material and unrelated installations.

## Troubleshooting

| Symptom | Likely meaning | Next action |
|----|----|----|
| Workspace absent | Wrong product composition or unavailable canonical runtime. | Check selected composition; activate through Finish Records Migration; wait for readiness. |
| Cannot sign in / 401 | Missing or expired named account session. | Sign in normally; reopen a Station launch ticket if applicable. |
| Permission denied / 403 | Account, module, source or browser-origin permission. | Ask the authorized administrator to inspect the intended permission; do not invent role headers. |
| Save conflict / 409 | The saved revision, expected source hash or lifecycle changed. | Keep edits, reopen current state and reconcile deliberately. |
| Invalid input / 422 | Required field, format, geometry, source envelope or state is invalid. | Read the field detail and correct the input/source; preserve originals. |
| Service unavailable / 503 | Database, schema, connected source or configuration unavailable. | Inspect System Health and the named dependency. Preserve work; retry only after readiness. |
| Export refused | Missing exact review, approval, audience or source authorization. | Read the refusal and complete the owning product’s explicit decision. |
| Restore needs service start | The snapshot was restored but services have not resumed. | Use Start, then Check and verify a saved record; do not blindly repeat restore. |

## Verified workflows and limits

The table records selected synthetic workflows from the original [Windows 1.6.0.1 Beta 1](https://github.com/townlight/townlight/releases/tag/townlight-beta-1) Sandbox run. Station’s later delivery has [separate Windows 1.6.0.1 acceptance](https://github.com/townlight/townlight/releases/tag/townlight-beta-1-station-delivery). See the [Windows 1.8.0.1 acceptance summary](https://github.com/townlight/townlight/releases/download/townlight-windows-v1.8.0.1/ACCEPTANCE-Windows-1.8.0.1.md) for the workflows and upgrade path exercised on the previous 1.8.0.1 MSI.

| Product | Recorded result | Precisely exercised |
|----|----|----|
| Planning | PASS | Adopted source import with neighborhood, saved/reviewed analysis and snapshot, persisted initiative/history and draft amendment, public explorer neighborhood readback and native workspace. |

The Windows 1.8.0.1 acceptance covers the tested installation paths and selected synthetic workflows, including Boards & Commissions, Contracts, and Procurement. Earlier results apply to their original builds. City field acceptance, physical equipment and network commissioning, Station automatic provisioning, and comprehensive UI and role coverage remain outside the 1.8.0.1 checks.

## Terms of service and license

### Scope and status

These terms describe the Townlight Beta 1 software and this documentation package. This public Windows beta is for evaluation. No uptime commitment, support response time, indemnity, data-processing agreement or paid service is created by these documents. A separate signed agreement, if any, governs services it actually provides.

### Software license and rights

Current Townlight-owned distributions identified in this candidate use **AGPL-3.0-only**. The full license is supplied with this documentation and with the source companion. The license governs rights to run, copy, modify and convey the covered software; these operational terms do not add restrictions to those rights. Historical grants and dependency licenses retain their own terms. CivicCast remains a separate product and is not relicensed by this documentation work.

When conveying covered software, retain applicable notices and provide the corresponding source and installation/build information required by the license. For a modified version supporting remote network interaction, follow section 13’s source-offer requirement. The companion archive identifies the source for this candidate; a link to a different public branch is not a substitute for the matching source. Read the supplied license for the complete conditions. See the [GNU license reference](https://www.gnu.org/licenses/agpl-3.0.html) and [GNU licensing FAQ](https://www.gnu.org/licenses/gpl-faq.en.html).

### Data ownership and access

Importing a document does not transfer its ownership or grant permission to publish it. The operating organization controls its accounts, access decisions, lawful source use, retention and review/release policy. Keep resident information, credentials, private notes and restricted evidence in their authorized locations. Documentation examples contain fictional data. No real city account, credential or record is required to exercise these examples in an isolated test environment.

### Local operation and external processors

The accepted beta workflow is local and uses named staff accounts. Station has separate storage and credentials. Configure backup destinations and optional model/network providers deliberately. A configured external provider may receive submitted prompts, images or audio according to that configuration and provider’s terms; this documentation does not promise that every optional configuration is offline. An email outbox or local public view does not establish external delivery or an internet deployment. This static documentation site has no analytics, account collection or remote font dependency.

### Staff decisions and source applicability

Staff verify the jurisdiction, source currency, permissions, citations and proposed audience. Model output and generated guidance require review. No draft is automatically an official legal interpretation, zoning determination, permit approval, fee assessment, enforcement notice or records-release decision. Official permit fee authority remains with the adopted source and responsible organization; imported amounts do not become a new authoritative calculation.

### Beta operation and recovery

Windows 1.8.0.1 was tested for fresh installation and in-place upgrade from 1.7.2.1. Upgrade paths from versions older than 1.7.2.1 are unverified. Station uses its separately configured service. Keep backups and original evidence. Test your physical equipment and network and service configuration before relying on them. See the [acceptance summary](https://github.com/townlight/townlight/releases/download/townlight-windows-v1.8.0.1/ACCEPTANCE-Windows-1.8.0.1.md) for the tested paths.

### Warranty and liability

The covered software’s warranty and liability conditions are those in sections 15–17 of the supplied AGPL and any applicable separate written undertaking. This documentation creates no additional warranty or limitation beyond those terms. Third-party software is subject to its retained license notices. Nothing here removes rights that applicable law makes nonwaivable.

### Support and incident reporting

Use the project’s existing SUPPORT and SECURITY guidance for its matching repository. Report reproducible behavior with the version, operation and redacted logs. Do not put credentials, resident records or unredacted evidence in a public issue. Coordinate sensitive reports through the channel designated in SECURITY. No new support address or service commitment is invented here.

### Ending a beta exercise and document changes

When an organization ends testing, it controls retention/export and removes access according to its policy. Uninstall may retain data; back up and inspect the selected removal options. Ending an exercise does not revoke rights already granted by AGPL. Later software/documentation versions must identify their changed candidate and scope; historical receipts retain their original identities. These terms do not claim that a city has accepted a contract merely by reading a manual.

## Glossary

| Term | Meaning |
|----|----|
| Approval | An explicit authorized decision on the saved text/artifact. It is separate from saving or attachment. |
| Canonical record | The owning product’s retained identity and saved version, rather than an editable copied label. |
| Composition | The selected set of desktop modules; inspections-preview exposes the eight staff products. |
| Corresponding source | The source/build material matching the delivered covered program, subject to its license. |
| Derivative / Records copy | A separately prepared document with its own intended audience and hash. |
| Hash / SHA256 | A fingerprint of exact bytes. It detects change; it does not establish legal authority. |
| Idempotency | Repeating the same identified request has the same intended effect; changing its payload can be refused. |
| IPC | The native desktop command boundary between its browser interface and Rust host. |
| MCP | Model Context Protocol; no direct Townlight product server is enabled by this beta. |
| Original | Retained source bytes. A reviewed derivative does not replace them. |
| Provenance | Source, version, date, actor and relationship information retained with evidence. |
| Revision | An immutable saved version. Later edits do not inherit an earlier review automatically. |
| Snapshot | A fixed audience-specific copy tied to a source/reviewed revision. |
| Station | Townlight’s separate media boundary using a pinned CivicCast-derived engine; standalone CivicCast remains separate. |

## Alphabetical subject index

- **Accounts and authentication** — [Security and permissions](https://townlight.github.io/manuals/planning.html#security-and-permissions).
- **AGPL and source** — [Terms of service and license](https://townlight.github.io/manuals/planning.html#terms-of-service-and-license).
- **API contracts** — [API and integration examples](https://townlight.github.io/manuals/planning.html#api-and-integration-examples).
- **Architecture** — [Architecture](https://townlight.github.io/manuals/planning.html#architecture).
- **Backup** — [Backup recovery and maintenance](https://townlight.github.io/manuals/planning.html#backup-recovery-and-maintenance).
- **Beta version** — [Beta identity](https://townlight.github.io/manuals/planning.html#beta-identity).
- **Configuration** — [Configuration and administration](https://townlight.github.io/manuals/planning.html#configuration-and-administration).
- **Evidence and acceptance** — [Verified workflows and limits](https://townlight.github.io/manuals/planning.html#verified-workflows-and-limits).
- **Fees and official decisions** — [Terms of service and license](https://townlight.github.io/manuals/planning.html#terms-of-service-and-license).
- **First run** — [First run](https://townlight.github.io/manuals/planning.html#first-run).
- **Handoffs and audience** — [Connected workflows](https://townlight.github.io/manuals/planning.html#connected-workflows).
- **MCP** — [MCP and automation boundary](https://townlight.github.io/manuals/planning.html#mcp-and-automation-boundary).
- **Originals and provenance** — [Security and permissions](https://townlight.github.io/manuals/planning.html#security-and-permissions).
- **Recovery** — [Backup recovery and maintenance](https://townlight.github.io/manuals/planning.html#backup-recovery-and-maintenance).
- **Staff procedures** — [Daily workflow](https://townlight.github.io/manuals/planning.html#daily-workflow).
- **Station configuration** — [Configuration and administration](https://townlight.github.io/manuals/planning.html#configuration-and-administration).
- **Technical stack** — [Technical specifications](https://townlight.github.io/manuals/planning.html#technical-specifications).
- **Troubleshooting** — [Troubleshooting](https://townlight.github.io/manuals/planning.html#troubleshooting).

### Operating subject links

- **Exploration initiatives and amendments** — [Exploration initiatives and amendments](https://townlight.github.io/manuals/planning.html#exploration-initiatives-and-amendments).
- **Explore adopted plans** — [Explore adopted plans](https://townlight.github.io/manuals/planning.html#explore-adopted-plans).
- **Retain an amendment lifecycle** — [Retain an amendment lifecycle](https://townlight.github.io/manuals/planning.html#retain-an-amendment-lifecycle).
- **Track a municipal initiative** — [Track a municipal initiative](https://townlight.github.io/manuals/planning.html#track-a-municipal-initiative).

## Source and document control

This edition is authored from the immutable corresponding-source companion, the generated installed-domain schema and the retained workflow receipts. The current software versions and signed artifacts are unchanged. Public historical pages are not synchronized or published by this local documentation task.

### Workflow subject index

- **Create and export a snapshot** — [Daily workflow, step 6](https://townlight.github.io/manuals/planning.html#workflow-6).

- **Create or reopen an analysis** — [Daily workflow, step 2](https://townlight.github.io/manuals/planning.html#workflow-2).

- **Import adopted policy** — [Daily workflow, step 1](https://townlight.github.io/manuals/planning.html#workflow-1).

- **Review the saved revision** — [Daily workflow, step 5](https://townlight.github.io/manuals/planning.html#workflow-5).

- **Save and reconcile** — [Daily workflow, step 4](https://townlight.github.io/manuals/planning.html#workflow-4).

- **Select policies and evidence** — [Daily workflow, step 3](https://townlight.github.io/manuals/planning.html#workflow-3).

- **Share deliberately** — [Daily workflow, step 8](https://townlight.github.io/manuals/planning.html#workflow-8).

- **Track initiatives and amendments** — [Daily workflow, step 7](https://townlight.github.io/manuals/planning.html#workflow-7).

- [Source inventory and file hashes](https://townlight.github.io/reference/source-inventory.json)

- [All component metadata](https://townlight.github.io/reference/component-metadata.json)

- [Installed domain OpenAPI](https://townlight.github.io/reference/desktop-domain-openapi.json)

- [Workflow matrix](https://townlight.github.io/reference/workflow-matrix.json)

- [Full AGPL text](https://townlight.github.io/reference/AGPL-3.0.txt)


## Source package installation

Use locally built wheels from the exact component sources in the corresponding-source companion and verify their hashes. Do not relabel historical release assets. Installation of these Python packages is a developer/package check;
the signed Windows MSI and its installed acceptance remain separate.

In a new Windows virtual environment, replace the example wheel-directory path
with your locally built wheel directory from the matching pinned source and verify its SHA256 manifest:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
$candidateWheels = (Resolve-Path 'C:\path\to\candidate-wheels').Path
python -m pip install (Join-Path $candidateWheels 'townlight_core-1.3.0.dev2-py3-none-any.whl')
python -m pip install (Join-Path $candidateWheels 'townlight_planning-0.4.0.dev2-py3-none-any.whl')
python -c "import townlight_planning; from importlib.metadata import version; print(version('townlight-planning'))"
```

Expected principal import: `townlight_planning`; expected distribution version:
`0.4.0.dev2`. For standalone component workflow testing, use a fresh empty database and profile. These component commands do not perform a Windows MSI upgrade. See First run for the supported Windows upgrade.

## License and responsible use

Current owned code is AGPL-3.0-only. Preserve full license, matching corresponding source, dependency notices and historical grants. Terms of use do not remove license rights. Source imports do not confer permission to publish third-party material. Review all automatic drafts and use the separate owning-product decision before official action. CivicCast remains independent.

## Earlier documentation

Previous editions are retained under `docs/history/pre-townlight-beta-1/`. They describe their original software and license grants. Use the current Townlight Beta 1 manual for this candidate.
