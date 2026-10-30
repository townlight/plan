# SPDX-License-Identifier: AGPL-3.0-only
"""One-shot edit: make /civicplan a live exploration of persisted plan sources.

Replaces the explicit static sample page with the server-rendered explorer and
adds JSON endpoints over the same service (so the browser and API provably agree),
plus a staff-vs-public revision boundary endpoint.

Idempotent; retained as the record of this edit.
"""
from pathlib import Path

TASK = Path(__file__).resolve().parents[3]
target = TASK / 'work/beta-products/plan/civicplan/main.py'
text = target.read_text(encoding='utf-8')

OLD_ROUTE = '''@app.get("/civicplan", response_class=HTMLResponse)
def public_civicplan_page() -> str:
    """Return the public sample plan-policy lookup UI."""

    return render_public_lookup_page()'''

NEW_ROUTE = '''@app.get("/civicplan", response_class=HTMLResponse)
def public_civicplan_page(
    q: str = "", goal: str = "", topic: str = "", plan_type: str = "", clear: str = ""
) -> str:
    """Explore the adopted plan sources this deployment actually holds.

    Public readers get only adopted, effective, public municipal revisions. When
    no plan database is configured the page says so instead of showing sample text.
    """

    if clear:
        q = goal = topic = plan_type = ""
    if _policy_database_url() is None:
        return render_unavailable(
            "No plan source database is configured for this deployment, so there are "
            "no adopted plan policies to explore yet.")
    try:
        with _sources() as repo:
            exploration = explore(PolicyService(repo), query=q, goal=goal, topic=topic,
                                  plan_type=plan_type, staff=False)
    except Exception:  # noqa: BLE001 - any source failure must not become sample text
        return render_unavailable(
            "The adopted plan sources could not be read just now. Nothing is shown "
            "rather than stale or sample plan text.")
    return render_explorer(exploration)


@app.get("/api/v1/civicplan/public/plan-explore")
def public_plan_explore(q: str = "", goal: str = "", topic: str = "",
                        plan_type: str = "") -> dict[str, object]:
    """The same persisted-source exploration as the page, as JSON."""

    if _policy_database_url() is None:
        raise HTTPException(503, "No plan source database is configured for this deployment.")
    with _sources() as repo:
        exploration = explore(PolicyService(repo), query=q, goal=goal, topic=topic,
                              plan_type=plan_type, staff=False)
    return {"query": exploration.query, "plan_type": exploration.plan_type,
            "goal": exploration.goal, "topic": exploration.topic,
            "total": exploration.total, "plans": exploration.plans,
            "facets": exploration.facets, "empty_reason": exploration.empty_reason,
            "review_required": True, "disclaimer": exploration.disclaimer}


@app.get("/api/v1/civicplan/public/policy/{revision_id}/{policy_id}")
def public_policy_citation(revision_id: str, policy_id: str) -> dict[str, object]:
    """One cited policy for a public reader, or a refusal.

    A staff-only, pending, superseded or non-effective revision is refused here by
    the service; naming its id does not reach it.
    """

    if _policy_database_url() is None:
        raise HTTPException(503, "No plan source database is configured for this deployment.")
    with _sources() as repo:
        service = PolicyService(repo)
        try:
            policy = resolve_public_policy(service, revision_id, policy_id)
        except ValueError as exc:
            raise HTTPException(404, str(exc)) from None
        return {**policy, 'review_required': True}'''

if OLD_ROUTE in text and 'public_plan_explore' not in text:
    text = text.replace(OLD_ROUTE, NEW_ROUTE)
    text = text.replace(
        'from civicplan.public_ui import render_public_lookup_page',
        'from civicplan.public_explore import explore, resolve_public_policy\n'
        'from civicplan.public_explore_ui import render_explorer, render_unavailable')
    target.write_text(text, encoding='utf-8')
    print('patched', target)
else:
    print('already patched' if 'public_plan_explore' in text else 'PATTERN NOT FOUND')
