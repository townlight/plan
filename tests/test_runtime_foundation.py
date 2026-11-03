import json
import pytest
import tomllib
from pathlib import Path

from fastapi.testclient import TestClient

import townlight_planning
from townlight_planning.main import app


client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]


def test_package_development_version() -> None:
    assert townlight_planning.__version__ == "0.4.0.dev2"


def test_private_candidate_pins_tested_core_wheel() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert "townlight-core==1.3.0.dev2" in data["project"]["dependencies"]
    assert data["project"]["version"] == townlight_planning.__version__


def test_ci_workflows_use_current_townlight_core_release_wheel() -> None:
    for path in [ROOT / ".github" / "workflows" / "verify.yml", ROOT / ".github" / "workflows" / "release.yml"]:
        text = path.read_text(encoding="utf-8")
        pin = json.loads((ROOT / "config/core-source.json").read_text(encoding="utf-8"))
        assert pin["distribution"] == "townlight-core"
        assert pin["version"] == "1.3.0.dev2"
        assert len(pin["commit"]) == 40 and all(c in "0123456789abcdef" for c in pin["commit"])
        assert "python scripts/install-core-candidate.py" in text, path
        assert "core/archive/" not in text and "core/releases/download/" not in text, path
        assert "v1.0.1/townlight_core-1.0.1-py3-none-any.whl" not in text, path


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()

    assert payload["name"] == "TownlightPlanning"
    assert payload["version"] == "0.4.0.dev2"
    assert payload["status"] == "Opt-in staff beta preparation; not a published installer"
    assert "staff-only local source-bundle imports" in payload["message"]
    assert "versioned policies" in payload["message"]
    assert "does not make official planning determinations" in payload["message"]
    assert payload["next_step"].startswith("Run explicit migrations")


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "townlight_planning"
    assert payload["version"] == "0.4.0.dev2"
    assert payload["townlight_core_version"] == "1.3.0.dev2"


def test_release_gate_prefers_native_unix_python_before_windows_launcher() -> None:
    script = (ROOT / "scripts" / "verify-release.sh").read_text(encoding="utf-8")

    python3_probe = "command -v python3"
    python_probe = "command -v python)"
    assert python3_probe in script
    assert python_probe in script
    assert script.index(python3_probe) < script.index(python_probe)


def test_documentation_gate_blocks_stale_product_release_claims() -> None:
    script = (ROOT / "scripts" / "verify-docs.sh").read_text(encoding="utf-8")

    assert "v0.2.0 recovery release" in script
    assert "published v0.2.0 recovery label" in script
    assert "current product release" in script
    assert "Townlight Beta 1" in script


def test_current_docs_mark_corrective_demotion_without_overclaim() -> None:
    docs = {
        "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
        "README.txt": (ROOT / "README.txt").read_text(encoding="utf-8"),
        "USER-MANUAL.md": (ROOT / "USER-MANUAL.md").read_text(encoding="utf-8"),
        "USER-MANUAL.txt": (ROOT / "USER-MANUAL.txt").read_text(encoding="utf-8"),
        "docs/index.html": (ROOT / "docs" / "index.html").read_text(encoding="utf-8"),
    }

    for path, text in docs.items():
        lowered = " ".join(text.lower().split())
        assert "townlight beta 1" in lowered, path
        assert "0.4.0.dev2" in lowered, path
        assert "demoted recovery label" not in lowered, path
        assert "review" in lowered, path
        assert "agpl-3.0" in lowered, path


@pytest.fixture(autouse=True)
def explicit_sample_mode(monkeypatch):
    monkeypatch.setenv("TOWNLIGHT_PLANNING_DEMO_MODE", "1")
