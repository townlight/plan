"""Explicit fictional source bundles; never loaded by application startup."""

import base64
import hashlib


def bundle(plan_type="comprehensive", **changes):
    text = "Fictional Redstone Valley plan. Preserve housing choice near civic services."
    raw = text.encode()
    result = {
        "plan_id": "redstone-" + plan_type, "title": "Fictional Redstone Valley Plan",
        "jurisdiction": "Fictional Redstone Valley", "plan_type": plan_type,
        "status": "adopted", "visibility": "public", "source_date": "2026-01-01",
        "adopted_on": "2026-02-01", "effective_on": "2026-03-01",
        "change_note": "Initial test adoption", "reviewer_label": "Fictional Planner",
        "documents": [{"document_id": "plan", "filename": "plan.txt", "media_type": "text/plain",
                       "sha256": hashlib.sha256(raw).hexdigest(),
                       "content_base64": base64.b64encode(raw).decode()}],
        "policies": [{"policy_id": "H-1", "document_id": "plan", "goal": "Housing choice",
                      "objective": "Access to services", "topic_key": "housing", "title": "Housing policy",
                      "citation": "Fictional Plan, H-1", "anchor": "paragraph 1",
                      "excerpt": "Preserve housing choice near civic services.",
                      "relevance": "Staff confirm applicability.", "staff_verified": True}],
        "adoption_evidence": [{"kind": "manual-record", "reference": "Fictional adoption record 26-1",
                               "document_id": "plan", "note": "Test-only staff-recorded adoption."}],
    }
    result.update(changes)
    return result
