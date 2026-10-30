# SPDX-License-Identifier: AGPL-3.0-only
"""One-shot edit: align the existing public-UI test with the required change.

The beta requirement is that the public Planning page stop being an *explicit
static sample* and instead explore persisted adopted public plan sources. The old
assertions pinned the sample's own strings, so they now assert the opposite of
the requirement. This rewrites that one test to assert the honest behaviour that
replaced it: with no source database the page states it is unavailable and shows
no sample plan text; with persisted sources it renders citations (which
``tests/test_public_explore.py`` covers in depth).

Idempotent; retained as the record of this edit.
"""
from pathlib import Path

TASK = Path(__file__).resolve().parents[3]
target = TASK / 'work/beta-products/plan/tests/test_planning_foundation.py'
text = target.read_text(encoding='utf-8')
start = text.index('def test_public_ui_route_is_accessible_and_honest() -> None:')
end = text.index('@pytest.fixture(autouse=True)')
NEW = '''def test_public_ui_route_is_accessible_and_honest(monkeypatch) -> None:
    """The public page may never present sample text as if it were an adopted plan.

    With no plan source database configured the honest answer is "not available";
    with sources configured the page renders citations from them (covered in
    ``tests/test_public_explore.py``). Either way, no static sample survives.
    """

    monkeypatch.delenv("CIVICPLAN_POLICY_DB_URL", raising=False)
    response = client.get("/civicplan")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    text = response.text
    assert "<main id=\\"main\\">" in text
    assert "not available" in text.lower()
    # The replaced sample's own prose and its "static sample" badge are gone.
    for gone in ("0.3.0+dev.1 explicit static sample", "Static sample proposal",
                 "Housing proposal context", "Plan navigator", "Progress tracking"):
        assert gone not in text, gone
    # The boundary statement is still made: this product never decides.
    assert "sample text" in text.lower() or "does not make" in text.lower()
    assert "certified ADA" not in text


'''
target.write_text(text[:start] + NEW + text[end:], encoding='utf-8')
print('patched', target)
