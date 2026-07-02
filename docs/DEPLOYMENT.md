# Production Deployment

## Recommended architecture

- API: containerised FastAPI service behind an HTTPS load balancer.
- Web: containerised Next.js app or standalone deployment.
- Cache: managed Redis where async jobs are enabled.
- Secrets: managed secret store such as GitHub Actions secrets, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, Doppler, 1Password or Vault.
- Observability: structured logs, uptime checks, error alerts and audit log export.

## Minimum production checklist

1. Set `RAEBURNAI_ENV=production`.
2. Replace `RAEBURNAI_SECRET_KEY` with a high-entropy value.
3. Serve API and web through HTTPS.
4. Restrict CORS to the deployed web origin.
5. Use least-privilege OAuth scopes for inbox, calendar, CRM and BI providers.
6. Enable CodeQL, Dependabot and branch protection.
7. Run `make lint`, `make typecheck`, `make test`, `make build` and `make docker-build` before release.

## Docker deployment

```bash
cp .env.example .env
make docker-build
docker compose up -d
```

## Kubernetes notes

- Run the API as a Deployment with readiness and liveness probes pointed at `/ready` and `/health`.
- Mount secrets from the platform secret manager.
- Use a NetworkPolicy to restrict egress to approved providers.
- Configure horizontal autoscaling on CPU and request latency.

## TODO before regulated enterprise rollout

- Replace in-memory rate limiting with Redis-backed distributed rate limiting.
- Add persistent audit-log storage.
- Add real OAuth connector implementations.
- Add SSO/RBAC for multi-user deployments.
