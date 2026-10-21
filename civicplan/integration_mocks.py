from __future__ import annotations

from dataclasses import dataclass
from typing import Any


SUPPORTED_PROVIDERS = frozenset(
    {
        "civiczone_policy_context",
        "civicclerk_staff_report_context",
        "geojson_area_boundary",
        "local_plan_document_import",
    }
)


@dataclass(frozen=True)
class IntegrationError:
    provider: str
    message: str
    fix: str
    code: str


@dataclass(frozen=True)
class IntegrationResult:
    provider: str
    records: tuple[dict[str, Any], ...]
    source: str
    warnings: tuple[str, ...] = ()


class CivicPlanIntegrationMockLayer:
    """Local-only integration boundary checks for Townlight Planning v1."""

    def run(self, provider: str, payload: dict[str, Any]) -> IntegrationResult | IntegrationError:
        if provider not in SUPPORTED_PROVIDERS:
            return IntegrationError(
                provider=provider,
                message="Unsupported Townlight Planning mock integration provider.",
                fix="Use a supported local mock provider for Townlight Planning v1 validation.",
                code="unsupported_provider",
            )
        for key in ("url", "endpoint", "service_url"):
            value = payload.get(key)
            if isinstance(value, str) and value.startswith(("http://", "https://")):
                return IntegrationError(
                    provider=provider,
                    message="Live external calls are disabled for Townlight Planning v1 integration mocks.",
                    fix="Use local fixture payloads; do not provide http/https endpoints.",
                    code="air_gap_violation",
                )
        if payload.get("provider") not in (None, provider):
            return IntegrationError(
                provider=provider,
                message="Payload provider does not match the requested provider.",
                fix="Set payload.provider to the same provider used in the mock call.",
                code="spoofed_provider",
            )
        if provider == "local_plan_document_import":
            return _plan_document_import(provider, payload)
        if provider == "civiczone_policy_context":
            return _civiczone_context(provider, payload)
        if provider == "civicclerk_staff_report_context":
            return _civicclerk_context(provider, payload)
        return _geojson_boundary(provider, payload)


def _plan_document_import(provider: str, payload: dict[str, Any]) -> IntegrationResult | IntegrationError:
    policies = payload.get("policies")
    if not isinstance(policies, list) or not policies:
        return _malformed(provider, "policies must be a non-empty local list.")
    records = []
    for policy in policies:
        if not isinstance(policy, dict) or not policy.get("policy_id") or not policy.get("citation"):
            return _malformed(provider, "each policy needs policy_id and citation.")
        records.append({"policy_id": policy["policy_id"], "citation": policy["citation"]})
    return IntegrationResult(provider=provider, records=tuple(records), source="local plan document fixture")


def _civiczone_context(provider: str, payload: dict[str, Any]) -> IntegrationResult | IntegrationError:
    if not payload.get("zone_code") and not payload.get("parcel_number"):
        return _malformed(provider, "provide zone_code or parcel_number for zoning policy context.")
    return IntegrationResult(
        provider=provider,
        records=(
            {
                "zone_code": payload.get("zone_code"),
                "parcel_number": payload.get("parcel_number"),
                "review_required": True,
            },
        ),
        source="local CivicZone context fixture",
    )


def _civicclerk_context(provider: str, payload: dict[str, Any]) -> IntegrationResult | IntegrationError:
    if not payload.get("agenda_item") or not payload.get("staff_report_id"):
        return _malformed(provider, "provide agenda_item and staff_report_id.")
    return IntegrationResult(
        provider=provider,
        records=(
            {
                "agenda_item": payload["agenda_item"],
                "staff_report_id": payload["staff_report_id"],
                "visibility": "staff_only",
            },
        ),
        source="local CivicClerk staff report fixture",
    )


def _geojson_boundary(provider: str, payload: dict[str, Any]) -> IntegrationResult | IntegrationError:
    if payload.get("type") != "FeatureCollection" or not isinstance(payload.get("features"), list):
        return _malformed(provider, "GeoJSON boundary payload must be a FeatureCollection.")
    return IntegrationResult(
        provider=provider,
        records=tuple({"feature_count": len(payload["features"])},),
        source="local GeoJSON boundary fixture",
    )


def _malformed(provider: str, detail: str) -> IntegrationError:
    return IntegrationError(
        provider=provider,
        message=f"Malformed local fixture payload: {detail}",
        fix="Repair the local mock fixture before retrying; no live fallback will be attempted.",
        code="malformed_payload",
    )
