# Native Planning development integration

Planning development `0.3.0+dev.1` supplies the persisted source, analysis and
snapshot services used by the opt-in Townlight `planning-preview` desktop profile.
The historical Planning release/installer version remains `0.2.2`. This work does
not certify a public release or change the signed Townlight 1.4 installer.

The native bridge lives in `townlight/townlight`, at `/desktop/v1/planning`. It
validates the existing native session proof, maps the account to its SQL UUID,
and derives import actors and review attribution on the server. City staff and
administrators can use private Planning work; a Records-only account uses the
existing Records snapshot selection contract. JavaScript receives no staff key.
The existing service-key API and its historical audit rows retain their contract.

Staff inventories expose current plan and analysis summaries in pages of 1-100
items, using stable IDs and an offset. Source inventory includes pending/private
imports. Original bytes, source history and full private analysis require separate
authenticated reads. Snapshot inventory rechecks current source permissions and
hashes for every returned item. Unavailable evidence is never a cached substitute.

`preview_snapshot` validates the current reviewed revision and intended audience
without writing. Creation uses that same canonical representation, then rechecks
the head inside the transaction. A stale revision returns a conflict; reopen saved
work and reconcile edits. Public snapshots contain the separately edited summary
and permitted citations. Staff proposal, considerations, private notes and review
notes remain outside the public representation. Access advice retains the original.

Native development acceptance and candidate provenance belong to the umbrella
repository. Source/unit/browser checks alone do not prove the installed workflow.
P6 release certification, signing, tags and publication remain separate work.
