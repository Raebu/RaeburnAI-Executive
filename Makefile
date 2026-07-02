.PHONY: install dev api web test lint format typecheck build docker docker-build security

install:
	python -m pip install -e apps/api[dev]
	cd apps/web && npm install

dev:
	make api & make web

api:
	uvicorn raeburnai_executive.main:app --app-dir apps/api --reload --host 0.0.0.0 --port 8000

web:
	cd apps/web && npm run dev

test:
	cd apps/api && pytest

lint:
	cd apps/api && ruff check .
	cd apps/web && npm run lint

format:
	cd apps/api && ruff format .

typecheck:
	cd apps/api && mypy raeburnai_executive
	cd apps/web && npm run typecheck

build:
	cd apps/web && npm run build
	docker compose config

security:
	cd apps/api && bandit -q -r raeburnai_executive

docker-build:
	docker build -f Dockerfile.api -t raeburnai-executive-api .
	docker build -f Dockerfile.web -t raeburnai-executive-web .

docker:
	docker compose up --build
