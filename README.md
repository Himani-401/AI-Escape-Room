# AI Escape Room – Vision Meets Reasoning

An immersive local escape-room game that blends symbolic vision analysis, semantic retrieval, and a graph-based reasoning workflow. The project runs locally with a FastAPI backend and a lightweight React frontend.

## Features

- Session-based escape room orchestration
- Puzzle generation with a seeded graph and progression logic
- Vision pipeline for symbol detection and image analysis
- Semantic retrieval and knowledge grounding with FAISS
- LLM-ready reasoning with offline deterministic fallback
- Docker Compose support for local execution
- FastAPI testing suite and e2e demo script

## Stack

- Backend: Python 3.11+, FastAPI, SQLAlchemy, SQLite
- Vision: OpenCV, numpy, PIL
- Retrieval: sentence-transformers, FAISS
- Reasoning: LangGraph, LangChain, optional OpenAI/Anthropic clients
- Frontend: React, Vite, TypeScript, Tailwind CSS
- Runtime: Docker Compose

## Local setup

### Option 1: Docker

```bash
docker compose up --build
```

Then open:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/docs

### Option 2: Local development

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
cd frontend && npm install
```

Start the services separately:

```bash
cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
cd frontend && npm run dev
```

## Project structure

```text
backend/
  app/
    core/
    db/
    graph/
    llm/
    puzzles/
    rag/
    vision/
    main.py
  tests/
  scripts/
frontend/
  src/
  package.json
Makefile
docker-compose.yml
README.md
```

## Usage flow

1. Start the app.
2. Create a new session from the web UI or API.
3. Submit answers to progress through puzzle stages.
4. Ask for hints when the reasoning path stalls.
5. Complete the room by solving the final challenge.

## API

The backend exposes session, answer, and hint routes via FastAPI. Open the Swagger UI at:

- http://localhost:8000/docs

Example session creation:

```bash
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"player_name":"Operator","puzzle_seed":42}'
```

## Verification

Run the backend tests:

```bash
cd backend && pytest -q
```

Run the demo script:

```bash
cd backend && python scripts/e2e_demo.py
```

## Notes

This project is intentionally self-contained and can run without external API keys. If OpenAI or Anthropic keys are configured, the app may switch to those providers. Otherwise it uses an offline deterministic fallback to ensure the room still runs locally.
