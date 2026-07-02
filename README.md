# RaeburnAI Executive

**A CEO's second brain for daily executive briefings, strategic insight, KPI monitoring, risk detection, market intelligence, and decision support.**

RaeburnAI Executive turns emails, calendar events, KPIs, sales signals, risks, competitor updates, and news into a concise daily briefing with recommended actions.

## Core capabilities

- Daily executive briefing generation
- Important email prioritisation
- Calendar and meeting risk review
- KPI monitoring and anomaly detection
- Sales pipeline and revenue insight
- Competitor and market intelligence
- News summarisation
- Risk register and suggested mitigations
- Suggested CEO actions with priority, owner, due date, and rationale
- API-first architecture for integration with Gmail, Calendar, CRM, BI, and news providers
- Open-source, extensible connector model

## Architecture

```text
apps/api          FastAPI service and briefing orchestration
apps/web          Next.js executive dashboard
packages/core     Shared TypeScript domain contracts
examples          Example payloads and demo data
.github           CI and project automation
```

## Quick start

```bash
cp .env.example .env
make install
make dev
```

API: <http://localhost:8000/docs>  
Web: <http://localhost:3000>

## Production deployment

```bash
docker compose up --build
```

## Briefing model

A briefing is composed from independent intelligence sections:

1. Executive summary
2. Priority inbox
3. Calendar review
4. KPI pulse
5. Sales pulse
6. Risk watch
7. Competitor intelligence
8. Market/news intelligence
9. Suggested actions

Each section includes confidence, source references, and freshness metadata.

## Open-source excellence principles

- Clear domain boundaries
- Connector-first architecture
- Secure-by-default configuration
- Typed contracts
- Testable services
- CI quality gates
- Dockerised local and production workflows
- Contribution and security guidance
- No hard-coded secrets

## Repository status

This repository contains the production-grade foundation for RaeburnAI Executive. Integrations are implemented as replaceable connectors so the platform can ship with mock/demo providers and scale into enterprise data sources.

## License

MIT. See [LICENSE](LICENSE).
