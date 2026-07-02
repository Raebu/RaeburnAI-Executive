from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .briefing import BriefingEngine
from .config import get_settings
from .models import BriefingRequest, ExecutiveBriefing

settings = get_settings()
app = FastAPI(
    title="RaeburnAI Executive API",
    description="CEO second brain for daily briefings, KPI monitoring and decision support.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.web_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
engine = BriefingEngine()

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "raeburnai-executive-api"}

@app.post("/v1/briefings/daily", response_model=ExecutiveBriefing)
async def generate_daily_briefing(request: BriefingRequest) -> ExecutiveBriefing:
    return await engine.generate(request)
