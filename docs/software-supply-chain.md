# Software supply-chain policy

RaeburnAI Executive treats dependency resolution, GitHub Actions workflows, production images and release evidence as security boundaries.

## Dependency integrity

- Python production and CI environments are committed as hash-locked `requirements.lock` and `requirements-dev.lock` files generated from `apps/api/pyproject.toml`.
- CI installs the dev lock with `--require-hashes` and audits the production lock directly with `pip-audit`.
- The web app commits `apps/web/package-lock.json`, uses `npm ci` and blocks High/Critical npm audit findings.
- The invalid historical Atheris 3.1.0 declaration was corrected to the published 3.0.0 release during lock bootstrapping.
- FastAPI/Starlette and the web stack were moved to audited current lines during lock generation rather than retaining vulnerable historical dependency graphs.

## Workflow and container integrity

- Third-party Actions must be pinned to full 40-character commit SHAs.
- API and web images are built with exact Git SHA tags in CI and scanned with Trivy for High/Critical findings.
- CI starts both exact images and verifies API `/health` plus the web root before passing.
- API uses the verified `python:3.11-alpine3.24` OCI index in a two-stage build, installs only the hash-locked runtime graph, keeps build tooling out of runtime, and strips pip/setuptools/wheel from the final image.
- Web uses the verified Node 22.23.2/Alpine 3.24 OCI index, builds from `package-lock.json`, strips package-manager frontends and runs the Next standalone server as non-root.
- Compose Redis is pinned to the verified Redis 7 Alpine OCI index.

Verified OCI indexes resolved on a clean GitHub-hosted runner on 2026-09-19:
- Python 3.11 / Alpine 3.24: `sha256:0495f5559318affa673172ec7e35cd0a5213e4aaf4c76d0a66554c0af97b157e` (hosted resolver run `35467103270`)
- Node 22.23.2 / Alpine 3.24: `sha256:b6f26b36c8ff49624cfdac716b8ea1138d606df02586a77d364bb5536a634f85`
- Redis 7 Alpine: `sha256:520775a41a63e77e06c73e35d2fd9cc15921a609516818796b4ecbb813078bc7`

## Release trust evidence

`.github/workflows/release-trust.yml` is the sole owner of file release trust assets. It verifies the exact tag, creates one deterministic `git archive | gzip -n`, generates isolated SPDX and CycloneDX SBOMs, creates one SHA-256 manifest, keyless-signs the archive/checksums/SBOMs with Sigstore, creates GitHub build provenance and both SBOM attestations, verifies checksums/Sigstore/GitHub attestation before publication, and performs exactly one `gh release upload`.

`.github/workflows/sbom.yml` remains repository-SBOM-only. The previous independent provenance and release-signing workflows are removed because independently recreated/clobbered archives can make trust evidence refer to different bytes.

Container publication remains separate: `publish-containers.yml` publishes release-tagged GHCR images with BuildKit provenance/SBOM metadata and does not own GitHub release file assets.

**Real release evidence** requires an executed exact-tag trust workflow plus inspection of its published assets. Workflow source alone is Coded evidence.

## Remediation expectations

- **Critical:** block release immediately and remediate as soon as practicable, normally within 24 hours. Any exception must be explicit, time-bounded, owned and document compensating controls.
- **High:** block release and remediate normally within 7 days or use the same governed exception process.
- **Medium/Low:** triage based on exploitability, reachability and impact.

Security gates are not weakened merely to make CI green.


## API base-image remediation evidence

The first exact-head container gate correctly rejected the Debian 13.7 slim API image with 44 High OS findings, while the application Python packages themselves were clean. The API image was therefore moved to the official Python 3.11/Alpine 3.24 multi-platform index resolved on GitHub-hosted run `35467103270`, and unnecessary runtime packaging tools were removed rather than suppressing Trivy findings. This change is not considered Tested until the repository's exact-head API build, Trivy scan and live `/health` smoke test pass.
