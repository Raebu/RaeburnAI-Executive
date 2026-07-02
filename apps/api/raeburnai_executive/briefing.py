from datetime import datetime, timedelta
from uuid import uuid4

from .connectors import CalendarConnector, EmailConnector, IntelligenceConnector, KpiConnector, RiskConnector, SalesConnector
from .models import BriefingRequest, ExecutiveBriefing, Priority, SuggestedAction

class BriefingEngine:
    def __init__(self) -> None:
        self.email = EmailConnector()
        self.calendar = CalendarConnector()
        self.kpi = KpiConnector()
        self.sales = SalesConnector()
        self.intel = IntelligenceConnector()
        self.risk = RiskConnector()

    async def generate(self, request: BriefingRequest) -> ExecutiveBriefing:
        important_emails = await self.email.important_emails()
        calendar = await self.calendar.calendar_signals()
        kpis = await self.kpi.kpis()
        risks = await self.risk.risk_signals()
        sales = await self.sales.sales_signals()
        competitors = await self.intel.competitor_signals(request.competitors)
        news = await self.intel.news_signals()
        actions = self._actions(risks, sales, calendar)
        return ExecutiveBriefing(
            briefing_id=str(uuid4()),
            generated_at=datetime.utcnow(),
            organisation=request.organisation,
            executive_name=request.executive_name,
            executive_summary=self._summary(kpis, risks, sales, important_emails),
            important_emails=important_emails,
            calendar=calendar,
            kpis=kpis,
            risks=risks,
            sales=sales,
            competitors=competitors,
            news=news,
            suggested_actions=actions,
        )

    def _summary(self, kpis, risks, sales, emails) -> str:
        high_count = len([item for item in [*risks, *sales, *emails] if item.priority in {Priority.high, Priority.urgent}])
        attention_kpis = [k.name for k in kpis if k.status in {Priority.high, Priority.urgent}]
        kpi_text = ", ".join(attention_kpis) if attention_kpis else "no major KPI exceptions"
        return f"Today's briefing highlights {high_count} high-priority signals. Watch {kpi_text}. Focus on retention, board readiness and late-stage sales execution."

    def _actions(self, risks, sales, calendar) -> list[SuggestedAction]:
        due = datetime.utcnow() + timedelta(days=1)
        return [
            SuggestedAction(
                title="Assign owner for retention review",
                rationale="Retention is outside target and needs a named owner with a clear recovery plan.",
                priority=Priority.high,
                owner="Chief Customer Officer",
                due_date=due,
                estimated_impact="Protect recurring revenue",
                source_refs=risks[0].source_refs if risks else [],
            ),
            SuggestedAction(
                title="Create board KPI and risk pack",
                rationale="The board meeting needs current KPIs, decision points and mitigations attached in advance.",
                priority=Priority.high,
                owner="CEO Office",
                due_date=due,
                estimated_impact="Improve board decision quality",
                source_refs=calendar[0].source_refs if calendar else [],
            ),
            SuggestedAction(
                title="Map executive sponsors to late-stage deals",
                rationale="Late-stage opportunities need executive sponsorship to increase close probability.",
                priority=Priority.medium,
                owner="Sales Director",
                due_date=due,
                estimated_impact="Improve sales conversion",
                source_refs=sales[0].source_refs if sales else [],
            ),
        ]
