.PHONY: install dev api web test lint docker

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
	docker compose config

docker:
	docker compose up --build
