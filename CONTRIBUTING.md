# Contributing

Thank you for helping improve RaeburnAI Executive.

## Development

1. Fork the repository.
2. Create a feature branch.
3. Run `make install`.
4. Run `make test` and `make lint` before opening a pull request.

## Standards

- Keep connectors isolated from core briefing logic.
- Do not commit secrets, private customer data, email bodies, calendar exports, or proprietary CRM data.
- Add tests for orchestration, scoring, connectors and API behaviour.
- Prefer small, reviewable pull requests.

## Good first areas

- New connectors for CRM, BI, inbox, calendar, project management and news providers.
- Better KPI anomaly detection.
- Executive action scoring.
- Notification and digest delivery channels.
