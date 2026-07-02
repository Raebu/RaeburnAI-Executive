from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field

class Priority(str, Enum):
    urgent = "urgent"
    high = "high"
    medium = "medium"
    low = "low"

class SourceRef(BaseModel):
    provider: str
    external_id: str | None = None
    title: str
    url: str | None = None
    collected_at: datetime = Field(default_factory=datetime.utcnow)

class ExecutiveSignal(BaseModel):
    title: str
    summary: str
    priority: Priority
    confidence: float = Field(ge=0, le=1)
    source_refs: list[SourceRef] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

class SuggestedAction(BaseModel):
    title: str
    rationale: str
    priority: Priority
    owner: str | None = None
    due_date: datetime | None = None
    estimated_impact: str | None = None
    source_refs: list[SourceRef] = Field(default_factory=list)

class KpiSnapshot(BaseModel):
    name: str
    value: float
    target: float | None = None
    unit: str = ""
    trend: str = "stable"
    status: Priority = Priority.low

class BriefingRequest(BaseModel):
    organisation: str = "RaeburnAI"
    executive_name: str = "CEO"
    timezone: str = "Europe/London"
    competitors: list[str] = Field(default_factory=list)
    focus_areas: list[str] = Field(default_factory=lambda: ["cash", "sales", "delivery", "risk"])

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
