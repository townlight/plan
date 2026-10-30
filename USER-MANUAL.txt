# Townlight Planning Manual

**Townlight Beta 1** · Documentation edition 30 October 2026

## Contents

- [Using this manual](#using-this-manual)
- [Beta identity](#beta-identity)
- [First run](#first-run)
- [Daily workflow](#daily-workflow)
- [Connected workflows](#connected-workflows)
- [Architecture](#architecture)
- [Exploration initiatives and amendments](#exploration-initiatives-and-amendments)
- [Technical specifications](#technical-specifications)
- [Configuration and administration](#configuration-and-administration)
- [API and integration examples](#api-and-integration-examples)
- [MCP and automation boundary](#mcp-and-automation-boundary)
- [Security and permissions](#security-and-permissions)
- [Backup recovery and maintenance](#backup-recovery-and-maintenance)
- [Troubleshooting](#troubleshooting)
- [Verified workflows and limits](#verified-workflows-and-limits)
- [Terms of service and license](#terms-of-service-and-license)
- [Glossary](#glossary)
- [Alphabetical subject index](#alphabetical-subject-index)
- [Source and document control](#source-and-document-control)

## Using this manual

Townlight Planning helps planning staff, municipal policy reviewers and authorized administrators. Planning retains adopted policy imports and neighborhood applicability, saved staff analyses, reviewed snapshots, municipal initiatives and amendment history. An analysis or amendment draft does not adopt policy.

Staff should begin with First run and Daily workflow. Administrators should also read Architecture, Technical specifications, Configuration, Security and Recovery. Developers should use the exact API/data dictionary and examples. The table of contents and alphabetical subject index link to the relevant sections in the HTML edition; the PDF preserves headings and searchable text. An editable Word edition is included with the same documentation companion.

## Beta identity

| Identity | Value |
| --- | --- |
| Public documentation identity | Townlight Beta 1 |
| Installer version | 1.6.0.1 |
| Product component | civicplan 0.4.0.dev1 |
| Native desktop source version | 1.6.0-1 |
| Candidate MSI SHA256 | `98bcdef11ebdf5c767f620c904ff49f85115fde3b5c23f62703b111e645aaf86` |
| Corresponding-source SHA256 | `84a23e1297e42d17b16cfc9e51b2dd78bc46414c0de8ad7ebd2466c1a409d06b` |
| Current owned software license | AGPL-3.0-only |
| Supported acceptance profile | Windows x64 fresh install; inspections-preview; separate Station configuration |


“Townlight Beta 1” identifies this coordinated beta delivery. It does not renumber the installer, native binary, Python packages or historical receipts. Component versions may differ. This documentation is a later companion to unchanged signed bytes, not a rebuilt installer. Historical release pages and manuals describe their own versions and are not the download instructions for this private candidate.

## First run

1. Obtain the identified signed private candidate and its corresponding-source companion from the beta coordinator. The landing pages in this documentation are not an installer download service.
2. On the intended fresh Windows test installation, verify the MSI hash and publisher signature before installing. Preserve unrelated profiles and recovery material. This candidate has fresh-install acceptance; historical in-place upgrades are unverified.
3. Launch Townlight under the intended named Windows account. Choose the storage folders. Select **Townlight Inspections candidate** (`inspections-preview`) for all eight desktop products. A narrower default selection will not expose all workspaces.
4. Enter the city profile, time zone and contacts. Create the first named local administrator, sign in and choose protected backup storage. **Continue without local AI** is valid for the deterministic workflows.
5. Run Health Check and wait for readiness. Open Townlight. In System Health select **Finish Records Migration** to activate the canonical Python/PostgreSQL runtime. Do not fabricate migration receipts or seed accounts.
6. Create named staff through Settings. Import authorized sources using each product’s source library. All examples in this package are synthetic; they are not municipal authority.
7. Provision Station separately if it is part of the beta exercise. Selecting the desktop composition does not start or configure Station. Configure vision explicitly only if automatic photo drafting is selected.

## Daily workflow

<a name="workflow-1"></a>

### 1. Import adopted policy

Open Policy library. Preview jurisdiction, adoption/source dates, policy IDs, neighborhood applicability and originals, then confirm the complete source bundle. Retain the previous revision.

<a name="workflow-2"></a>

### 2. Create or reopen an analysis

Open Analyses and select the project. Use Next page when the loaded page does not contain the saved work. Enter the proposal, analysis and private staff notes.

<a name="workflow-3"></a>

### 3. Select policies and evidence

In Policies & evidence select exact policy revisions and applicable neighborhood context. Record supporting, conflicting or uncertain considerations. Select permitted Meetings or Zoning evidence with its expected hash.

<a name="workflow-4"></a>

### 4. Save and reconcile

Use Save draft before navigating or signing out. When another revision exists, reopen it and reconcile your edits. Do not resubmit against a guessed revision identifier.

<a name="workflow-5"></a>

### 5. Review the saved revision

In Review & export check the audience, public summary and review notes. Save, then Record review of saved draft. The trusted staff path derives identity/date. Editing later produces a new revision requiring review.

<a name="workflow-6"></a>

### 6. Create and export a snapshot

Preview the reviewed saved revision, inspect the returned content, then create the snapshot. Public copies exclude staff notes and full staff analysis under the public contract. Export verifies the expected SHA256.

<a name="workflow-7"></a>

### 7. Track initiatives and amendments

Create and revise municipal initiative status, responsibility, targets, milestones and measurements using the existing controls. Retain history. Draft and review amendments separately; adoption must identify the actual adopted source revision.

<a name="workflow-8"></a>

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
| --- | --- |
| Input | Complete adopted policy source bundles, proposal context, versioned policy selections, permitted Meetings/Zoning evidence and staff progress updates. |
| Output | Cited analyses, audience-specific reviewed snapshots, durable initiative/history records and amendment lifecycle records. |


### Product boundary

Existing initiative/amendment persistence is included. A draft amendment does not change an adopted source revision. Historical standalone sample pages are not the installed staff workspace. Analysis lists and project filters operate on loaded pages; use pagination to reach additional records.

## Architecture

![Townlight Planning architecture and evidence flow](docs/beta-1/assets/planning-architecture.svg)

The drawing shows the principal staff/evidence path. Native commands carry trusted identity to Python business services; PostgreSQL and retained original files hold durable state. A downstream copy does not silently transfer decision authority. Station has its own configured authority/media boundary, database and mutable files. The connected-workflow text supplies the drawing’s reading order and accessibility alternative.

## Exploration initiatives and amendments

### Explore adopted plans

Open **Policy library** and find **Explore adopted plans**. Enter a topic and/or choose the supplied goal, neighborhood and plan-type filters. These are separate facets; keyword search is not a substitute for neighborhood applicability. Run exploration and inspect each returned plan, adopted/source dates, exact policy references and permitted original material. Empty results can mean no matching permitted adopted source, not an error or an invented plan.

The existing public exploration transport is `planning_public_request`, separate from staff `planning_domain_request`. Technical clients use its documented `plan-explore` operation or the mounted public route in the API companion. A native operation fragment is:

```json
{"operation":"plan-explore","payload":{"topic":"synthetic mobility","neighborhood":"Synthetic North","goal":"","plan_type":""}}
```

Only public-permitted adopted sources belong in this result. Private staff analyses, selected restricted evidence and staff notes do not become public through exploration. The output includes matching plans/facets and an informational disclaimer; no cross-plan AI synthesis or internet portal commissioning is implied.

### Track a municipal initiative

Open **Implementation & amendments**. Choose an actual retained policy selection, title, responsible staff, target, unit, due date and explanatory note. Save a planned/active initiative and reopen its current revision/history. Add milestones and measurements with their dates and evidence. Each change uses the latest `expected_revision`; reconcile a conflict by reopening the current state rather than guessing a revision.

The initiative statuses are `planned`, `active`, `completed` and `cancelled`. A completed initiative requires measurement evidence and every supplied milestone completed. A milestone completion needs supporting evidence and a completion date that is not in the future. Numerical progress without its source/evidence is not a completed municipal outcome.

For a synthetic exercise, create an active initiative with a fictional policy selection, target `3`, unit `synthetic reviews`, an intended future due date and a note explaining the test. Add one evidence-backed measurement, then complete each milestone before requesting completed status. Read the saved initiative/history after every accepted revision. No external project system is updated by this save.

### Retain an amendment lifecycle

An amendment has its own proposal and history; changing an analysis does not adopt an amendment. In **Implementation & amendments**, select the actual policy, enter proposal text, title, responsible staff and a note, then save `draft`. The allowed amendment statuses are `draft`, `review`, `adopted` and `withdrawn`.

Moving to `review` or `adopted` requires a recorded `review_note`. Before recording `adopted`, import and verify the actual adopted policy revision, then supply its `adoption_revision` identity. Only an adopted amendment may carry that field; draft/review/withdrawn records must omit it or use null. The proposal's existing policy reference and newly imported adoption revision have distinct roles. Staff record the authorized decision; a status choice does not itself enact policy.

Use the latest `expected_revision` when revising. Reopen the amendment and municipal history, confirm status, review note and adoption link, and retain prior revisions. Public exploration changes only when its permitted adopted sources actually change, not merely because staff created a proposal.

Source contracts: `civicplan/public_explore.py`, `municipal.py`, `civicsuite_runtime/planning_bridge.py` and the Planning view. The API dictionary carries `InitiativeInput`, `Milestone`, `Measurement`, `AmendmentInput` and the exact policy-selection fields; conditional completion/adoption checks above also apply beyond simple field validation.


## Technical specifications
### Runtime and storage

The accepted package targets **Windows x64 fresh installation**. Its native shell uses **Rust 2021, Tauri 2 and Microsoft WebView2**; browser assets are JavaScript built with **Vite 8.1.6**. This describes the native desktop frontend; Station has a separate React operator, specified below or in its product manual. Canonical business workflows use bundled **CPython 3.13.5, FastAPI, Pydantic, SQLAlchemy and Alembic**, with **PostgreSQL 17 / PostGIS** and managed original files. The installed runtime tested here contains FastAPI 0.162.0. Package minimum Python requirements can differ from the bundled executable; the metadata reference preserves both. No stack rewrite is implied by the beta label.

The native transport is fixed to loopback `127.0.0.1:15480`; PostgreSQL uses the configured local runtime port (default `15432`). Optional local model service defaults to `127.0.0.1:15434`. Those are deployment defaults, not internet endpoints. The runtime has health, module and readiness endpoints; readiness is stronger than process existence. The task queue is the existing local Core task infrastructure, not an assertion that a separate Redis service is required for this desktop composition.

The default native profile is `%LOCALAPPDATA%\CivicSuite`; the historical directory name remains part of compatibility. Do not rename it to Townlight. A configured `TOWNLIGHT_PROFILE_ROOT` must be absolute. Local configuration and secrets live under that profile; protected managed files and database state must be backed up coherently. Source/runtime identity is distinct from a product’s display label.

### Data and consistency

Plan bundles and revisions; original documents; versioned policy selections and neighborhood applicability; analysis revisions; reviews and snapshots; initiatives, milestones and measurements; amendment revisions.

Versioned saves use expected prior revision identifiers where defined. Reopen and reconcile on conflict. Exact exports and handoffs use source IDs, current visibility, revision and SHA256. Review belongs to the saved revision and does not transfer silently to edited text. Database changes use the owning product’s migrations; a request or readiness check is not an authorization to mutate schema.

### Capacity and platform statements

This beta has synthetic single-profile workflow evidence. It does not have a published benchmark for concurrent staff capacity, minimum RAM/CPU, large-source limits or a field SLA. Do not turn a developer machine’s specification into a supported minimum. Installer size is 2,092,122,112 bytes before installation; allow additional disk for extracted runtime, database, originals, exports, media and backups. Select equipment/storage after sizing those actual workloads.

The exact [runtime payload lock](docs/beta-1/reference/runtime-payload-lock.json) records pinned files, sizes and hashes. The [component metadata](docs/beta-1/reference/component-metadata.json) records shipped dependency declarations. These references are more precise than a manually copied dependency list. Third-party and historical license notices must accompany their matching payloads.

## Configuration and administration
### Native deployment configuration

Use Setup, Settings and System Health for supported staff operation. Administrators provision folders, backup storage, named accounts and the city profile. Select `inspections-preview` for the full eight-workspace desktop. Station remains a separate service boundary. Do not use a standalone product’s demo server as a substitute for the installed workspace.

Technical deployments use `TOWNLIGHT_PRODUCT_PROFILE`, `TOWNLIGHT_PROFILE_ROOT`, `DATABASE_URL`, `CIVICSUITE_RUNTIME_PORT`, `PORTAL_MODE` and the runtime-managed secret files. Treat database URLs and native session proofs as secrets. The installed native domain runtime explicitly refuses non-loopback binding. `PORTAL_MODE=private` is the accepted posture; changing it does not by itself commission an internet portal, authentication provider or reverse proxy.

The isolated documentation exporter sets a fictional profile and unusable synthetic database origin only to read schemas; those values are not deployment configuration. Keep deployment values in the intended process/account scope. An already-running process does not automatically inherit later environment edits.

## API and integration examples
### Native command example

The following JavaScript belongs in the existing trusted Townlight frontend/development environment with `invoke` imported from `@tauri-apps/api/core`. It is not a command for an arbitrary web page or an instruction for nontechnical staff. IDs must come from records created in an isolated synthetic exercise.

```javascript
import { invoke } from '@tauri-apps/api/core';
const result = await invoke('planning_domain_request', {request: {operation: 'sources', offset: 0}});
console.log(result);
```

### Trusted local HTTP example

An administrator/developer can inspect an already-configured isolated runtime from a trusted local process. This PowerShell example reads the signed-in synthetic profile’s existing proof into memory; it does not create a user, seed a session, reveal the proof in output or bypass a permission check. Do not use real city data in development examples. A read response does not prove approval or publication.

```powershell
$profilePath = Join-Path $env:LOCALAPPDATA 'CivicSuite'
$sessionPath = Join-Path $profilePath 'config\local-session.json'
$session = Get-Content -LiteralPath $sessionPath -Raw | ConvertFrom-Json
$headers = @{ 'X-Townlight-Session' = $session.session_hash }
Invoke-RestMethod -Uri 'http://127.0.0.1:15480/desktop/v1/planning/sources' -Headers $headers
Remove-Variable session, headers
```

### Complete synthetic source bundle

The [synthetic Planning bundle](docs/beta-1/reference/examples/synthetic-plan-bundle.json) is the retained fixture used by the beta staff exercise. It includes the complete supported source envelope rather than a shortened pseudo-payload. Keep its fictional source labels. For Planning, wrap it as `{"bundle": BUNDLE, "expected_previous_revision": null}`; for Permitting use `{"bundle": BUNDLE, "expected_revision": null}`. Code and Zoning take their own complete import envelopes. Replace null with the current expected revision when revising an existing source, as the applicable schema requires. These are import examples, not legal authority or permission to load them into a live city profile.

### A synthetic write with subsequent readback

This example demonstrates the existing Meetings HTTP contract in an isolated exercise. It is intentionally fictional. It does not start a service. Its authentication setup is included so it can be run independently under the signed-in synthetic account. If a write times out, inspect current records before repeating it.

```powershell
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

Read the [Planning API reference](docs/beta-1/api/planning.html) for every documented operation, request field, constraint, response declaration and source supplement. Download the [OpenAPI JSON](docs/beta-1/api/planning-openapi.json) for tools. For Station this is the suite-side schema only; its separate service contract is documented in the API supplement. The [reference directory](docs/beta-1/reference/index.html) includes configuration/source inventories, dependency declarations, native command contracts, MCP signatures and candidate evidence.

## MCP and automation boundary

No direct product MCP server is exposed by the accepted Townlight desktop or Station boundary. Do not configure an invented `townlight mcp` command or assume an AI client has staff permissions. The integration surfaces for this beta are native IPC, the documented HTTP APIs, source bundle imports, exact exports and the existing Station CLI.

The bundled transcription code includes a **TextFlowKit MCP adapter** as a separate source capability. It offers job-based `transcribe_media`, `get_transcript`, `list_jobs`, `get_job_status` and `export_transcript`, and additional tools declared in that adapter. It uses stdio first and optional Streamable HTTP, with the MCP SDK as an optional extra. It is not automatically launched, authenticated as Townlight staff or accepted as a Townlight product MCP deployment. This documentation does not add such a service.

For a transcription client already provisioned separately, an illustrative tool call is:

```json
{"name":"get_job_status","arguments":{"job_id":"synthetic-existing-job-id"}}
```

Use a job ID returned by that transcription service. This example does not create a Townlight record or bypass its review/Records handoff. The exact optional adapter tool signatures are supplied in the [MCP source reference](docs/beta-1/reference/mcp.html). Station meeting capture does not become live speech recognition because this optional donor adapter exists.

## Security and permissions


Use your own named account and save before leaving a screen. A saved draft is durable; unsaved form text may not be. If a write has an unknown result, reopen its record before repeating it.

Read source jurisdiction, dates, citation, version and visibility. A copied source hash identifies exact bytes, not their legal applicability. If a source changes or permission is removed, resolve the source problem rather than substituting stale cached content.

Keep originals and derivatives separate. Review the intended audience before export. A public summary excludes private fields only through the applicable copy contract and your review. A renamed private packet is still private content.

Drafting, review, approval, attachment, export, fulfillment and publication are separate operations. A Townlight workpaper does not itself adopt law, issue a permit, impose a fine or release a records response. The responsible staff member records the applicable decision.

The native session is validated and mapped to a persisted SQL identity. An editable actor/reviewer label is not authentication. Product/module permissions and source visibility apply at the server boundary. Revoked/unavailable authority fails closed for new Station operations; a previous permission result is not a perpetual authorization.

Use protected local folders, account permissions and credential storage. Never include the native session file, database passwords, provider keys or unredacted support bundles in a public issue or generated public documentation. A local public view is not automatically a secured internet deployment. Keep network exposure and real equipment acceptance specific to the chosen beta site.

## Backup recovery and maintenance

Save work and use Core’s canonical **Backup Now** before maintenance. That operation stops writers. Preserve the coherent profile/database/document backup and its receipt, then use **Start** to resume. A source export is not a full backup.

Use **Restore Latest Backup** through the supported controls. If the result says **Restore needs service start**, use **Start**, then **Check**, and reopen a known record. Do not repeat restore merely because services need to start. The fresh-profile acceptance verified that a fulfilled request survived restore and a post-backup marker did not.

Keep Station’s dedicated database and media evidence together in its own backup. Core’s native-profile backup must not be assumed to include an external Station data directory. Stop writers during a coordinated backup. Preserve failed media attempts and logs.

On failure, record the time, selected composition, component/installer versions and exact message. Check System Health for stopped, starting, ready or failed dependencies. Use the existing Retry control after readiness; do not create duplicate business records to refresh a stale view. Share only a redacted diagnostic bundle. Preserve secrets, original evidence, recovery material and unrelated installations.

## Troubleshooting

| Symptom | Likely meaning | Next action |
| --- | --- | --- |
| Workspace absent | Wrong product composition or unavailable canonical runtime. | Check selected composition; activate through Finish Records Migration; wait for readiness. |
| Cannot sign in / 401 | Missing or expired named account session. | Sign in normally; reopen a Station launch ticket if applicable. |
| Permission denied / 403 | Account, module, source or browser-origin permission. | Ask the authorized administrator to inspect the intended permission; do not invent role headers. |
| Save conflict / 409 | The saved revision, expected source hash or lifecycle changed. | Keep edits, reopen current state and reconcile deliberately. |
| Invalid input / 422 | Required field, format, geometry, source envelope or state is invalid. | Read the field detail and correct the input/source; preserve originals. |
| Service unavailable / 503 | Database, schema, connected source or configuration unavailable. | Inspect System Health and the named dependency. Preserve work; retry only after readiness. |
| Export refused | Missing exact review, approval, audience or source authorization. | Read the refusal and complete the owning product’s explicit decision. |
| Restore needs service start | The snapshot was restored but services have not resumed. | Use Start, then Check and verify a saved record; do not blindly repeat restore. |


## Verified workflows and limits

| Product | Recorded result | Precisely exercised |
| --- | --- | --- |
| Planning | PASS | Adopted source import with neighborhood, saved/reviewed analysis and snapshot, persisted initiative/history and draft amendment, public explorer neighborhood readback and native workspace. |


These results come from the identified signed candidate’s fresh normal-profile Sandbox exercise: real native IPC/HTTP/PostgreSQL and selected headless controls. All accounts, source bundles and media were synthetic. The guest install/uninstall and recovery passed, and the owned Sandbox stopped. No host installed application or standalone CivicCast was changed. This documentation task reuses those receipts; it does not claim a new software acceptance run.

The [workflow matrix](docs/beta-1/reference/workflow-matrix.json) identifies raw receipt filenames. The [evidence index](docs/beta-1/reference/sandbox-evidence-index.json) retains their original hashes; raw receipts remain in the private beta handoff rather than being silently republished with the documentation site.

The limits remain: actual city field acceptance and equipment/network commissioning; Station automatic provisioning/SCM commissioning; every UI/role combination; field recognition accuracy; and historical in-place upgrades are not certified. They are not five invented feature requirements. Fresh-install controlled beta handoff remains the accepted scope. This package makes no city-deployment, publication or general-availability claim.

## Terms of service and license

### Scope and status

These terms describe the Townlight Beta 1 software and this documentation package. This is a locally prepared private beta, not a hosted-service subscription, a city deployment agreement or a public release. No uptime commitment, support response time, indemnity, data-processing agreement or paid service is created by these documents. A separate signed agreement, if any, governs services it actually provides.

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

Use the identified candidate in its supported fresh-install scope. Preserve backups and original evidence. Test physical equipment and chosen network/service configuration before relying on them. The supplied acceptance describes selected synthetic workflows, not every screen, vendor, field condition or upgrade. Operators decide whether a particular deployment meets their own operational obligations.

### Warranty and liability

The covered software’s warranty and liability conditions are those in sections 15–17 of the supplied AGPL and any applicable separate written undertaking. This documentation creates no additional warranty or limitation beyond those terms. Third-party software is subject to its retained license notices. Nothing here removes rights that applicable law makes nonwaivable.

### Support and incident reporting

Use the project’s existing SUPPORT and SECURITY guidance for its matching repository. Report reproducible behavior with the version, operation and redacted logs. Do not put credentials, resident records or unredacted evidence in a public issue. Coordinate sensitive reports through the channel designated in SECURITY. No new support address or service commitment is invented here.

### Ending a beta exercise and document changes

When an organization ends testing, it controls retention/export and removes access according to its policy. Uninstall may retain data; back up and inspect the selected removal options. Ending an exercise does not revoke rights already granted by AGPL. Later software/documentation versions must identify their changed candidate and scope; historical receipts retain their original identities. These terms do not claim that a city has accepted a contract merely by reading a manual.

## Glossary

| Term | Meaning |
| --- | --- |
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

- **Accounts and authentication** — [Security and permissions](#security-and-permissions).
- **AGPL and source** — [Terms of service and license](#terms-of-service-and-license).
- **API contracts** — [API and integration examples](#api-and-integration-examples).
- **Architecture** — [Architecture](#architecture).
- **Backup** — [Backup recovery and maintenance](#backup-recovery-and-maintenance).
- **Beta version** — [Beta identity](#beta-identity).
- **Configuration** — [Configuration and administration](#configuration-and-administration).
- **Evidence and acceptance** — [Verified workflows and limits](#verified-workflows-and-limits).
- **Fees and official decisions** — [Terms of service and license](#terms-of-service-and-license).
- **First run** — [First run](#first-run).
- **Handoffs and audience** — [Connected workflows](#connected-workflows).
- **MCP** — [MCP and automation boundary](#mcp-and-automation-boundary).
- **Originals and provenance** — [Security and permissions](#security-and-permissions).
- **Recovery** — [Backup recovery and maintenance](#backup-recovery-and-maintenance).
- **Staff procedures** — [Daily workflow](#daily-workflow).
- **Station configuration** — [Configuration and administration](#configuration-and-administration).
- **Technical stack** — [Technical specifications](#technical-specifications).
- **Troubleshooting** — [Troubleshooting](#troubleshooting).

### Operating subject links

- **Exploration initiatives and amendments** — [Exploration initiatives and amendments](#exploration-initiatives-and-amendments).
- **Explore adopted plans** — [Explore adopted plans](#explore-adopted-plans).
- **Retain an amendment lifecycle** — [Retain an amendment lifecycle](#retain-an-amendment-lifecycle).
- **Track a municipal initiative** — [Track a municipal initiative](#track-a-municipal-initiative).

## Source and document control

This edition is authored from the immutable corresponding-source companion, the generated installed-domain schema and the retained workflow receipts. The current software versions and signed artifacts are unchanged. Public historical pages are not synchronized or published by this local documentation task.

### Workflow subject index

- **Create and export a snapshot** — [Daily workflow, step 6](#workflow-6).
- **Create or reopen an analysis** — [Daily workflow, step 2](#workflow-2).
- **Import adopted policy** — [Daily workflow, step 1](#workflow-1).
- **Review the saved revision** — [Daily workflow, step 5](#workflow-5).
- **Save and reconcile** — [Daily workflow, step 4](#workflow-4).
- **Select policies and evidence** — [Daily workflow, step 3](#workflow-3).
- **Share deliberately** — [Daily workflow, step 8](#workflow-8).
- **Track initiatives and amendments** — [Daily workflow, step 7](#workflow-7).

- [Source inventory and file hashes](docs/beta-1/reference/source-inventory.json)
- [All component metadata](docs/beta-1/reference/component-metadata.json)
- [Installed domain OpenAPI](docs/beta-1/reference/desktop-domain-openapi.json)
- [Workflow matrix](docs/beta-1/reference/workflow-matrix.json)
- [Full AGPL text](docs/beta-1/reference/AGPL-3.0.txt)
