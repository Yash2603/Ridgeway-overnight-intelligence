from backend.app.models import Event, SiteContextResponse, Zone
from shared.seed_data import OVERNIGHT_EVENTS, SHIFT_NOTE, SITE_NAME, SITE_ZONES


def get_site_context() -> SiteContextResponse:
    zones = [Zone(**item) for item in SITE_ZONES]
    events = [Event(**item) for item in OVERNIGHT_EVENTS]
    return SiteContextResponse(site_name=SITE_NAME, shift_note=SHIFT_NOTE, zones=zones, events=events)
