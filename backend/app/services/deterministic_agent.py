from datetime import datetime, timezone

from backend.app.data import get_site_context
from backend.app.models import Briefing, Finding, InvestigationResponse, MissionPlan, ToolTrace


def build_deterministic_investigation(operator_note: str = "") -> InvestigationResponse:
    context = get_site_context()
    note = operator_note.strip() or "No additional operator note supplied."

    return InvestigationResponse(
        mode="deterministic_fallback",
        generated_at=datetime.now(timezone.utc).isoformat(),
        site_name=context.site_name,
        agent_summary=(
            "The fallback investigation connected the perimeter disturbance, suspicious vehicle dwell, "
            "camera degradation, and drone recheck into a single operator-ready morning narrative."
        ),
        briefing=Briefing(
            headline="Probable overnight probe around Block C, with no evidence of an active on-site threat at 6:10 AM.",
            summary=(
                "Gate 3 perimeter activity was followed by an unplanned vehicle dwell near Block C and overlapping "
                "camera degradation. A later drone pass found no people on site but did confirm fresh tire tracks."
            ),
            what_happened=[
                "22:41 to 23:19 UTC: Gate 3 fence vibration, suspicious vehicle activity, and camera instability clustered around Block C.",
                "23:04 UTC: An expired contractor badge failed three times at Checkpoint Alpha and never gained access.",
                "00:16 UTC: Drone R-12 rechecked the area and found fresh tracks but no thermal anomaly.",
            ],
            harmless_signals=[
                "The East Yard contractor van matched a valid work order and is treated as baseline activity.",
                "The failed badge attempt appears adjacent to the incident, not a confirmed breach path.",
            ],
            escalation_items=[
                "Escalate the Block C sequence to Nisha and verify inventory integrity before the 8:00 AM review.",
                "Preserve Gate 3 access data and camera health logs in case the incident needs formal investigation.",
            ],
            follow_ups=[
                "Dispatch a daylight patrol over Gate 3, Block C, and East Yard.",
                "Inspect camera cam-n4 and adjacent network equipment for intentional or environmental interference.",
                "Confirm seals, stock counts, and tire marks around Block C.",
            ],
        ),
        findings=[
            Finding(
                id="finding-1",
                title="Likely low-duration reconnaissance around Block C",
                narrative=(
                    "The highest-confidence interpretation is a short reconnaissance or unauthorized inspection attempt. "
                    "The vehicle route, fence anomaly, and camera instability are too tightly clustered to dismiss as unrelated."
                ),
                severity="critical",
                confidence=0.86,
                status="pending",
                supporting_event_ids=["evt-001", "evt-002", "evt-004", "evt-006"],
                recommended_action="Escalate to site leadership and verify Block C inventory immediately.",
            ),
            Finding(
                id="finding-2",
                title="Badge swipe incident is probably adjacent context",
                narrative=(
                    "The denied contractor credential matters because it signals access-control hygiene risk, "
                    "but it did not result in entry and is not the strongest explanation for the main incident."
                ),
                severity="medium",
                confidence=0.74,
                status="needs-follow-up",
                supporting_event_ids=["evt-003"],
                recommended_action="Interview the contractor supervisor and clean up expired credentials.",
            ),
            Finding(
                id="finding-3",
                title="Drone patrol reduced uncertainty without fully closing the case",
                narrative=(
                    "The later drone pass lowered the chance of an active threat but supported the earlier vehicle route with fresh tire-track evidence."
                ),
                severity="high",
                confidence=0.82,
                status="pending",
                supporting_event_ids=["evt-005"],
                recommended_action="Run a daylight sweep to validate traces, seals, and blind spots.",
            ),
        ],
        mission=MissionPlan(
            title="Block C daylight verification sweep",
            objective="Reconfirm that no unauthorized assets or personnel remain near Block C before leadership arrives.",
            rationale="The earlier signal cluster centered on Block C and the likely ingress/egress route through Gate 3.",
            eta_minutes=14,
            route_zone_ids=["drone-bay", "gate-3", "block-c", "yard-east", "drone-bay"],
        ),
        uncertainties=[
            "There is no direct visual evidence proving what the pickup intended to do at Block C.",
            "The badge swipe timing is suspicious, but the available evidence does not prove coordination.",
            "Camera degradation may have been environmental or deliberate; the current data cannot distinguish that confidently.",
            f"Operator note included in review: {note}",
        ],
        tool_trace=[
            ToolTrace(
                tool="fallback_storyline_builder",
                source="system",
                reason="Provide a deterministic report when OpenAI or MCP infrastructure is not configured.",
                input_summary="Seeded overnight events and operator note",
                output_summary="Generated structured morning briefing draft",
            )
        ],
        raw_output_text="",
    )
