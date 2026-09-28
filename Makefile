PYTHON ?= python
PIP ?= pip
BACKEND_DIR := backend
FRONTEND_DIR := frontend

.PHONY: install backend-test frontend-build run docker-up

install:
	cd $(BACKEND_DIR) && $(PYTHON) -m pip install -r requirements.txt
	cd $(FRONTEND_DIR) && npm install

backend-test:
	cd $(BACKEND_DIR) && $(PYTHON) -m pytest -q

frontend-build:
	cd $(FRONTEND_DIR) && npm run build

run:
	cd $(BACKEND_DIR) && $(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

docker-up:
	docker compose up --build
