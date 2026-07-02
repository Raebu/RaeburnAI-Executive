# RaeburnAI Executive

[![CI](https://github.com/Raebu/RaeburnAI-Executive/actions/workflows/ci.yml/badge.svg)](https://github.com/Raebu/RaeburnAI-Executive/actions/workflows/ci.yml)
[![CodeQL](https://github.com/Raebu/RaeburnAI-Executive/actions/workflows/codeql.yml/badge.svg)](https://github.com/Raebu/RaeburnAI-Executive/actions/workflows/codeql.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

## One-line positioning statement

A CEO's second brain for daily executive briefings, KPI monitoring, market intelligence, risk detection and decision support.

## Short product description

RaeburnAI Executive turns emails, calendar events, KPIs, sales signals, risks, competitor updates and news into a concise daily briefing with recommended actions. It is designed as an extensible open-source foundation for executive operating systems, board preparation, founder dashboards and AI-assisted leadership workflows.

## Part of the RaeburnAI Platform

RaeburnAI Executive is part of the RaeburnAI Platform: an open, modular enterprise AI ecosystem for governance, intelligence, automation, operations and decision support.

The platform is designed so each project can run independently while also working as part of a broader AI operating layer for modern organisations.

### Ecosystem map

```text
RaeburnAI Platform
├── RaeburnAI Executive              CEO briefings, decision support and strategic actions
├── RaeburnAI Compliance Engine      AI governance, GDPR, ISO and EU AI Act readiness
├── Universal AI Knowledge Graph     Shared organisational intelligence and context layer
├── RaeburnAI Business Twin          Business simulation, operating model and scenario planning
├── RaeburnAI Executive Briefing     Board and leadership briefing generation
├── OpenAI Operations Dashboard      Model usage, spend, latency, safety and audit analytics
├── RaeburnAI Proposal Generator     Consulting proposals, roadmaps, pricing and ROI analysis
├── RaeburnAI Meeting Intelligence   Decisions, actions, owners and follow-up automation
└── RaeburnAI Workflow Auditor       Workflow analysis, automation opportunities and savings
```

### Core project links

- [RaeburnAI Compliance Engine](https://github.com/Raebu/RaeburnAI-Compliance-Engine)
- [Universal AI Knowledge Graph](https://github.com/Raebu/Universal-AI-Knowledge-Graph)
- [RaeburnAI Business Twin](https://github.com/Raebu/RaeburnAI-Business-Twin)
- [OpenAI Operations Dashboard](https://github.com/Raebu/OpenAI-Operations-Dashboard)
- [RaeburnAI Proposal Generator](https://github.com/Raebu/RaeburnAI-Proposal-Generator)
- [RaeburnAI Meeting Intelligence](https://github.com/Raebu/RaeburnAI-Meeting-Intelligence)
- [RaeburnAI Workflow Auditor](https://github.com/Raebu/RaeburnAI-Workflow-Auditor)

## Core features

- Daily executive briefing generation
- Important email prioritisation
- Calendar and board-preparation review
- KPI monitoring and anomaly surfacing
- Sales pipeline and revenue insight
- Competitor and market intelligence sections
- News and external signal summaries
- Risk register and mitigation prompts
- Suggested actions with priority, owner, due date and rationale
- API key guard, input validation and rate limiting
- Human approval requirement for risky write-style actions
- Health and readiness endpoints
- Structured application logging
- CI, CodeQL, dependency review and Dependabot baseline

## Architecture

```text
apps/api          FastAPI briefing API and orchestration engine
apps/web          Next.js executive dashboard
examples          Demo payloads and example usage data
docs              Architecture, deployment and screenshot documentation
tests/e2e         Basic end-to-end smoke checks
.github           CI, CodeQL and dependency automation
```

Briefing flow:

```text
Connectors -> Normalisation -> Signal scoring -> Briefing orchestration -> Action generation -> API/Web delivery
```

The current implementation ships with mock providers so the product can run locally without external secrets. Production deployments should replace these providers with least-privilege integrations for inbox, calendar, CRM, BI, finance and news systems.

## Quick start

```bash
cp .env.example .env
make install
make test
make lint
make typecheck
make build
make dev
```

API documentation: <http://localhost:8000/docs>  
Web dashboard: <http://localhost:3000>

Docker:

```bash
cp .env.example .env
make docker-build
docker compose up
```

## Environment variables

| Variable | Purpose | Default |
| --- | --- | --- |
| `RAEBURNAI_ENV` | Runtime environment | `development` |
| `RAEBURNAI_API_HOST` | API bind host | `0.0.0.0` |
| `RAEBURNAI_API_PORT` | API port | `8000` |
| `RAEBURNAI_WEB_URL` | Allowed web origin for CORS | `http://localhost:3000` |
| `RAEBURNAI_API_URL` | Public API URL | `http://localhost:8000` |
| `RAEBURNAI_SECRET_KEY` | API key / app secret placeholder | `change-me` |
| `RAEBURNAI_DATABASE_URL` | Future persistence connection string | `sqlite:///./raeburnai_executive.db` |
| `RAEBURNAI_REDIS_URL` | Future distributed cache / limiter URL | `redis://redis:6379/0` |
| `RAEBURNAI_LLM_PROVIDER` | LLM provider selector | `mock` |
| `OPENAI_API_KEY` | Optional LLM provider key | empty |
| `NEWS_API_KEY` | Optional news provider key | empty |
| `CRM_PROVIDER` | CRM connector selector | `mock` |
| `CRM_API_KEY` | Optional CRM connector key | empty |

## Usage examples

Generate a daily briefing:

```bash
curl -X POST http://localhost:8000/v1/briefings/daily \
  -H 'Content-Type: application/json' \
  -d @examples/demo-data.json
```

Run the E2E smoke test after starting the API:

```bash
bash tests/e2e/smoke.sh
```

Human-approved action request:

```bash
curl -X POST http://localhost:8000/v1/actions/execute \
  -H 'Content-Type: application/json' \
  -H 'X-Human-Approval: approved' \
  -d '{"action_title":"Create board pack","target_system":"calendar","dry_run":true}'
```

## Security model

- No secrets are committed to the repository.
- `.env.example` documents required configuration without real credentials.
- API requests support an API-key guard via `X-API-Key` outside local development.
- Risky write-style actions require `X-Human-Approval: approved`.
- Input models use Pydantic validation and bounded field lengths.
- CORS is restricted to the configured web origin.
- Basic in-memory rate limiting protects briefing and action endpoints.
- Structured logs record request metadata and action audit IDs.
- Containers run as non-root users with hardened compose settings.

Production TODOs are intentionally documented rather than hidden: replace in-memory rate limiting with Redis, add persistent audit storage, add SSO/RBAC and wire real OAuth connectors.

## Production readiness

Implemented:

- Install, lint, typecheck, test, build and Docker build commands
- Unit tests and API integration tests
- Basic E2E smoke test
- CI pipeline
- CodeQL security scanning
- Dependency review and Dependabot
- Dockerfile and docker-compose
- Health and readiness endpoints
- Security, contribution, deployment, roadmap and screenshot docs

Known remaining work before regulated enterprise use:

- Real production connectors for Gmail/Microsoft 365, calendar, CRM, BI and news providers
- Persistent database-backed audit logs
- Redis-backed distributed rate limiting
- Enterprise SSO/RBAC
- Background scheduler and delivery channels
- Production UI screenshots after deployment

## Roadmap

See [ROADMAP.md](ROADMAP.md).

Near-term priorities:

1. Real inbox and calendar connectors
2. CRM and finance KPI connectors
3. Persistent audit logging
4. SSO/RBAC
5. Scheduled daily delivery to email, Slack and Teams
6. Advanced competitor monitoring

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

Please keep connectors isolated, avoid committing sensitive data, add tests for new behaviour and follow the same README/documentation structure used across the RaeburnAI ecosystem.

## Licence

Apache-2.0. See [LICENSE](LICENSE).
