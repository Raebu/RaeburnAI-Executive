from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class Priority(str, Enum):
    urgent = "urgent"
    high = "high"
    medium = "medium"
    low = "low"


class SourceRef(BaseModel):
    provider: str = Field(min_length=1, max_length=80)
    external_id: str | None = Field(default=None, max_length=160)
    title: str = Field(min_length=1, max_length=240)
    url: str | None = Field(default=None, max_length=500)
    collected_at: datetime = Field(default_factory=datetime.utcnow)


class ExecutiveSignal(BaseModel):
    title: str = Field(min_length=1, max_length=240)
    summary: str = Field(min_length=1, max_length=2000)
    priority: Priority
    confidence: float = Field(ge=0, le=1)
    source_refs: list[SourceRef] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class SuggestedAction(BaseModel):
    title: str = Field(min_length=1, max_length=240)
    rationale: str = Field(min_length=1, max_length=2000)
    priority: Priority
    owner: str | None = Field(default=None, max_length=120)
    due_date: datetime | None = None
    estimated_impact: str | None = Field(default=None, max_length=500)
    source_refs: list[SourceRef] = Field(default_factory=list)


class KpiSnapshot(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    value: float
    target: float | None = None
    unit: str = Field(default="", max_length=24)
    trend: str = Field(default="stable")
    status: Priority = Priority.low


class BriefingRequest(BaseModel):
    organisation: str = Field(default="RaeburnAI", min_length=1, max_length=120)
    executive_name: str = Field(default="CEO", min_length=1, max_length=120)
    timezone: str = Field(default="Europe/London", min_length=1, max_length=80)
    competitors: list[str] = Field(default_factory=list, max_length=10)
    focus_areas: list[str] = Field(default_factory=lambda: ["cash", "sales", "delivery", "risk"], max_length=12)

    @field_validator("competitors", "focus_areas")
    @classmethod
    def strip_items(cls, values: list[str]) -> list[str]:
        return [item.strip()[:120] for item in values if item.strip()]


class ExecutiveBriefing(BaseModel):
    briefing_id: str
    generated_at: datetime
    organisation: str
    executive_name: str
    executive_summary: str
    important_emails: list[ExecutiveSignal]
    calendar: list[ExecutiveSignal]
    kpis: list[KpiSnapshot]
    risks: list[ExecutiveSignal]
    sales: list[ExecutiveSignal]
    competitors: list[ExecutiveSignal]
    news: list[ExecutiveSignal]
    suggested_actions: list[SuggestedAction]


class ActionExecutionRequest(BaseModel):
    action_title: str = Field(min_length=1, max_length=240)
    target_system: str = Field(min_length=1, max_length=80)
    dry_run: bool = True


class ActionExecutionResponse(BaseModel):
    status: str
    message: str
    audit_id: str
