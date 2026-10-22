import pytest
import tomllib
from pathlib import Path

from fastapi.testclient import TestClient

import civicplan
from civicplan.main import app


client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]


def test_package_development_version() -> None:
    assert civicplan.__version__ == "0.3.0+dev.1"


def test_pyproject_uses_published_civiccore_release_wheel() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = data["project"]["dependencies"]

    assert data["tool"]["hatch"]["metadata"]["allow-direct-references"] is True
    assert (
        "civiccore @ https://github.com/townlight/core/releases/download/"
        "v1.2.1/civiccore-1.2.1-py3-none-any.whl#sha256=8dde29408e206048bde63ec14156a8e6329382af4d16b12710d12aa5c27f3f59"
    ) in dependencies
    assert "civiccore==1.0.0" not in dependencies


def test_ci_workflows_use_current_civiccore_release_wheel() -> None:
    for path in [ROOT / ".github" / "workflows" / "verify.yml", ROOT / ".github" / "workflows" / "release.yml"]:
        text = path.read_text(encoding="utf-8")
        assert "v1.2.1/civiccore-1.2.1-py3-none-any.whl" in text, path
        assert "v1.0.1/civiccore-1.0.1-py3-none-any.whl" not in text, path


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()

    assert payload["name"] == "CivicPlan"
    assert payload["version"] == "0.3.0+dev.1"
    assert payload["status"] == "P3/P4 development workflows; not an installed public beta"
    assert "staff-only local source-bundle imports" in payload["message"]
    assert "versioned policies" in payload["message"]
    assert "does not make official planning determinations" in payload["message"]
    assert payload["next_step"].startswith("Run explicit migrations")


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "civicplan"
    assert payload["version"] == "0.3.0+dev.1"
    assert payload["civiccore_version"] == "1.2.1"


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
    assert "0.3.0+dev.1 P3/P4 development workflows" in script


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
        assert "0.3.0+dev.1 p3/p4 development workflows" in lowered, path
        assert "previous v1.0.0 release was published in error" in lowered, path
        assert "demoted recovery label" not in lowered, path
        assert "official planning determinations" in lowered, path


@pytest.fixture(autouse=True)
def explicit_sample_mode(monkeypatch):
    monkeypatch.setenv("CIVICPLAN_DEMO_MODE", "1")
