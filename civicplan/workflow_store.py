"""Versioned staff work and immutable, permission-rechecked source snapshots."""
from datetime import UTC, datetime
import hashlib
import json
from uuid import NAMESPACE_URL, uuid4, uuid5

from civiccore.audit import ZERO_HASH, PersistedAuditLogEntry, compute_persisted_audit_hash, verify_persisted_audit_chain
import sqlalchemy as sa

from civicplan.connections import ConnectionUnavailable, permitted
from civicplan.policy_lookup import DISCLAIMER
from civicplan.policy_service import PolicyService
from civicplan.source_store import SourceConflict
from civicplan.workflow_schema import analyses, versions, snapshots, events


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


class WorkflowRepository:
    def __init__(self, sources, providers=None, access_rewrite=None):
        self.sources = sources
        self.engine = sources.engine
        self.policies = PolicyService(sources)
        self.providers = providers or {}
        self.access_rewrite = access_rewrite

    def _lock(self, conn, analysis_id):
        if conn.dialect.name == 'postgresql':
            key = int.from_bytes(hashlib.sha256(('analysis:' + analysis_id).encode()).digest()[:8], 'big', signed=True)
            conn.execute(sa.text('SELECT pg_advisory_xact_lock(:key)'), {'key': key})

    def _event(self, conn, analysis_id, actor, action, details):
        previous = conn.execute(sa.select(events).where(events.c.analysis_id == analysis_id)
                                .order_by(events.c.sequence.desc()).limit(1)).mappings().first()
        old_hash = previous['entry_hash'] if previous else ZERO_HASH
        timestamp = datetime.now(UTC).isoformat()
        conn.execute(events.insert().values(event_id=str(uuid4()), analysis_id=analysis_id,
            sequence=previous['sequence'] + 1 if previous else 1, previous_hash=old_hash,
            timestamp=timestamp, actor_id=actor, action=action, details=details,
            entry_hash=compute_persisted_audit_hash(previous_hash=old_hash, timestamp=timestamp,
                                                  actor_id=actor, action=action, details=details)))

    def _policies(self, selections, *, public=False):
        result = []
        for ref in selections:
            policy = self.policies.resolve(ref['revision_id'], ref['policy_id'], staff=not public)
            if policy['plan_id'] != ref['plan_id']:
                raise ValueError('Selected plan does not own this policy revision.')
            if not self.sources.verify_sources(ref['plan_id'])['ok']:
                raise ValueError('Source integrity failed; no analysis or export accepted.')
            result.append(policy)
        return result

    def _links(self, selections):
        return [{'provider': link['provider'], 'relation': link['relation'],
                 'source': permitted(self.providers, link)} for link in selections]

    def save(self, data, actor, analysis_id=None):
        if not actor.strip():
            raise ValueError('Authenticated actor required.')
        analysis_id = analysis_id or str(uuid4())
        payload = data.model_dump(mode='json', exclude={'expected_previous_revision'})
        context = self._policies(payload['selected_policies'])
        self._links(payload['linked_sources'])
        payload['policy_context'] = context
        payload['disclaimer'] = DISCLAIMER
        if not payload['analysis_text']:
            payload['analysis_text'] = 'Draft for staff review.\n\n' + '\n\n'.join(
                f'{p["citation"]}, {p["anchor"]} ({p["effective_on"]}): {p["excerpt"]}' for p in context)
        digest = sha(canonical(payload))
        revision_id = str(uuid5(NAMESPACE_URL, f'townlight:planning:analysis:{analysis_id}:{digest}'))
        with self.engine.begin() as conn:
            self._lock(conn, analysis_id)
            head = conn.execute(sa.select(analyses).where(analyses.c.analysis_id == analysis_id)).mappings().first()
            if conn.execute(sa.select(versions.c.revision_id).where(versions.c.revision_id == revision_id)).first():
                return {'analysis_id': analysis_id, 'revision_id': revision_id, 'sha256': digest, 'created': False}
            previous = head['latest_revision_id'] if head else None
            if previous != data.expected_previous_revision:
                raise SourceConflict('Analysis changed; reload and reconcile before saving.')
            if not head:
                conn.execute(analyses.insert().values(analysis_id=analysis_id, latest_revision_id=revision_id))
            conn.execute(versions.insert().values(revision_id=revision_id, analysis_id=analysis_id,
                parent_revision_id=previous, payload=payload, sha256=digest, actor_id=actor,
                created_at=datetime.now(UTC).isoformat()))
            if head:
                conn.execute(analyses.update().where(analyses.c.analysis_id == analysis_id)
                             .values(latest_revision_id=revision_id))
            self._event(conn, analysis_id, actor, 'planning.analysis.save', {'revision_id': revision_id, 'sha256': digest})
        return {'analysis_id': analysis_id, 'revision_id': revision_id, 'sha256': digest, 'created': True}

    def get(self, analysis_id, revision_id=None):
        with self.engine.connect() as conn:
            head = conn.execute(sa.select(analyses).where(analyses.c.analysis_id == analysis_id)).mappings().first()
            if head is None:
                return None
            row = conn.execute(sa.select(versions).where(versions.c.analysis_id == analysis_id,
                versions.c.revision_id == (revision_id or head['latest_revision_id']))).mappings().first()
        if row is None:
            return None
        result = dict(row)
        if sha(canonical(result['payload'])) != result['sha256']:
            raise ValueError('Stored analysis integrity failed.')
        self._policies(result['payload']['selected_policies'])
        result['connected_sources'] = self._links(result['payload']['linked_sources'])
        result['review_required'] = result['payload']['review_state'] != 'reviewed'
        result['is_latest'] = result['revision_id'] == head['latest_revision_id']
        return result

    def history(self, analysis_id):
        with self.engine.connect() as conn:
            ids = conn.execute(sa.select(versions.c.revision_id).where(versions.c.analysis_id == analysis_id)
                               .order_by(versions.c.created_at, versions.c.revision_id)).scalars().all()
        return [self.get(analysis_id, revision_id) for revision_id in ids]

    def inventory(self, *, limit=50, offset=0):
        """Bounded staff summaries, without proposal text or private notes."""
        if not 1 <= limit <= 100 or not 0 <= offset <= 100_000:
            raise ValueError('Use limit 1-100 and offset 0-100000.')
        with self.engine.connect() as conn:
            rows = conn.execute(sa.select(versions).join(
                analyses, versions.c.revision_id == analyses.c.latest_revision_id,
            ).order_by(versions.c.analysis_id).limit(limit + 1).offset(offset)).mappings().all()
        items = []
        for row in rows[:limit]:
            if sha(canonical(row['payload'])) != row['sha256']:
                raise ValueError('Stored analysis integrity failed.')
            items.append({**{k: row[k] for k in ('analysis_id', 'revision_id', 'sha256', 'created_at')},
                          **{k: row['payload'][k] for k in ('project_name', 'review_state', 'audience')}})
        return {'items': items, 'next_offset': offset + limit if len(rows) > limit else None}

    def snapshot_inventory(self, *, limit=50, offset=0, staff=False):
        """Permission-rechecked snapshots; unavailable rows are never cached content."""
        if not 1 <= limit <= 100 or not 0 <= offset <= 100_000:
            raise ValueError('Use limit 1-100 and offset 0-100000.')
        query = sa.select(snapshots.c.snapshot_id).order_by(snapshots.c.snapshot_id)
        if not staff:
            query = query.where(snapshots.c.visibility == 'public')
        with self.engine.connect() as conn:
            ids = conn.execute(query.limit(limit + 1).offset(offset)).scalars().all()
        items = []
        for snapshot_id in ids[:limit]:
            try:
                document = self.document(snapshot_id, staff=staff)
            except (ValueError, ConnectionUnavailable):
                continue
            if document:
                items.append(document)
        return {'items': items, 'next_offset': offset + limit if len(ids) > limit else None}

    def preview_snapshot(self, analysis_id, expected_revision, visibility):
        if visibility not in ('public', 'staff_only'):
            raise ValueError('Valid snapshot visibility required.')
        analysis = self.get(analysis_id, expected_revision)
        if analysis is None:
            raise ValueError('Analysis revision not found.')
        if not analysis['is_latest']:
            raise SourceConflict('Analysis changed; review the current revision before previewing a snapshot.')
        payload = analysis['payload']
        if payload['review_state'] != 'reviewed':
            raise ValueError('Staff review is required before a snapshot.')
        public = visibility == 'public'
        if public and (payload['audience'] != 'public' or not payload['public_summary']):
            raise ValueError('Public snapshots require a public analysis and explicitly edited public summary.')
        policies = self._policies(payload['selected_policies'], public=public)
        linked = self._links(payload['linked_sources'])
        result = {'analysis_id': analysis_id, 'analysis_revision_id': expected_revision,
                  'title': payload['project_name'], 'policy_sources': policies, 'linked_evidence': linked,
                  'review_state': payload['review_state'], 'reviewer_label': payload['reviewer_label'],
                  'reviewed_on': payload['reviewed_on'], 'disclaimer': DISCLAIMER,
                  'analysis_text': payload['public_summary'] if public else payload['analysis_text']}
        if not public:
            result.update({k: payload[k] for k in ('proposal', 'considerations', 'staff_notes', 'review_notes')})
        text = canonical(result)
        digest = sha(text)
        snapshot_id = str(uuid5(NAMESPACE_URL, f'townlight:planning:snapshot:{expected_revision}:{visibility}:{digest}'))
        return {'snapshot_id': snapshot_id, 'analysis_revision_id': expected_revision,
                'visibility': visibility, 'text': text, 'sha256': digest}

    def snapshot(self, analysis_id, expected_revision, visibility, actor):
        if not actor.strip():
            raise ValueError('Authenticated actor required.')
        preview = self.preview_snapshot(analysis_id, expected_revision, visibility)
        snapshot_id, text, digest = (preview[k] for k in ('snapshot_id', 'text', 'sha256'))
        with self.engine.begin() as conn:
            self._lock(conn, analysis_id)
            head = conn.execute(sa.select(analyses).where(analyses.c.analysis_id == analysis_id)).mappings().one()
            if head['latest_revision_id'] != expected_revision:
                raise SourceConflict('Analysis changed; review the current revision before creating a snapshot.')
            if not conn.execute(sa.select(snapshots.c.snapshot_id).where(snapshots.c.snapshot_id == snapshot_id)).first():
                conn.execute(snapshots.insert().values(snapshot_id=snapshot_id, analysis_id=analysis_id,
                    analysis_revision_id=expected_revision, visibility=visibility, text=text, sha256=digest,
                    actor_id=actor, created_at=datetime.now(UTC).isoformat()))
                self._event(conn, analysis_id, actor, 'planning.snapshot.create', {'snapshot_id': snapshot_id, 'sha256': digest})
        return self.document(snapshot_id, staff=True)

    def document(self, snapshot_id, *, staff=False):
        with self.engine.connect() as conn:
            row = conn.execute(sa.select(snapshots).where(snapshots.c.snapshot_id == snapshot_id)).mappings().first()
        if not row or (not staff and row['visibility'] != 'public'):
            return None
        payload = json.loads(row['text'])
        if sha(row['text']) != row['sha256']:
            raise ValueError('Snapshot integrity failed.')
        refs = [{k: p[k] for k in ('plan_id', 'revision_id', 'policy_id')} for p in payload['policy_sources']]
        self._policies(refs, public=row['visibility'] == 'public')
        for link in payload['linked_evidence']:
            permitted(self.providers, {'provider': link['provider'], 'source_id': link['source']['source_id'],
                                       'expected_sha256': link['source']['sha256']})
        return {'source_id': 'townlight:planning:snapshot:' + snapshot_id, 'kind': 'planning',
                'title': payload['title'], 'text': row['text'], 'sha256': row['sha256'],
                'version': snapshot_id, 'visibility': row['visibility'], 'excerpt': payload['analysis_text'][:500],
                'citation': f'Planning review snapshot {snapshot_id}; sha256={row["sha256"]}',
                'analysis_revision_id': row['analysis_revision_id']}

    def public_documents(self, query='', source_id=None):
        with self.engine.connect() as conn:
            ids = conn.execute(sa.select(snapshots.c.snapshot_id).where(snapshots.c.visibility == 'public')).scalars().all()
        result = []
        for snapshot_id in ids:
            if source_id and source_id != 'townlight:planning:snapshot:' + snapshot_id:
                continue
            try:
                doc = self.document(snapshot_id)
            except (ValueError, ConnectionUnavailable):
                continue  # Revoked evidence is unavailable, never a cached source.
            if doc and query.casefold() in (doc['title'] + ' ' + doc['text']).casefold():
                result.append(doc)
        return result

    def access_advice(self, snapshot_id):
        doc = self.document(snapshot_id, staff=True)
        if doc is None:
            raise ValueError('Snapshot not found.')
        if not callable(self.access_rewrite):
            raise ConnectionUnavailable('Access support unavailable; original snapshot retained.')
        try:
            advice = self.access_rewrite(doc['text'])
        except Exception:
            raise ConnectionUnavailable('Access support unavailable; original snapshot retained.') from None
        return {'source_id': doc['source_id'], 'source_sha256': doc['sha256'],
                'original': doc['text'], 'advice': advice,
                'review_required': True}

    def audit(self, analysis_id):
        with self.engine.connect() as conn:
            rows = conn.execute(sa.select(events).where(events.c.analysis_id == analysis_id)
                                .order_by(events.c.sequence)).mappings().all()
            stored_versions = conn.execute(sa.select(versions).where(versions.c.analysis_id == analysis_id)).mappings().all()
            stored_snapshots = conn.execute(sa.select(snapshots).where(snapshots.c.analysis_id == analysis_id)).mappings().all()
        entries = [PersistedAuditLogEntry(entry_id=r['event_id'], **{k: r[k] for k in (
            'previous_hash', 'entry_hash', 'timestamp', 'actor_id', 'action', 'details')}) for r in rows]
        ok, count, error = verify_persisted_audit_chain(entries, accept_first_previous_hash=False)
        integrity = all(sha(canonical(r['payload'])) == r['sha256'] for r in stored_versions)
        integrity = integrity and all(sha(r['text']) == r['sha256'] for r in stored_snapshots)
        return {'ok': ok and integrity and count == len(stored_versions) + len(stored_snapshots),
                'count': count, 'error': error, 'integrity': integrity}
