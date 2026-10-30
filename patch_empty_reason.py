# SPDX-License-Identifier: AGPL-3.0-only
"""One-shot edit: make the empty exploration state name what was asked.

An empty result must be checkable: the page has to say which query, goal, topic or
plan type produced nothing, so a reader (and an acceptance run) can tell an honest
empty result from a broken filter. Idempotent; retained as the record of this edit.
"""
from pathlib import Path

TASK = Path(__file__).resolve().parents[3]
target = TASK / 'work/beta-products/plan/civicplan/public_explore.py'
text = target.read_text(encoding='utf-8')
old = """            reason = ('No adopted public policy matches this exploration. Try a '
                      'broader term, or clear the filters to see everything published.')"""
new = """            reason = ('No adopted public policy matches %s. Try a broader term, '
                      'or clear the filters to see everything published.') % _describe(
                          query=query, goal=goal, topic=topic, plan_type=plan_type)"""
describe = '''def _describe(*, query, goal, topic, plan_type) -> str:
    """Name what was actually asked, so an empty result is checkable."""
    parts = [f'"{query}"' if query else '', f'goal "{goal}"' if goal else '',
             f'topic "{topic}"' if topic else '',
             f'plan type "{plan_type}"' if plan_type else '']
    asked = ', '.join(part for part in parts if part)
    return asked or 'the current filters'


def _facets('''
if old in text and '_describe' not in text:
    text = text.replace(old, new).replace('def _facets(', describe, 1)
    target.write_text(text, encoding='utf-8')
    print('patched', target)
else:
    print('already patched' if '_describe' in text else 'PATTERN NOT FOUND')
