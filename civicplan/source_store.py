"""Transactional append-only plan imports and permission-filtered source reads."""

import base64
from datetime import UTC, date, datetime
import hashlib
import json
from uuid import NAMESPACE_URL, uuid5

from civiccore.audit import (
    PersistedAuditLogEntry, ZERO_HASH, compute_persisted_audit_hash, verify_persisted_audit_chain,
)
import sqlalchemy as sa

from civicplan.migrations import ready
from civicplan.source_bundle import PlanBundle
from civicplan.source_schema import documents, events, evidence, plans, policies, revisions


class SourceConflict(ValueError):
    pass


class SourcesUnavailable(RuntimeError):
    pass


class PlanSourceRepository:
    def __init__(self, engine: sa.Engine):
        self.engine = engine
        if not ready(engine):
            raise SourcesUnavailable("Run python -m civicplan.migrations before importing Planning sources.")

    def import_bundle(
        self, bundle: PlanBundle, *, actor_id: str, expected_previous_revision: str | None = None,
    ) -> dict:
        if not actor_id.strip():
            raise ValueError("An authenticated import actor is required.")
        digest = _bundle_hash(bundle)
        revision_id = str(uuid5(NAMESPACE_URL, f"townlight:planning:{bundle.plan_id}:{digest}"))
        timestamp = datetime.now(UTC).isoformat()
        with self.engine.begin() as connection:
            # Serialize imports/audit for each plan, including the first insert.
            if connection.dialect.name == "postgresql":
                lock = int.from_bytes(hashlib.sha256(bundle.plan_id.encode()).digest()[:8], "big", signed=True)
                connection.execute(sa.text("SELECT pg_advisory_xact_lock(:key)"), {"key": lock})
            duplicate = connection.execute(sa.select(revisions).where(
                revisions.c.revision_id == revision_id
            )).mappings().first()
            if duplicate:
                return {"revision_id": revision_id, "bundle_sha256": digest, "created": False}
            head = connection.execute(sa.select(plans).where(
                plans.c.plan_id == bundle.plan_id
            )).mappings().first()
            previous = head["latest_revision_id"] if head else None
            if previous != expected_previous_revision:
                raise SourceConflict("Plan changed; read its history and supply the current previous revision.")
            previous_event = connection.execute(sa.select(events).where(
                events.c.revision_id == previous
            )).mappings().first() if previous else None
            sequence = previous_event["sequence"] + 1 if previous_event else 1
            if not head:
                connection.execute(plans.insert().values(plan_id=bundle.plan_id, latest_revision_id=revision_id))
            connection.execute(revisions.insert().values(
                revision_id=revision_id, parent_revision_id=previous, sequence=sequence,
                bundle_sha256=digest, actor_id=actor_id, created_at=timestamp,
                **{k: getattr(bundle, k) for k in (
                    "plan_id", "title", "jurisdiction", "plan_type", "status", "visibility",
                    "dataset_kind", "source_date", "adopted_on", "effective_on", "change_note", "reviewer_label",
                )},
            ))
            for doc in bundle.documents:
                connection.execute(documents.insert().values(
                    revision_id=revision_id, document_id=doc.document_id, filename=doc.filename,
                    media_type=doc.media_type, sha256=doc.sha256, original_bytes=doc.original_bytes(),
                ))
            for policy in bundle.policies:
                connection.execute(policies.insert().values(
                    revision_id=revision_id, **policy.model_dump(exclude={"staff_verified"}),
                ))
            for index, item in enumerate(bundle.adoption_evidence):
                connection.execute(evidence.insert().values(
                    revision_id=revision_id, ordinal=index, **item.model_dump(),
                ))
            details = {"plan_id": bundle.plan_id, "revision_id": revision_id, "bundle_sha256": digest}
            previous_hash = previous_event["entry_hash"] if previous_event else ZERO_HASH
            action = "planning.source.import"
            connection.execute(events.insert().values(
                revision_id=revision_id, plan_id=bundle.plan_id, sequence=sequence,
                previous_hash=previous_hash, timestamp=timestamp, actor_id=actor_id, action=action,
                details=details, entry_hash=compute_persisted_audit_hash(
                    previous_hash=previous_hash, timestamp=timestamp, actor_id=actor_id,
                    action=action, details=details,
                ),
            ))
            if head:
                connection.execute(plans.update().where(plans.c.plan_id == bundle.plan_id).values(
                    latest_revision_id=revision_id
                ))
        return {"revision_id": revision_id, "bundle_sha256": digest, "created": True}

    def history(self, plan_id: str, *, staff: bool = False) -> list[dict]:
        with self.engine.connect() as connection:
            query = sa.select(revisions).where(revisions.c.plan_id == plan_id).order_by(revisions.c.sequence)
            if not staff:
                query = query.where(revisions.c.visibility == "public", revisions.c.dataset_kind == "municipal")
            result = [dict(row) for row in connection.execute(query).mappings()]
            if not staff:
                for item in result:
                    for key in ("reviewer_label", "actor_id", "change_note"):
                        item.pop(key, None)
            return result

    def revision(self, revision_id: str, *, staff: bool = False) -> dict | None:
        with self.engine.connect() as connection:
            query = sa.select(revisions).where(revisions.c.revision_id == revision_id)
            if not staff:
                query = query.where(revisions.c.visibility == "public", revisions.c.dataset_kind == "municipal")
            row = connection.execute(query).mappings().first()
            if not row:
                return None
            result = dict(row)
            for label, table in (("policies", policies), ("adoption_evidence", evidence)):
                result[label] = [dict(item) for item in connection.execute(
                    sa.select(table).where(table.c.revision_id == revision_id).order_by(
                        table.c.ordinal if label == "adoption_evidence" else table.c.policy_id
                    )
                ).mappings()]
            result["documents"] = [dict(item) for item in connection.execute(sa.select(
                documents.c.document_id, documents.c.filename, documents.c.sha256, documents.c.media_type,
            ).where(documents.c.revision_id == revision_id)).mappings()]
            if not staff:
                for key in ("reviewer_label", "actor_id", "change_note"):
                    result.pop(key, None)
            return result

    def original_document(self, revision_id: str, document_id: str, *, staff: bool = False) -> dict | None:
        if self.revision(revision_id, staff=staff) is None:
            return None
        with self.engine.connect() as connection:
            row = connection.execute(sa.select(documents).where(
                documents.c.revision_id == revision_id, documents.c.document_id == document_id,
            )).mappings().first()
            return dict(row) if row else None

    def adopted_policies(self, *, as_of: date | None = None) -> list[dict]:
        """Public municipal policy projection; pending revisions never replace adopted text."""
        as_of = as_of or date.today()
        with self.engine.connect() as connection:
            rows = connection.execute(sa.select(revisions).order_by(revisions.c.sequence)).mappings().all()
            active = {}
            for row in rows:
                when = row["effective_on"] or row["source_date"]
                if row["status"] != "pending" and when <= as_of:
                    active[row["plan_id"]] = row
            ids = [r["revision_id"] for r in active.values() if r["status"] == "adopted"
                   and r["visibility"] == "public" and r["dataset_kind"] == "municipal"]
            return [dict(row) for row in connection.execute(sa.select(
                policies, revisions.c.plan_type, revisions.c.plan_id,
                revisions.c.adopted_on, revisions.c.effective_on,
            ).join(revisions, policies.c.revision_id == revisions.c.revision_id).where(
                policies.c.revision_id.in_(ids)
            )).mappings()]

    def audit(self, plan_id: str) -> dict:
        with self.engine.connect() as connection:
            rows = connection.execute(sa.select(events).where(
                events.c.plan_id == plan_id
            ).order_by(events.c.sequence)).mappings().all()
        entries = [PersistedAuditLogEntry(**{key: row[key] for key in (
            "previous_hash", "entry_hash", "timestamp", "actor_id", "action", "details",
        )}, entry_id=row["revision_id"]) for row in rows]
        ok, count, error = verify_persisted_audit_chain(entries, accept_first_previous_hash=False)
        if count != len(self.history(plan_id, staff=True)):
            ok, error = False, "audit/revision count mismatch"
        integrity = self.verify_sources(plan_id)
        return {"ok": ok and integrity["ok"], "count": count, "error": error,
                "source_integrity": integrity, "events": [dict(row) for row in rows]}

    def verify_sources(self, plan_id: str) -> dict:
        """Rebuild the canonical imported bundle from independent stored rows/bytes."""
        for revision in self.history(plan_id, staff=True):
            stored = self.revision(revision["revision_id"], staff=True)
            data = {key: stored[key] for key in PlanBundle.model_fields if key in stored}
            data["documents"] = []
            for doc in stored["documents"]:
                original = self.original_document(revision["revision_id"], doc["document_id"], staff=True)
                data["documents"].append({**doc, "content_base64": base64.b64encode(original["original_bytes"]).decode()})
            data["policies"] = [{**{key: value for key, value in p.items() if key != "revision_id"},
                                 "staff_verified": True} for p in stored["policies"]]
            data["adoption_evidence"] = [{key: value for key, value in e.items()
                                          if key not in {"revision_id", "ordinal"}}
                                         for e in stored["adoption_evidence"]]
            try:
                rebuilt = PlanBundle.model_validate(data)
                if _bundle_hash(rebuilt) != revision["bundle_sha256"]:
                    return {"ok": False, "revision_id": revision["revision_id"], "error": "bundle hash mismatch"}
            except ValueError:
                return {"ok": False, "revision_id": revision["revision_id"], "error": "stored source validation failed"}
        return {"ok": True}


def _bundle_hash(bundle: PlanBundle) -> str:
    payload = bundle.model_dump(mode="json")
    payload["documents"] = sorted(payload["documents"], key=lambda item: item["document_id"])
    payload["policies"] = sorted(payload["policies"], key=lambda item: item["policy_id"])
    for document in payload["documents"]:
        document["content_base64"] = base64.b64encode(
            next(d for d in bundle.documents if d.document_id == document["document_id"]).original_bytes()
        ).decode()
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
