from datetime import datetime, timedelta
from .models import ExecutiveSignal, KpiSnapshot, Priority, SourceRef

class EmailConnector:
    async def important_emails(self) -> list[ExecutiveSignal]:
        return [
            ExecutiveSignal(
                title="Enterprise prospect requested implementation plan",
                summary="A high-value prospect asked for pricing, timeline and security evidence before Friday.",
                priority=Priority.high,
                confidence=0.92,
                source_refs=[SourceRef(provider="mock-gmail", title="Implementation plan request")],
            ),
            ExecutiveSignal(
                title="Supplier contract renewal needs review",
                summary="Renewal terms include a 14% uplift and a 7-day response window.",
                priority=Priority.medium,
                confidence=0.84,
                source_refs=[SourceRef(provider="mock-gmail", title="Contract renewal")],
            ),
        ]

class CalendarConnector:
    async def calendar_signals(self) -> list[ExecutiveSignal]:
        return [
            ExecutiveSignal(
                title="Board prep gap",
                summary="Tomorrow's board meeting has no linked KPI pack or risk appendix attached.",
                priority=Priority.high,
                confidence=0.88,
                source_refs=[SourceRef(provider="mock-calendar", title="Board meeting")],
            )
        ]

class KpiConnector:
    async def kpis(self) -> list[KpiSnapshot]:
        return [
            KpiSnapshot(name="Monthly recurring revenue", value=128000, target=140000, unit="GBP", trend="up", status=Priority.medium),
            KpiSnapshot(name="Sales qualified pipeline", value=820000, target=750000, unit="GBP", trend="up", status=Priority.low),
            KpiSnapshot(name="Customer churn", value=3.8, target=2.5, unit="%", trend="up", status=Priority.high),
            KpiSnapshot(name="Runway", value=9.5, target=12, unit="months", trend="down", status=Priority.medium),
        ]

class SalesConnector:
    async def sales_signals(self) -> list[ExecutiveSignal]:
        return [
            ExecutiveSignal(
                title="Pipeline above target but close risk is rising",
                summary="Top-line pipeline is strong, but two late-stage deals have no executive sponsor mapped.",
                priority=Priority.high,
                confidence=0.86,
                source_refs=[SourceRef(provider="mock-crm", title="Sales pipeline")],
            )
        ]

class IntelligenceConnector:
    async def competitor_signals(self, competitors: list[str]) -> list[ExecutiveSignal]:
        names = competitors or ["Competitor A", "Competitor B"]
        return [
            ExecutiveSignal(
                title=f"{name} launched an AI executive workflow feature",
                summary="Positioning overlaps with daily briefings and decision support. Review differentiation and pricing.",
                priority=Priority.medium,
                confidence=0.72,
                source_refs=[SourceRef(provider="mock-market", title=f"{name} update")],
            )
            for name in names[:3]
        ]

    async def news_signals(self) -> list[ExecutiveSignal]:
        return [
            ExecutiveSignal(
                title="AI governance demand continues to increase",
                summary="Enterprise buyers are asking for stronger auditability, access controls and AI risk reporting.",
                priority=Priority.medium,
                confidence=0.8,
                source_refs=[SourceRef(provider="mock-news", title="AI governance market signal")],
            )
        ]

class RiskConnector:
    async def risk_signals(self) -> list[ExecutiveSignal]:
        return [
            ExecutiveSignal(
                title="Customer churn above tolerance",
                summary="Churn is 1.3 percentage points above target and trending upward. Investigate retention drivers.",
                priority=Priority.high,
                confidence=0.9,
                source_refs=[SourceRef(provider="mock-bi", title="Churn KPI")],
            ),
            ExecutiveSignal(
                title="Board materials incomplete",
                summary="Missing KPI and risk pack could reduce decision quality in tomorrow's meeting.",
                priority=Priority.medium,
                confidence=0.82,
                source_refs=[SourceRef(provider="mock-calendar", title="Board meeting")],
            ),
        ]
