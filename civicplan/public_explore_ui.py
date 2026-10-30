# SPDX-License-Identifier: AGPL-3.0-only
"""Server-rendered public plan exploration page.

The page renders only what :mod:`civicplan.public_explore` derived from stored,
adopted, effective, public plan revisions. It has no client-side data source, no
embedded sample content, and no state of its own: every view is a GET of this
page with query parameters, so the public surface cannot diverge from the
persisted sources and works without JavaScript.

Accessibility and honesty constraints kept here: real ``<form>`` with a submit
button, labelled controls, ``<main>`` and heading order, visible text for every
citation, an explicit empty state, and the review-required boundary stated on
every page.
"""
from __future__ import annotations

from html import escape

from civicplan.public_explore import excerpt

STYLE = """
:root{--ink:#17202a;--muted:#4d5a63;--paper:#fffdf8;--blue:#184d70;--green:#2f6b50;
--line:#cbd6d0;--gold:#b57f14}
*{box-sizing:border-box}body{margin:0;color:var(--ink);background:#f4f7f5;
font-family:"Segoe UI",Aptos,sans-serif;line-height:1.6}
header,main,footer{width:min(1080px,calc(100% - 32px));margin:0 auto}
header{padding:36px 0 18px}a{color:var(--blue)}h1{font-size:clamp(1.9rem,4vw,2.6rem);margin:.2rem 0 .6rem}
.eyebrow{text-transform:uppercase;letter-spacing:.16em;font-size:.75rem;font-weight:800;color:var(--blue)}
.lede{max-width:72ch;color:#2b3a43}
form.explore{display:flex;flex-wrap:wrap;gap:14px;align-items:end;margin:22px 0;
padding:20px;border:1px solid var(--line);border-radius:18px;background:var(--paper)}
label{display:grid;gap:6px;font-weight:700;font-size:.9rem;min-width:12rem;flex:1}
input,select,button{font:inherit;padding:11px;border:1px solid #7f938c;border-radius:8px;min-height:44px;background:#fff}
button{background:var(--blue);color:#fff;font-weight:700;cursor:pointer;align-self:end}
button.secondary{background:#e9efec;color:var(--ink)}
:focus-visible{outline:3px solid var(--gold);outline-offset:3px}
.result-count{margin:18px 0 0;font-weight:700}
.plan{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:22px;margin:18px 0}
.goal{margin:16px 0 0;padding-left:14px;border-left:4px solid var(--green)}
.objective{margin:12px 0 0;padding-left:12px;border-left:2px solid #d8e2dd}
.policy{border-top:1px solid #e4ece8;padding-top:12px;margin-top:12px}
.citation{font-weight:800;color:var(--blue)}
.anchor{color:var(--muted);font-size:.9rem}
.excerpt{margin:.45rem 0;max-width:78ch}
.empty{padding:22px;border:1px dashed var(--gold);border-radius:16px;background:#fffbef}
.boundary{margin:26px 0 0;padding:16px;border-radius:14px;background:#eef3f0;color:#22343b}
dl.facets{display:grid;grid-template-columns:max-content 1fr;gap:6px 16px;font-size:.92rem}
dl.facets dt{font-weight:800}dl.facets dd{margin:0}
footer{padding:30px 0 48px;color:var(--muted);font-size:.9rem}
@media(max-width:640px){form.explore{flex-direction:column;align-items:stretch}label{min-width:0}}
"""


def _option(value: str, label: str, chosen: str) -> str:
    selected = ' selected' if value == chosen else ''
    return f'<option value="{escape(value)}"{selected}>{escape(label)}</option>'


def render_explorer(exploration) -> str:
    """Render one exploration result set. Pure: no I/O, no client state."""
    facets = exploration.facets
    rows = []
    for plan in exploration.plans:
        goal_blocks = []
        for goal in plan['goals']:
            objective_blocks = []
            for objective in goal['objectives']:
                policy_blocks = []
                for policy in objective['policies']:
                    policy_blocks.append(
                        '<div class="policy" data-policy="%s">'
                        '<p class="citation">%s</p>'
                        '<p class="anchor">%s</p>'
                        '<p class="excerpt">%s</p>'
                        '<p class="anchor">Adopted %s · source document %s '
                        '(<a href="%s">cited source</a>)</p></div>' % (
                            escape(policy['policy_id']), escape(policy['citation']),
                            escape(policy['anchor']), escape(excerpt(policy)),
                            escape(policy['adopted_on']), escape(policy['filename']),
                            escape(policy['source_location'])))
                objective_blocks.append('<div class="objective"><h5>%s</h5>%s</div>' % (
                    escape(objective['title']), ''.join(policy_blocks)))
            goal_blocks.append('<div class="goal"><h4>%s</h4>%s</div>' % (
                escape(goal['title']), ''.join(objective_blocks)))
        rows.append('<article class="plan" data-plan="%s"><h3>%s</h3>'
                    '<p class="anchor">%s plan · revision %s</p>%s</article>' % (
                        escape(plan['plan_id']), escape(plan['title']),
                        escape(plan['plan_type']), escape(plan['revision_id']),
                        ''.join(goal_blocks)))
    if rows:
        body = ('<p class="result-count" role="status">%d adopted public polic%s across '
                '%d plan%s.</p>%s') % (exploration.total,
                                       'y' if exploration.total == 1 else 'ies',
                                       len(exploration.plans),
                                       '' if len(exploration.plans) == 1 else 's',
                                       ''.join(rows))
    else:
        body = ('<div class="empty" role="status"><p><strong>Nothing to show.</strong></p>'
                '<p>%s</p></div>') % escape(exploration.empty_reason or 'No adopted public policy matched.')
    facet_list = ''.join(
        '<dt>%s</dt><dd>%s</dd>' % (escape(title), escape(', '.join(values)))
        for title, values in (('Plans', [p['title'] for p in facets['plans']]),
                              ('Plan types', facets['plan_types']),
                              ('Goals', facets['goals']), ('Topics', facets['topics']),
                              ('Neighborhoods', facets['neighborhoods']))
        if values)
    template = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Townlight Planning · Adopted plan exploration</title>
<style>[[STYLE]]</style></head><body>
<header><p class="eyebrow">Townlight Planning</p>
<h1>Explore the adopted plan</h1>
<p class="lede">Search adopted comprehensive-plan text by topic, neighborhood, goal or
plan. Every result is a citation to a stored, adopted, currently effective plan
revision, with its source document. This page explores and cites; it does not make
planning, zoning or legal determinations.</p></header>
<main id="main">
<form class="explore" method="get" action="/civicplan">
  <label for="q">Keyword
    <input id="q" name="q" value="[[QUERY]]" maxlength="200"
           placeholder="e.g. missing middle housing, transit corridor"></label>
  <label for="goal">Goal
    <select id="goal" name="goal">[[GOALS]]</select></label>
  <label for="topic">Topic
    <select id="topic" name="topic">[[TOPICS]]</select></label>
  <label for="neighborhood">Neighborhood
    <select id="neighborhood" name="neighborhood">[[NEIGHBORHOODS]]</select></label>
  <label for="plan_type">Plan type
    <select id="plan_type" name="plan_type">[[PLAN_TYPES]]</select></label>
  <button type="submit">Explore adopted plan</button>
  <button type="submit" class="secondary" name="clear" value="1">Clear filters</button>
</form>
[[BODY]]
<p class="boundary">Review required: a planner of record must confirm facts,
procedures and official findings before any decision. Multiple excerpts may
overlap or conflict.</p>
<dl class="facets">[[FACETS]]</dl>
</main>
<footer><p>Townlight Planning · AGPL-3.0 · Cited public plan exploration.
Staff-only revisions are not shown here.</p></footer>
</body></html>"""
    values = {
        '[[STYLE]]': STYLE,
        '[[QUERY]]': escape(exploration.query),
        '[[GOALS]]': _option('', 'Any goal', exploration.goal)
        + ''.join(_option(g, g, exploration.goal) for g in facets['goals']),
        '[[TOPICS]]': _option('', 'Any topic', exploration.topic)
        + ''.join(_option(t, t, exploration.topic) for t in facets['topics']),
        '[[NEIGHBORHOODS]]': _option('', 'Any neighborhood', exploration.neighborhood)
        + ''.join(_option(n, n, exploration.neighborhood) for n in facets['neighborhoods']),
        '[[PLAN_TYPES]]': _option('', 'Any plan type', exploration.plan_type)
        + ''.join(_option(t, t, exploration.plan_type) for t in facets['plan_types']),
        '[[BODY]]': body,
        '[[FACETS]]': facet_list,
    }
    for marker, value in values.items():
        template = template.replace(marker, value)
    return template


def render_unavailable(reason: str) -> str:
    """Render the honest unavailable state (no database configured, etc.)."""

    page = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Townlight Planning · Adopted plan exploration unavailable</title>
<style>[[STYLE]]</style></head><body>
<header><p class="eyebrow">Townlight Planning</p>
<h1>Adopted plan exploration is not available</h1></header>
<main id="main"><div class="empty" role="status"><p>[[REASON]]</p></div>
<p class="boundary">This page only ever shows stored, adopted, effective plan
revisions. It never substitutes sample text for a plan the city has not loaded.</p></main>
<footer><p>Townlight Planning - AGPL-3.0</p></footer></body></html>"""
    return page.replace('[[STYLE]]', STYLE).replace('[[REASON]]', escape(reason))
