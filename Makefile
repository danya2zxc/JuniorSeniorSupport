# ===============================
# Constants
# ===============================
COMPOSE := docker compose
SERVICE := api

# ===============================
# Phony targets
# ===============================
.PHONY: run up down restart build logs migrate shell lint fix test

# ===============================
# Development
# ===============================
run:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

lint:
	python -m ruff . && python -m black --check . && python -m isort --check .

fix:
	python -m ruff --fix . && python -m black . && python -m isort .

test:
	pytest -v

# ===============================
# Docker
# ===============================
up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build

restart:
	$(COMPOSE) down && $(COMPOSE) up --build -d

logs:
	$(COMPOSE) logs -f $(SERVICE)

shell:
	$(COMPOSE) exec $(SERVICE) bash

# ===============================
# Database
# ===============================
migrate:
	$(COMPOSE) exec $(SERVICE) alembic upgrade head

# ===============================
# Celery
# ===============================
broker:
	celery -A src.mailing.celery_app worker --pool threads --loglevel=INFO
