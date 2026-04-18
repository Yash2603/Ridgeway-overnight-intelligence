from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

from backend.app.config import get_settings
from backend.app.data import get_site_context
from backend.app.models import InvestigationRequest, InvestigationResponse, SiteContextResponse
from backend.app.services.openai_agent import run_openai_investigation

settings = get_settings()

origins = [
    "https://ridgeway-overnight-intelligence.vercel.app",
]


app = FastAPI(
    title="Ridgeway Overnight Intelligence",
    version="1.0.0",
    description="Python backend for the Ridgeway overnight intelligence workflow.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    #allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "ok", "service": "ridgeway-api"}

@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/site-context", response_model=SiteContextResponse)
def site_context() -> SiteContextResponse:
    return get_site_context()


@app.post("/api/investigate", response_model=InvestigationResponse)
def investigate(payload: InvestigationRequest) -> InvestigationResponse:
    try:
        return run_openai_investigation(payload.operator_note, settings)
    except Exception as e:
        print("ERROR:", str(e))  # shows in Render logs
        raise HTTPException(status_code=500, detail=str(e))
