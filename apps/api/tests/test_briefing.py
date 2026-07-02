import pytest
from pydantic import ValidationError

from raeburnai_executive.briefing import BriefingEngine
from raeburnai_executive.models import BriefingRequest, ExecutiveSignal, Priority
from raeburnai_executive.security import InMemoryRateLimiter


@pytest.mark.asyncio
async def test_generate_daily_briefing_contains_required_sections():
    briefing = await BriefingEngine().generate(BriefingRequest(organisation="TestCo", competitors=["Acme AI"]))
    assert briefing.organisation == "TestCo"
    assert briefing.executive_summary
    assert briefing.important_emails
    assert briefing.calendar
    assert briefing.kpis
    assert briefing.risks
    assert briefing.sales
    assert briefing.competitors
    assert briefing.news
    assert briefing.suggested_actions


def test_signal_confidence_validation():
    with pytest.raises(ValidationError):
        ExecutiveSignal(title="Bad", summary="Invalid", priority=Priority.low, confidence=1.5)


def test_rate_limiter_blocks_after_limit():
    limiter = InMemoryRateLimiter(limit=2, window_seconds=60)
    assert limiter.check("client") is True
    assert limiter.check("client") is True
    assert limiter.check("client") is False
