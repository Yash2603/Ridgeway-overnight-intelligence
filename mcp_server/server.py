import os

import uvicorn
from fastapi import FastAPI

from shared.seed_data import OVERNIGHT_EVENTS, SITE_ZONES

try:
    from fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("fastmcp must be installed to run the MCP server.") from exc


mcp = FastMCP("ridgeway-mcp")


@mcp.tool
def fetch_incident_log(zone_id: str | None = None, event_type: str | None = None, severity: str | None = None) -> dict:
    events = [
        event
        for event in OVERNIGHT_EVENTS
        if (zone_id is None or event["zone_id"] == zone_id)
        and (event_type is None or event["type"] == event_type)
        and (severity is None or event["severity"] == severity)
    ]
    return {"events": events}


@mcp.tool
def query_badge_system(zone_id: str | None = None, person_name: str | None = None) -> dict:
    badge_events = [
        event
        for event in OVERNIGHT_EVENTS
        if event["type"] == "badge-swipe"
        and (zone_id is None or event["zone_id"] == zone_id)
        and (person_name is None or event.get("actor") == person_name)
    ]
    return {"badge_events": badge_events}


@mcp.tool
def get_zone_context(zone_id: str) -> dict:
    zone = next((zone for zone in SITE_ZONES if zone["id"] == zone_id), None)
    return {"zone": zone}


@mcp.tool
def simulate_drone_followup(hotspot_zone_id: str) -> dict:
    return {
        "mission": {
            "title": "Block C daylight verification sweep",
            "objective": "Reconfirm no unauthorized personnel or staged assets remain near the overnight hotspot.",
            "rationale": "The overnight signal cluster centered on Block C and likely ingress through Gate 3.",
            "eta_minutes": 14,
            "route_zone_ids": ["drone-bay", "gate-3", hotspot_zone_id, "yard-east", "drone-bay"],
        }
    }

transport_path = os.getenv("MCP_PATH", "/mcp")
mcp_app = mcp.http_app(path=transport_path)
app = FastAPI()

@app.get("/tools")
def get_tools():
    return {
        "tools": [
            {
                "name": "fetch_incident_log",
                "description": "Return overnight site events",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "zone_id": {"type": "string"},
                        "event_type": {"type": "string"},
                        "severity": {"type": "string"}
                    },
                    "required": []
                }
            },
            {
                "name": "query_badge_system",
                "description": "Check badge anomalies",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "zone_id": {"type": "string"},
                        "person_name": {"type": "string"}
                    },
                    "required": []
                }
            }
        ]
    }

@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "ok", "service": "ridgeway-mcp"}


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


mcp_app = mcp.http_app(path="/")
app.mount("/mcp", mcp_app)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.getenv("MCP_HOST", "0.0.0.0"),
        port=int(os.getenv("MCP_PORT", "9000")),
    )
