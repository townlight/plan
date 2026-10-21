import tomllib
from pathlib import Path

from fastapi.testclient import TestClient

import civicplan
from civicplan.main import app


client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]


def test_package_version_is_100() -> None:
    assert civicplan.__version__ == "0.2.2"


def test_pyproject_uses_published_civiccore_release_wheel() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = data["project"]["dependencies"]

    assert data["tool"]["hatch"]["metadata"]["allow-direct-references"] is True
    assert (
        "civiccore @ https://github.com/CivicSuite/civiccore/releases/download/"
        "v1.1.0/civiccore-1.1.0-py3-none-any.whl#sha256=3ab146f4fea2ae99640d5b1b013be1a9676de5f91b783eaeaa913043a2ae2b87"
    ) in dependencies
    assert "civiccore==1.0.0" not in dependencies


def test_ci_workflows_use_current_civiccore_release_wheel() -> None:
    for path in [ROOT / ".github" / "workflows" / "verify.yml", ROOT / ".github" / "workflows" / "release.yml"]:
        text = path.read_text(encoding="utf-8")
        assert "v1.1.0/civiccore-1.1.0-py3-none-any.whl" in text, path
        assert "v1.0.1/civiccore-1.0.1-py3-none-any.whl" not in text, path


def test_root_endpoint_states_runtime_boundary() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()

    assert payload["name"] == "CivicPlan"
    assert payload["version"] == "0.2.2"
    assert payload["status"] == "v1 cited planning policy and staff analysis runtime"
    assert "staff-only local policy ingestion" in payload["message"]
    assert "Townlight Zoning and Townlight Meetings context contracts" in payload["message"]
    assert "does not make official planning determinations" in payload["message"]
    assert payload["next_step"].startswith("Configure local plan policies")


def test_health_endpoint_reports_versions() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "civicplan"
    assert payload["version"] == "0.2.2"
    assert payload["civiccore_version"] == "1.1.0"


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
    assert "v0.2.2 corrective demotion state" in script


def test_current_docs_mark_corrective_demotion_without_overclaim() -> None:
    docs = {
        "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
        "README.txt": (ROOT / "README.txt").read_text(encoding="utf-8"),
        "USER-MANUAL.md": (ROOT / "USER-MANUAL.md").read_text(encoding="utf-8"),
        "USER-MANUAL.txt": (ROOT / "USER-MANUAL.txt").read_text(encoding="utf-8"),
        "docs/index.html": (ROOT / "docs" / "index.html").read_text(encoding="utf-8"),
    }

    for path, text in docs.items():
        lowered = text.lower()
        assert "v0.2.2 corrective demotion state" in lowered, path
        assert "previous v1.0.0 release was published in error" in lowered, path
        assert "demoted recovery label" not in lowered, path
        assert "official planning determinations" in lowered, path
