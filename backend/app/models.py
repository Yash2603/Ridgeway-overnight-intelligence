from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


Severity = Literal["low", "medium", "high", "critical"]
InvestigationStatus = Literal["pending", "approved", "needs-follow-up"]


class Zone(BaseModel):
    id: str
    label: str
    kind: str
    x: int
    y: int
    width: int
    height: int
    risk_weight: int
    description: str


class Event(BaseModel):
    id: str
    type: str
    zone_id: str
    started_at: str
    ended_at: Optional[str] = None
    title: str
    detail: str
    severity: Severity
    confidence: float
    actor: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SiteContextResponse(BaseModel):
    site_name: str
    shift_note: str
    zones: List[Zone]
    events: List[Event]


class InvestigationRequest(BaseModel):
    operator_note: str = ""


class ToolTrace(BaseModel):
    tool: str
    source: Literal["mcp", "function", "system"]
    reason: str
    input_summary: str
    output_summary: str


class Finding(BaseModel):
    id: str
    title: str
    narrative: str
    severity: Severity
    confidence: float
    status: InvestigationStatus
    supporting_event_ids: List[str]
    recommended_action: str


class MissionPlan(BaseModel):
    title: str
    objective: str
    rationale: str
    eta_minutes: int
    route_zone_ids: List[str]


class Briefing(BaseModel):
    headline: str
    summary: str
    what_happened: List[str]
    harmless_signals: List[str]
    escalation_items: List[str]
    follow_ups: List[str]


class InvestigationResponse(BaseModel):
    mode: Literal["openai_remote_mcp", "openai_function_fallback", "deterministic_fallback"]
    generated_at: str
    site_name: str
    agent_summary: str
    briefing: Briefing
    findings: List[Finding]
    mission: MissionPlan
    uncertainties: List[str]
    tool_trace: List[ToolTrace]
    raw_output_text: str = ""
