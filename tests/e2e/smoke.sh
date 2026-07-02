#!/usr/bin/env bash
set -euo pipefail

API_URL="${API_URL:-http://localhost:8000}"

curl --fail --silent "$API_URL/health" >/dev/null
curl --fail --silent \
  -H 'Content-Type: application/json' \
  -d '{"organisation":"E2E Demo"}' \
  "$API_URL/v1/briefings/daily" | grep -q 'E2E Demo'

echo "E2E smoke test passed"
