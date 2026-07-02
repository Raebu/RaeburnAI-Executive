import logging
from uuid import uuid4

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .briefing import BriefingEngine
from .config import get_settings
from .logging_config import configure_logging
from .models import ActionExecutionRequest, ActionExecutionResponse, BriefingRequest, ExecutiveBriefing
from .security import enforce_rate_limit, require_api_key, require_human_approval

configure_logging()
logger = logging.getLogger(__name__)
settings = get_settings()
app = FastAPI(
    title="RaeburnAI Executive API",
    description="CEO second brain for daily briefings, KPI monitoring and decision support.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.web_url],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type", "X-API-Key", "X-Human-Approval"],
)
engine = BriefingEngine()


@app.middleware("http")
async def request_logging(request: Request, call_next):
    response = await call_next(request)
    logger.info("request path=%s status=%s", request.url.path, response.status_code)
    return response


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "raeburnai-executive-api"}


@app.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready", "environment": settings.env}


@app.post("/v1/briefings/daily", response_model=ExecutiveBriefing, dependencies=[Depends(enforce_rate_limit)])
async def generate_daily_briefing(
    request: BriefingRequest,
    actor: str = Depends(require_api_key),
) -> ExecutiveBriefing:
    logger.info("briefing_generated actor=%s organisation=%s", actor, request.organisation)
    return await engine.generate(request)


@app.post(
    "/v1/actions/execute",
    response_model=ActionExecutionResponse,
    dependencies=[Depends(enforce_rate_limit), Depends(require_human_approval)],
)
async def execute_action(
    request: ActionExecutionRequest,
    actor: str = Depends(require_api_key),
) -> ActionExecutionResponse:
    audit_id = str(uuid4())
    logger.info("action_execution_requested actor=%s audit_id=%s target=%s", actor, audit_id, request.target_system)
    return ActionExecutionResponse(
        status="accepted" if request.dry_run else "queued",
        message="Action recorded with human approval. Production connectors should execute this asynchronously.",
        audit_id=audit_id,
    )
