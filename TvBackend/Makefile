.PHONY: install run migrate revision seed superuser import test lint fmt typecheck check

VENV ?= .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

install:  ## Create venv and install the package with dev extras
	python3.12 -m venv $(VENV)
	$(PIP) install -U pip
	$(PIP) install -e ".[dev]"

run:  ## Run the dev server with autoreload
	$(VENV)/bin/uvicorn ssmarttv.main:app --reload --port 8000

migrate:  ## Apply migrations
	$(VENV)/bin/alembic upgrade head

revision:  ## Autogenerate a migration: make revision m="message"
	$(VENV)/bin/alembic revision --autogenerate -m "$(m)"

seed:  ## Seed reference data (roles, permissions, genres, countries)
	$(PY) scripts/seed_reference.py

superuser:  ## Create a superuser: make superuser u=admin p=secret
	$(PY) scripts/bootstrap_superuser.py --username "$(u)" --password "$(p)"

import:  ## Import channels: make import f=data/uzbek-channels.m3u c=uz
	$(PY) scripts/import_m3u.py "$(f)" --country "$(c)"

test:  ## Run the test suite
	$(VENV)/bin/pytest -q

lint:  ## Lint with ruff
	$(VENV)/bin/ruff check src scripts tests

fmt:  ## Auto-fix lint issues
	$(VENV)/bin/ruff check --fix src scripts tests

typecheck:  ## Type-check with mypy
	$(VENV)/bin/mypy src

check: lint typecheck test  ## Run all quality gates
