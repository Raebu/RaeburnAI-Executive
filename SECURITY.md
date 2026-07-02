# Security Policy

RaeburnAI Executive is designed for sensitive business workflows. Treat connected inbox, calendar, KPI and CRM data as confidential.

## Reporting vulnerabilities

Please open a private security advisory on GitHub or contact the project maintainers directly. Do not disclose exploitable vulnerabilities publicly until a fix is available.

## Security expectations

- Never commit secrets.
- Use least-privilege API scopes for connectors.
- Encrypt secrets and tokens in production.
- Keep source references auditable.
- Avoid storing full email/calendar content unless explicitly required.
- Log metadata rather than sensitive payloads.
- Validate all connector input and output.

## Production checklist

- Replace default secret values.
- Configure HTTPS at the edge.
- Add authentication and role-based access control.
- Use managed secret storage.
- Enable database backups.
- Enable audit logging.
- Review third-party data-processing agreements.
