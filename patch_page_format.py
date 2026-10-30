# SPDX-License-Identifier: AGPL-3.0-only
"""One-shot edit: render the explorer template with placeholders, not "%" formatting.

The page's CSS legitimately contains percent signs (widths, clamp), which
"%"-formatting consumed. Placeholders make the template unambiguous.
Idempotent; retained as the record of this edit.
"""
from pathlib import Path

TASK = Path(__file__).resolve().parents[3]
target = TASK / 'work/beta-products/plan/civicplan/public_explore_ui.py'
text = target.read_text(encoding='utf-8')
start = text.index('    return """<!DOCTYPE html>')
NEW = '''    template = """<!DOCTYPE html>
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
  <label for="q">Topic, neighborhood or keyword
    <input id="q" name="q" value="[[QUERY]]" maxlength="200"
           placeholder="e.g. missing middle housing, transit corridor"></label>
  <label for="goal">Goal
    <select id="goal" name="goal">[[GOALS]]</select></label>
  <label for="topic">Topic
    <select id="topic" name="topic">[[TOPICS]]</select></label>
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
'''
target.write_text(text[:start] + NEW, encoding='utf-8')
print('rewrote', target)
