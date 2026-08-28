# Security Policy

RaeburnAI Executive is designed for sensitive business workflows. Treat connected inbox, calendar, KPI and CRM data as confidential.

## Reporting vulnerabilities

Please do **not** disclose exploitable vulnerabilities through public issues. Report a suspected vulnerability privately through GitHub Security Advisories:

https://github.com/Raebu/RaeburnAI-Executive/security/advisories/new

If private reporting is unavailable, contact the repository maintainers through the repository owner profile rather than publishing exploit details.

Please include the affected component and version, reproduction steps or proof of concept, the expected impact, and any suggested remediation.

We aim to acknowledge a vulnerability report within **2 business days**, provide an initial assessment within **7 days**, and coordinate remediation and disclosure with the reporter. Unless an actively exploited vulnerability requires a faster response, coordinated public disclosure should normally occur after a fix is available and no later than **90 days** after confirmation.

Please keep vulnerability details confidential during the coordinated disclosure period. We will disclose security fixes transparently once affected users have a reasonable opportunity to update.

## Security expectations

- Never commit secrets.
- Use least-privilege API scopes for connectors and automation tokens.
- Encrypt secrets and tokens in production.
- Keep source references auditable.
- Avoid storing full email/calendar content unless explicitly required.
- Log metadata rather than sensitive payloads.
- Validate all connector input and output.
- Review third-party dependencies and security updates promptly.

## Production checklist

- Replace default secret values.
- Configure HTTPS at the edge.
- Add authentication and role-based access control.
- Use managed secret storage.
- Enable database backups.
- Enable audit logging.
- Review third-party data-processing agreements.
