"""Local, staff-verified import contract; no network retrieval or file execution."""

import base64
import binascii
from datetime import date
import hashlib
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

PlanType = Literal["comprehensive", "small-area", "transportation", "parks", "sustainability"]


class BundleModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class SourceDocument(BundleModel):
    document_id: str = Field(min_length=1, max_length=160, pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
    filename: str = Field(min_length=1, max_length=255)
    media_type: Literal[
        "text/plain", "text/markdown", "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    content_base64: str = Field(min_length=1, max_length=14_000_000)

    def original_bytes(self) -> bytes:
        try:
            data = base64.b64decode(self.content_base64, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError("Source content must be valid base64.") from exc
        if not data or len(data) > 10_000_000:
            raise ValueError("Each source must contain 1 to 10000000 bytes.")
        if hashlib.sha256(data).hexdigest() != self.sha256:
            raise ValueError("Source SHA256 does not match the original bytes.")
        return data

    @model_validator(mode="after")
    def validate_source(self):
        if any(c in self.filename for c in ("/", "\\", ":")) or self.filename in {".", ".."}:
            raise ValueError("Use a local filename, not a path or URL.")
        suffixes = {
            "text/plain": ".txt", "text/markdown": ".md", "application/pdf": ".pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
        }
        if not self.filename.lower().endswith(suffixes[self.media_type]):
            raise ValueError("Source filename extension must match its media type.")
        data = self.original_bytes()
        if self.media_type.startswith("text/"):
            try:
                data.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ValueError("Text sources must be UTF-8.") from exc
        elif self.media_type == "application/pdf" and not data.startswith(b"%PDF-"):
            raise ValueError("PDF source header is invalid.")
        elif self.media_type.endswith("document") and not data.startswith(b"PK"):
            raise ValueError("DOCX source header is invalid.")
        return self


class SourcePolicy(BundleModel):
    policy_id: str = Field(min_length=1, max_length=160)
    document_id: str = Field(min_length=1, max_length=160)
    goal: str = Field(min_length=1, max_length=500)
    objective: str = Field(min_length=1, max_length=500)
    topic_key: str = Field(min_length=1, max_length=160)
    title: str = Field(min_length=1, max_length=500)
    citation: str = Field(min_length=1, max_length=500)
    anchor: str = Field(min_length=1, max_length=500)
    excerpt: str = Field(min_length=1, max_length=20000)
    relevance: str = Field(min_length=1, max_length=2000)
    staff_verified: Literal[True]


class AdoptionEvidence(BundleModel):
    kind: Literal["manual-record", "meeting-reference", "source-document"]
    reference: str = Field(min_length=1, max_length=1000)
    document_id: str | None = Field(default=None, min_length=1, max_length=160)
    note: str = Field(min_length=1, max_length=4000)


class PlanBundle(BundleModel):
    schema_version: Literal[1] = 1
    plan_id: str = Field(min_length=1, max_length=160, pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
    title: str = Field(min_length=1, max_length=500)
    jurisdiction: str = Field(min_length=1, max_length=255)
    plan_type: PlanType
    status: Literal["pending", "adopted", "superseded"]
    visibility: Literal["staff", "public"] = "staff"
    dataset_kind: Literal["municipal", "demo"] = "municipal"
    source_date: date
    adopted_on: date | None = None
    effective_on: date | None = None
    change_note: str = Field(min_length=1, max_length=4000)
    reviewer_label: str = Field(min_length=1, max_length=255)
    documents: list[SourceDocument] = Field(min_length=1, max_length=20)
    policies: list[SourcePolicy] = Field(min_length=1, max_length=1000)
    adoption_evidence: list[AdoptionEvidence] = Field(default_factory=list, max_length=100)

    @model_validator(mode="after")
    def validate_bundle(self):
        docs = {doc.document_id: doc for doc in self.documents}
        if len(docs) != len(self.documents):
            raise ValueError("Document IDs must be unique within a revision.")
        if len({p.policy_id for p in self.policies}) != len(self.policies):
            raise ValueError("Policy IDs must be unique within a revision.")
        if sum(len(doc.original_bytes()) for doc in self.documents) > 25_000_000:
            raise ValueError("Total source bytes exceed the 25000000-byte bundle limit.")
        if self.status == "adopted" and not (
            self.adopted_on and self.effective_on and self.adoption_evidence
        ):
            raise ValueError("Adopted plans require adoption/effective dates and recorded evidence.")
        if self.status == "superseded" and not self.adoption_evidence:
            raise ValueError("Supersession requires recorded evidence.")
        for item in [*self.policies, *self.adoption_evidence]:
            if item.document_id is not None and item.document_id not in docs:
                raise ValueError("Every document reference must resolve within the bundle.")
        for policy in self.policies:
            doc = docs[policy.document_id]
            if doc.media_type.startswith("text/") and policy.excerpt not in doc.original_bytes().decode("utf-8"):
                raise ValueError("Policy excerpt must occur in its referenced UTF-8 source.")
        return self
