# RAGOps Makefile

.PHONY: bootstrap dev test lint deploy-staging

bootstrap:
	pip install pre-commit && pre-commit install
	cp .env.example .env
	docker compose pull

dev:
	docker compose up -d postgres redis qdrant
	cd services/auth      && uvicorn app.main:app --reload --port 8000 &
	cd services/embedding && uvicorn app.main:app --reload --port 8001 &
	cd services/rag-engine && uvicorn app.main:app --reload --port 8003 &

test:
	pytest services/ -v --cov=services --cov-report=html

lint:
	ruff check . && mypy services/ && eslint frontend/src

migrate:
	cd migrations && alembic upgrade head