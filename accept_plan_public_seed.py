# SPDX-License-Identifier: AGPL-3.0-only
"""Seed synthetic fictional plan sources for the Planning public acceptance.

Two adopted public plans and one staff-only plan, each with real source documents
whose text contains the cited excerpts (the source-integrity rule). Uses only
Planning's own source store against the configured database.
"""
import base64
import hashlib
import json
import os
import sys
from pathlib import Path

from civicplan.migrations import source_engine
from civicplan.source_bundle import PlanBundle
from civicplan.source_store import PlanSourceRepository

ROOT = Path(sys.argv[1]).resolve()


def document(paragraphs):
    text = '\n\n'.join(paragraphs) + '\n'
    raw = text.encode()
    return {'document_id': 'plan', 'filename': 'plan.txt', 'media_type': 'text/plain',
            'sha256': hashlib.sha256(raw).hexdigest(),
            'content_base64': base64.b64encode(raw).decode()}


HOUSING_EXCERPT = ('Encourage missing-middle housing within walking distance of transit, '
                   'schools, parks and daily services.')
TRANSIT_EXCERPT = ('Prioritize pedestrian crossings and transit stop access on corridors '
                   'serving schools and civic buildings.')
INTERNAL_EXCERPT = 'Staff-only working draft about housing on the east corridor.'


def bundle(plan_id, title, policies, visibility='public'):
    paragraphs = ['Fictional synthetic plan used only for acceptance testing.']
    paragraphs += [policy['excerpt'] for policy in policies]
    return {'plan_id': plan_id, 'title': title, 'jurisdiction': 'Fictional Testville',
            'plan_type': 'comprehensive', 'status': 'adopted', 'visibility': visibility,
            'source_date': '2026-01-01', 'adopted_on': '2026-02-01',
            'effective_on': '2026-03-01', 'change_note': 'Synthetic acceptance adoption',
            'reviewer_label': 'Fictional Planner', 'documents': [document(paragraphs)],
            'policies': policies,
            'adoption_evidence': [{'kind': 'manual-record',
                                   'reference': 'Fictional adoption record',
                                   'document_id': 'plan',
                                   'note': 'Synthetic staff-recorded adoption for testing.'}]}


def policy(policy_id, document_id, goal, objective, topic, title, citation, anchor, excerpt):
    return {'policy_id': policy_id, 'document_id': document_id, 'goal': goal,
            'objective': objective, 'topic_key': topic, 'title': title,
            'citation': citation, 'anchor': anchor, 'excerpt': excerpt,
            'relevance': 'Staff confirm applicability.', 'staff_verified': True}


def main():
    engine = source_engine(os.environ['CIVICPLAN_POLICY_DB_URL'])
    repo = PlanSourceRepository(engine)
    try:
        imported = {}
        for plan_id, title, items in (
            ('testville-comprehensive', 'Fictional Testville Comprehensive Plan', [
                policy('H-1', 'plan', 'Housing choice', 'Access to services', 'housing',
                       'Missing-middle housing near services',
                       'Comprehensive Plan, Housing Element, Policy H-1', 'paragraph 2',
                       HOUSING_EXCERPT),
            ]),
            ('testville-mobility', 'Fictional Testville Mobility Plan', [
                policy('M-3', 'plan', 'Safe streets', 'Pedestrian access', 'transportation',
                       'Transit corridor access',
                       'Mobility Plan, Policy M-3', 'paragraph 2', TRANSIT_EXCERPT),
            ]),
        ):
            imported[plan_id] = repo.import_bundle(
                PlanBundle.model_validate(bundle(plan_id, title, items)),
                actor_id='fixture-importer')
        # A staff-only plan. The public surface must never show it.
        imported['testville-internal'] = repo.import_bundle(
            PlanBundle.model_validate(bundle(
                'testville-internal', 'Fictional Testville Internal Working Plan', [
                    policy('INTERNAL-1', 'plan', 'Internal working goal', 'Draft objective',
                           'internal', 'Internal draft', 'Internal Plan, INTERNAL-1',
                           'paragraph 2', INTERNAL_EXCERPT)], visibility='staff')),
            actor_id='fixture-importer')
        (ROOT / 'seeded-sources.json').write_text(json.dumps(imported, indent=2), encoding='utf-8')
        print(json.dumps(imported))
    finally:
        engine.dispose()


if __name__ == '__main__':
    main()
