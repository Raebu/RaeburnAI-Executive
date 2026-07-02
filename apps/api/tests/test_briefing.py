import pytest
from raeburnai_executive.briefing import BriefingEngine
from raeburnai_executive.models import BriefingRequest

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
