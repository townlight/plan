# SPDX-License-Identifier: AGPL-3.0-only
"""Public plan exploration over *persisted* adopted plan sources.

The public Planning page previously rendered an explicit static sample: fixed
prose that was not read from any stored plan. This module turns the page into an
exploration of the plan sources Planning actually holds: adopted, effective,
public revisions only, navigable by plan, goal, objective, topic and free text,
with every result carrying its citation and source document.

Boundaries this module keeps, deliberately:

* it reads through :class:`civicplan.policy_service.PolicyService`, so the
  public/staff revision rule is enforced in one place -- a staff-only revision
  is never rendered here, and asking for one by id is refused;
* it explores and cites; it never determines consistency, entitlement or
  compliance, and every payload keeps the service's ``review_required`` flag and
  disclaimer;
* neighborhood applicability comes from staff-verified imported policy metadata,
  never inferred from a keyword, parcel, GIS or address lookup.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from civicplan.policy_service import PolicyService, words

#: How much of an excerpt the public list shows before the reader opens the
#: citation. Full text is always available from the cited source document.
EXCERPT_CHARS = 320


@dataclass(frozen=True)
class Exploration:
    """One exploration request and what the persisted sources support for it."""

    query: str = ''
    plan_type: str = ''
    goal: str = ''
    topic: str = ''
    neighborhood: str = ''
    plans: list = field(default_factory=list)
    total: int = 0
    review_required: bool = True
    disclaimer: str = ''
    empty_reason: str | None = None
    #: Dimensions actually offered by the stored sources, so the page can only
    #: offer filters that are backed by data.
    facets: dict = field(default_factory=dict)

    @property
    def is_empty(self) -> bool:
        return not self.plans


def _norm(value: str | None) -> str:
    return (value or '').strip().casefold()


def _matches(policy, *, terms, goal, topic, plan_type, neighborhood) -> bool:
    if neighborhood and _norm(neighborhood) not in {_norm(n) for n in policy.get('neighborhoods', [])}:
        return False
    if plan_type and _norm(policy['plan_type']) != _norm(plan_type):
        return False
    if goal and _norm(policy['goal']) != _norm(goal):
        return False
    if topic and _norm(policy['topic_key']) != _norm(topic):
        return False
    if not terms:
        return True
    haystack = ' '.join(str(policy.get(key) or '') for key in
                        ('topic_key', 'title', 'goal', 'objective', 'citation', 'excerpt'))
    return bool(terms & words(haystack))


def explore(service: PolicyService, *, query: str = '', plan_type: str = '',
            goal: str = '', topic: str = '', neighborhood: str = '', staff: bool = False) -> Exploration:
    """Explore adopted plan policies the requesting audience may see.

    ``staff=False`` is the public path: only public, adopted, currently effective
    municipal revisions are reachable, and an unpublished revision cannot be
    reached by naming it.
    """
    navigator = service.navigator(staff=staff, plan_type=plan_type or None)
    terms = words(query) if query else set()
    plans = []
    total = 0
    for plan in navigator['plans']:
        goals = []
        for goal_node in plan['goals']:
            objectives = []
            for objective_node in goal_node['objectives']:
                policies = [p for p in objective_node['policies']
                            if _matches(p, terms=terms, goal=goal, topic=topic,
                                        plan_type=plan_type, neighborhood=neighborhood)]
                if not policies:
                    continue
                total += len(policies)
                objectives.append({'title': objective_node['title'], 'policies': policies})
            if objectives:
                goals.append({'title': goal_node['title'], 'objectives': objectives})
        if goals:
            plans.append({**{k: plan[k] for k in ('plan_id', 'title', 'plan_type', 'revision_id')},
                          'goals': goals})
    facets = _facets(navigator['plans'])
    reason = None
    if not plans:
        if not navigator['plans']:
            reason = ('No adopted public plan source is loaded. Staff import a '
                      'staff-verified plan bundle before anything appears here.')
        else:
            reason = ('No adopted public policy matches %s. Try a broader term, '
                      'or clear the filters to see everything published.') % _describe(
                          query=query, goal=goal, topic=topic, plan_type=plan_type, neighborhood=neighborhood)
    return Exploration(query=query, plan_type=plan_type, goal=goal, topic=topic,
                       neighborhood=neighborhood,
                       plans=plans, total=total, review_required=True,
                       disclaimer=navigator['disclaimer'], empty_reason=reason,
                       facets=facets)


def _describe(*, query, goal, topic, plan_type, neighborhood) -> str:
    """Name what was actually asked, so an empty result is checkable."""
    parts = [f'"{query}"' if query else '', f'goal "{goal}"' if goal else '',
             f'topic "{topic}"' if topic else '',
             f'neighborhood "{neighborhood}"' if neighborhood else '',
             f'plan type "{plan_type}"' if plan_type else '']
    asked = ', '.join(part for part in parts if part)
    return asked or 'the current filters'


def _facets(navigator_plans) -> dict:
    goals, topics, plans, types, neighborhoods = set(), set(), [], set(), set()
    for plan in navigator_plans:
        plans.append({'plan_id': plan['plan_id'], 'title': plan['title']})
        types.add(plan['plan_type'])
        for goal in plan['goals']:
            goals.add(goal['title'])
            for objective in goal['objectives']:
                for policy in objective['policies']:
                    topics.add(policy['topic_key'])
                    neighborhoods.update(policy.get('neighborhoods', []))
    return {'goals': sorted(goals), 'topics': sorted(topics), 'plans': plans,
            'plan_types': sorted(types), 'neighborhoods': sorted(neighborhoods)}


def resolve_public_policy(service: PolicyService, revision_id: str, policy_id: str):
    """Resolve one policy for a public reader, or refuse.

    A staff-only or superseded revision is refused by the service, not by the
    caller, so the public boundary cannot be bypassed by naming an id.
    """
    return service.resolve(revision_id, policy_id, staff=False)


def excerpt(policy, limit: int = EXCERPT_CHARS) -> str:
    text = re.sub(r'\s+', ' ', str(policy.get('excerpt') or '')).strip()
    return text if len(text) <= limit else text[:limit].rsplit(' ', 1)[0] + '…'
