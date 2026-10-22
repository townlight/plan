"""Versioned, cited policy retrieval. Deterministic evidence, never determinations."""
from datetime import date
import re

import sqlalchemy as sa

from civicplan.policy_lookup import DISCLAIMER
from civicplan.source_schema import revisions

STOP = frozenset('a an and are as at be by can do does for from how i in is it may of on or our plan policy policies should that the their this to under us what when where which who will with would'.split())


def words(value):
    return set(re.findall(r"[\w-]+", value.casefold())) - STOP


def evidence(revision, policy):
    document = next(d for d in revision['documents'] if d['document_id'] == policy['document_id'])
    revision_id = revision['revision_id']
    return {**{k: v for k, v in policy.items() if k != 'revision_id'},
            **{k: revision[k] for k in ('plan_id', 'plan_type', 'visibility', 'bundle_sha256')},
            'revision_id': revision_id, 'plan_title': revision['title'],
            **{k: revision[k].isoformat() for k in ('source_date', 'adopted_on', 'effective_on')},
            'source_sha256': document['sha256'], 'filename': document['filename'],
            'source_location': (f'/api/v1/civicplan/policy-sources/{revision_id}/documents/{document["document_id"]}'
                                if revision['visibility'] == 'public' else
                                f'/api/v1/civicplan/source-revisions/{revision_id}/documents/{document["document_id"]}'),
            'disclaimer': DISCLAIMER}


class PolicyService:
    def __init__(self, sources):
        self.sources = sources

    def active_revisions(self, *, as_of=None):
        as_of = as_of or date.today()
        with self.sources.engine.connect() as conn:
            rows = conn.execute(sa.select(revisions).order_by(revisions.c.sequence)).mappings()
            active = {}
            for row in rows:
                if row['status'] != 'pending' and (row['effective_on'] or row['source_date']) <= as_of:
                    active[row['plan_id']] = dict(row)
            return active

    def resolve(self, revision_id, policy_id, *, staff=False):
        revision = self.sources.revision(revision_id, staff=staff)
        if revision is None or revision['dataset_kind'] != 'municipal':
            raise ValueError('Policy source unavailable for this audience.')
        if revision['status'] != 'adopted' or revision['effective_on'] > date.today():
            raise ValueError('Select an effective adopted policy revision.')
        if not staff and not self.public_permitted(revision_id):
            raise ValueError('Policy source is no longer public.')
        policy = next((p for p in revision['policies'] if p['policy_id'] == policy_id), None)
        if policy is None:
            raise ValueError('Policy is not present in the selected revision.')
        return evidence(revision, policy)

    def public_permitted(self, revision_id):
        revision = self.sources.revision(revision_id)
        if (revision is None or revision['status'] != 'adopted'
                or revision['effective_on'] > date.today()):
            return False
        current = self.active_revisions().get(revision['plan_id'])
        return bool(current and current['visibility'] == 'public' and current['dataset_kind'] == 'municipal')

    def current(self, *, staff=False, plan_type=None):
        result = []
        for row in self.active_revisions().values():
            if row['status'] != 'adopted' or row['dataset_kind'] != 'municipal':
                continue
            if not staff and row['visibility'] != 'public':
                continue
            if plan_type and row['plan_type'] != plan_type.casefold():
                continue
            revision = self.sources.revision(row['revision_id'], staff=staff)
            result.extend(evidence(revision, p) for p in revision['policies'])
        return sorted(result, key=lambda p: (p['plan_id'], p['policy_id']))

    def answer(self, query, *, staff=False, plan_type=None):
        terms = words(query)
        candidates = self.current(staff=staff, plan_type=plan_type)
        matches = [p for p in candidates if query.casefold().strip() == p['policy_id'].casefold()
                   or terms & words(' '.join(p[k] for k in ('topic_key', 'title', 'goal', 'objective', 'excerpt')))]
        ambiguous = len(matches) > 1
        return {'status': 'needs_review' if ambiguous else 'answered' if matches else 'no_supported_policy',
                'answer': '\n\n'.join(f'{p["citation"]} ({p["anchor"]}): {p["excerpt"]}' for p in matches),
                'sources': matches, 'citations': [p['citation'] for p in matches],
                'source_policy_ids': [p['policy_id'] for p in matches],
                'review_required': True, 'disclaimer': DISCLAIMER,
                'review_task': {'reason': 'Multiple source excerpts may overlap or conflict; staff must reconcile applicability.',
                                'source_references': [{k: p[k] for k in ('plan_id', 'revision_id', 'policy_id')} for p in matches]}
                               if ambiguous else None}

    def navigator(self, *, staff=False, plan_type=None):
        plans = {}
        for p in self.current(staff=staff, plan_type=plan_type):
            node = plans.setdefault(p['plan_id'], {'plan_id': p['plan_id'], 'title': p['plan_title'],
                    'plan_type': p['plan_type'], 'revision_id': p['revision_id'], 'goals': {}})
            node['goals'].setdefault(p['goal'], {}).setdefault(p['objective'], []).append(p)
        for node in plans.values():
            node['goals'] = [{'title': g, 'objectives': [{'title': o, 'policies': ps} for o, ps in os.items()]}
                             for g, os in node['goals'].items()]
        return {'plans': list(plans.values()), 'review_required': True, 'disclaimer': DISCLAIMER}
