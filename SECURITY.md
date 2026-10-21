# Security

Townlight Planning Current version: 0.2.2. This is a narrow truth-repair release with no functional upgrade. The previous v1.0.0 release was published in error and does not prove public-use readiness. Deploy it only for local scaffold evaluation behind the city's trusted access layer, configure local adopted plan-policy records, and keep official planning determinations with municipal staff and elected bodies.

When `CIVICPLAN_POLICY_DB_URL` is configured, persisted staff-analysis create/read routes require `CIVICPLAN_STAFF_API_KEY`, `X-CivicPlan-Role: staff`, and a matching `X-CivicPlan-Staff-Key` from a trusted staff workflow. Townlight Planning uses Townlight Core `staff_key_gate` for timing-safe key comparison. This header gate is a local release safeguard, not a replacement for production identity, tenant scoping, and audit logging.

Report suspected vulnerabilities privately to the project maintainer. Do not open public issues containing exploit details, secrets, or sensitive municipal data.
