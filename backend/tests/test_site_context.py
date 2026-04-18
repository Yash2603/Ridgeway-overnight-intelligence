from backend.app.data import get_site_context
from backend.app.services.deterministic_agent import build_deterministic_investigation


def test_site_context_has_seeded_events() -> None:
    context = get_site_context()
    assert context.site_name == "Ridgeway Site"
    assert len(context.events) >= 6
    assert any(event.zone_id == "block-c" for event in context.events)


def test_deterministic_fallback_returns_structured_response() -> None:
    response = build_deterministic_investigation("Focus on Block C.")
    assert response.mode == "deterministic_fallback"
    assert response.findings
    assert response.mission.route_zone_ids[2] == "block-c"
