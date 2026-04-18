import json
from datetime import datetime, timezone
from typing import Any, Dict, List

from openai import OpenAI

from backend.app.config import Settings
from backend.app.data import get_site_context
from backend.app.models import InvestigationResponse, ToolTrace
from backend.app.services.deterministic_agent import build_deterministic_investigation


REPORT_SCHEMA: Dict[str, Any] = {
    "type": "json_schema",
    "name": "ridgeway_investigation_report",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "agent_summary": {"type": "string"},
            "briefing": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "headline": {"type": "string"},
                    "summary": {"type": "string"},
                    "what_happened": {"type": "array", "items": {"type": "string"}},
                    "harmless_signals": {"type": "array", "items": {"type": "string"}},
                    "escalation_items": {"type": "array", "items": {"type": "string"}},
                    "follow_ups": {"type": "array", "items": {"type": "string"}},
                },
                "required": [
                    "headline",
                    "summary",
                    "what_happened",
                    "harmless_signals",
                    "escalation_items",
                    "follow_ups",
                ],
            },
            "findings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "id": {"type": "string"},
                        "title": {"type": "string"},
                        "narrative": {"type": "string"},
                        "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                        "confidence": {"type": "number"},
                        "status": {"type": "string", "enum": ["pending", "approved", "needs-follow-up"]},
                        "supporting_event_ids": {"type": "array", "items": {"type": "string"}},
                        "recommended_action": {"type": "string"},
                    },
                    "required": [
                        "id",
                        "title",
                        "narrative",
                        "severity",
                        "confidence",
                        "status",
                        "supporting_event_ids",
                        "recommended_action",
                    ],
                },
            },
            "mission": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "title": {"type": "string"},
                    "objective": {"type": "string"},
                    "rationale": {"type": "string"},
                    "eta_minutes": {"type": "integer"},
                    "route_zone_ids": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["title", "objective", "rationale", "eta_minutes", "route_zone_ids"],
            },
            "uncertainties": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["agent_summary", "briefing", "findings", "mission", "uncertainties"],
    },
}


FUNCTION_TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "name": "fetch_incident_log",
        "description": "Return overnight site events, optionally filtered by zone, event type, or severity.",
        "strict": True,
        "parameters": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "zone_id": {"type": "string"},
                "event_type": {"type": "string"},
                "severity": {"type": "string"},
            },
            "required": [],
        },
    },
    {
        "type": "function",
        "name": "query_badge_system",
        "description": "Look up badge access anomalies and contractor credential context for a specific zone or person.",
        "strict": True,
        "parameters": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "zone_id": {"type": "string"},
                "person_name": {"type": "string"},
            },
            "required": [],
        },
    },
    {
        "type": "function",
        "name": "get_zone_context",
        "description": "Return business context, risk score, and description for a site zone.",
        "strict": True,
        "parameters": {
            "type": "object",
            "additionalProperties": False,
            "properties": {"zone_id": {"type": "string"}},
            "required": ["zone_id"],
        },
    },
    {
        "type": "function",
        "name": "simulate_drone_followup",
        "description": "Create a lightweight follow-up patrol route for a suspicious hotspot zone.",
        "strict": True,
        "parameters": {
            "type": "object",
            "additionalProperties": False,
            "properties": {"hotspot_zone_id": {"type": "string"}},
            "required": ["hotspot_zone_id"],
        },
    },
]


def _investigation_prompt(operator_note: str) -> List[Dict[str, Any]]:
    context = get_site_context()
    return [
        {
            "role": "system",
            "content": (
                "You are Maya's overnight investigation copilot for Ridgeway Site. "
                "Investigate first, use tools instead of guessing, be explicit about uncertainty, "
                "and produce a concise morning-briefing JSON report. Do not invent facts beyond tool outputs."
            ),
        },
        {
            "role": "user",
            "content": (
                f"It is 6:10 AM at {context.site_name}. Maya needs to know what happened, what matters, "
                "what was harmless, what deserves escalation, what the drone checked, and what still needs follow-up "
                f"before the 8:00 AM leadership review. Night supervisor note: {context.shift_note}. "
                f"Operator note: {operator_note or 'No extra operator note provided.'}"
            ),
        },
    ]


def _dispatch_function(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    context = get_site_context()
    events = [event.model_dump() for event in context.events]
    zones = [zone.model_dump() for zone in context.zones]

    if name == "fetch_incident_log":
        zone_id = arguments.get("zone_id")
        event_type = arguments.get("event_type")
        severity = arguments.get("severity")
        return {
            "events": [
                event
                for event in events
                if (not zone_id or event["zone_id"] == zone_id)
                and (not event_type or event["type"] == event_type)
                and (not severity or event["severity"] == severity)
            ]
        }

    if name == "query_badge_system":
        person_name = arguments.get("person_name")
        zone_id = arguments.get("zone_id")
        return {
            "badge_events": [
                event
                for event in events
                if event["type"] == "badge-swipe"
                and (not person_name or event.get("actor") == person_name)
                and (not zone_id or event["zone_id"] == zone_id)
            ]
        }

    if name == "get_zone_context":
        zone = next((zone for zone in zones if zone["id"] == arguments["zone_id"]), None)
        return {"zone": zone}

    if name == "simulate_drone_followup":
        hotspot_zone_id = arguments["hotspot_zone_id"]
        return {
            "mission": {
                "title": "Block C daylight verification sweep",
                "objective": "Reconfirm no unauthorized personnel or staged assets remain near the overnight hotspot.",
                "rationale": "The overnight signal cluster centered on Block C and likely ingress through Gate 3.",
                "eta_minutes": 14,
                "route_zone_ids": ["drone-bay", "gate-3", hotspot_zone_id, "yard-east", "drone-bay"],
            }
        }

    raise ValueError(f"Unknown tool: {name}")


def _build_remote_mcp_tool(settings: Settings) -> List[Dict[str, Any]]:
    return [
        {
            "type": "mcp",
            "server_label": "ridgeway_mcp",
            "server_description": "Ridgeway overnight incident tools for logs, badge access, zone context, and drone missions.",
            "server_url": settings.openai_mcp_server_url,
            "require_approval": "never",
            "allowed_tools": [
                "fetch_incident_log",
                "query_badge_system",
                "get_zone_context",
                "simulate_drone_followup",
            ],
        }
    ]


def _trace_from_output_items(items: List[Any], default_source: str) -> List[ToolTrace]:
    traces: List[ToolTrace] = []
    for item in items:
        item_type = getattr(item, "type", None)
        if item_type == "function_call":
            traces.append(
                ToolTrace(
                    tool=item.name,
                    source="function",
                    reason="Model requested application-side data access.",
                    input_summary=getattr(item, "arguments", "{}"),
                    output_summary="Function call executed",
                )
            )
        elif item_type == "mcp_call":
            traces.append(
                ToolTrace(
                    tool=item.name,
                    source="mcp",
                    reason="Model requested MCP-hosted operational context.",
                    input_summary=getattr(item, "arguments", "{}"),
                    output_summary=getattr(item, "output", "") or "MCP tool executed",
                )
            )
        elif item_type == "mcp_list_tools":
            traces.append(
                ToolTrace(
                    tool="mcp_list_tools",
                    source="mcp",
                    reason="Responses API imported tools from the remote MCP server.",
                    input_summary="server tool discovery",
                    output_summary="Available tools listed for model",
                )
            )
        elif item_type == "reasoning":
            traces.append(
                ToolTrace(
                    tool="reasoning",
                    source=default_source,
                    reason="Model reasoning step captured for transparency.",
                    input_summary="internal reasoning",
                    output_summary="Reasoning summary available in response output",
                )
            )
    return traces


def run_openai_investigation(operator_note: str, settings: Settings) -> InvestigationResponse:
    if not settings.openai_api_key:
        return build_deterministic_investigation(operator_note)

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = _investigation_prompt(operator_note)

    if settings.openai_tool_mode == "remote_mcp" and settings.openai_mcp_server_url:
        response = client.responses.create(
            model=settings.openai_model,
            input=prompt,
            tools=_build_remote_mcp_tool(settings),
            text={"format": REPORT_SCHEMA},
            max_output_tokens=2200,
        )
        parsed = json.loads(response.output_text)
        traces = _trace_from_output_items(response.output, "mcp")
        return InvestigationResponse(
            mode="openai_remote_mcp",
            generated_at=datetime.now(timezone.utc).isoformat(),
            site_name=get_site_context().site_name,
            tool_trace=traces,
            raw_output_text=response.output_text,
            **parsed,
        )

    response = client.responses.create(
        model=settings.openai_model,
        input=prompt,
        tools=FUNCTION_TOOLS,
        text={"format": REPORT_SCHEMA},
        max_output_tokens=2200,
    )
    traces = _trace_from_output_items(response.output, "function")

    while True:
        function_calls = [item for item in response.output if getattr(item, "type", None) == "function_call"]
        if not function_calls:
            break

        follow_up_input: List[Dict[str, Any]] = []
        for tool_call in function_calls:
            args = json.loads(tool_call.arguments)
            result = _dispatch_function(tool_call.name, args)
            follow_up_input.append(
                {
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": json.dumps(result),
                }
            )

        response = client.responses.create(
            model=settings.openai_model,
            previous_response_id=response.id,
            input=follow_up_input,
            tools=FUNCTION_TOOLS,
            text={"format": REPORT_SCHEMA},
            max_output_tokens=2200,
        )
        traces.extend(_trace_from_output_items(response.output, "function"))

    parsed = json.loads(response.output_text)
    return InvestigationResponse(
        mode="openai_function_fallback",
        generated_at=datetime.now(timezone.utc).isoformat(),
        site_name=get_site_context().site_name,
        tool_trace=traces,
        raw_output_text=response.output_text,
        **parsed,
    )
