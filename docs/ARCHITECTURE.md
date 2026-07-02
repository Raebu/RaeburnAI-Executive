# Architecture

RaeburnAI Executive is built around a connector-first briefing pipeline.

## Flow

```text
Connectors -> Normalisation -> Signal scoring -> Briefing orchestration -> Action generation -> API/Web delivery
```

## Core services

- `BriefingEngine`: coordinates the daily briefing.
- `EmailConnector`: returns prioritised inbox signals.
- `CalendarConnector`: identifies preparation gaps and schedule risks.
- `KpiConnector`: returns business metric snapshots.
- `SalesConnector`: returns CRM and pipeline signals.
- `RiskConnector`: converts operational and KPI issues into risk signals.
- `IntelligenceConnector`: returns competitor and market intelligence.

## Extension model

Each connector should expose a small async interface and return typed domain models. This keeps the product shippable with mock providers while allowing production deployments to wire in Gmail, Google Calendar, Microsoft 365, HubSpot, Salesforce, Stripe, QuickBooks, Xero, Looker, Power BI, Snowflake, Slack, GitHub and news providers.

## Data principles

- Store source references and freshness metadata.
- Keep raw sensitive content out of logs.
- Prefer short summaries over full data retention.
- Score confidence separately from priority.
- Keep actions explainable with rationale and source refs.
