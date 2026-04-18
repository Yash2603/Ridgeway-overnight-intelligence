# Ridgeway Overnight Intelligence

Production-ready submission for the Skylark assignment using the requested architecture:

- Frontend: React + Vite + Leaflet
- Backend: Python FastAPI
- AI layer: OpenAI Responses API tool-calling
- MCP layer: formal FastMCP server over streamable HTTP
- Data: fully simulated and seeded

## What this is

Ridgeway Overnight Intelligence is an AI-first operator console for making sense of a messy overnight shift before the 8:00 AM leadership review. The product helps Maya move from raw signals to a reviewable morning briefing with:

- map-based context
- tool-driven investigation
- surfaced uncertainty
- a human approval layer
- a lightweight drone follow-up mission

## Repo layout

- `frontend/`: React operator console
- `backend/`: FastAPI API and OpenAI orchestration
- `mcp_server/`: formal MCP server with incident tools
- `shared/`: seeded overnight site data
- `docs/`: deployment, write-up, demo script, and submission assets

## Quick Start Local

Run this locally first to verify everything works before deploying.

### 1. Create the Python environment

From the repo root:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m ensurepip --upgrade
.\.venv\Scripts\python -m pip install -r backend\requirements.txt -r mcp_server\requirements.txt
```

### 2. Install frontend dependencies

```powershell
cd frontend
npm install
cd ..
```

### 3. Optional: enable real OpenAI tool-calling

Create [backend/.env](C:/Users/YASH/OneDrive/Documents/Playground%202/backend/.env) from [backend/.env.example](C:/Users/YASH/OneDrive/Documents/Playground%202/backend/.env.example).

Minimum values:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1
OPENAI_TOOL_MODE=function_fallback
BACKEND_CORS_ORIGINS=http://localhost:5173
```

If you do not set `OPENAI_API_KEY`, the backend uses a deterministic fallback report so the app still runs.

### 4. Start the backend API

```powershell
.\.venv\Scripts\python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Health check:

- [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### 5. Start the MCP server

```powershell
.\.venv\Scripts\python -m mcp_server.server
```

Health check:

- [http://127.0.0.1:9000/health](http://127.0.0.1:9000/health)

MCP endpoint:

- [http://127.0.0.1:9000/mcp](http://127.0.0.1:9000/mcp)

### 6. Start the frontend

```powershell
cd frontend
npm run dev
```

Frontend URL:

- [http://localhost:5173](http://localhost:5173)

## Deploy Publicly

The intended hosted architecture is:

- Vercel for the frontend
- Render or Railway for the backend API
- Render or Railway for the MCP server

This split is important because the production OpenAI MCP flow requires the MCP server to be publicly reachable.

## Deploy To Vercel + Render

### Frontend on Vercel

Deploy `frontend/` as a Vite project.

Included config:

- [frontend/vercel.json](C:/Users/YASH/OneDrive/Documents/Playground%202/frontend/vercel.json)

Set this env var in Vercel:

```env
VITE_API_BASE_URL=https://your-backend-service.example.com
```

### Backend and MCP on Render

Included blueprint:

- [render.yaml](C:/Users/YASH/OneDrive/Documents/Playground%202/render.yaml)

Deploy two services:

1. `ridgeway-api`
2. `ridgeway-mcp`

Backend env vars:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1
OPENAI_TOOL_MODE=remote_mcp
OPENAI_MCP_SERVER_URL=https://your-mcp-service.example.com/mcp
BACKEND_CORS_ORIGINS=https://your-vercel-frontend.vercel.app
```

MCP env vars:

```env
MCP_PATH=/mcp
```

## Deploy To Railway

Railway is also supported. Use:

- [railway.toml](C:/Users/YASH/OneDrive/Documents/Playground%202/railway.toml)
- [docs/DEPLOYMENT.md](C:/Users/YASH/OneDrive/Documents/Playground%202/docs/DEPLOYMENT.md)

Create two Railway services from the same repo:

1. backend API
2. MCP server

Backend start command:

```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

MCP server start command:

```bash
python -m mcp_server.server
```

## Production Tool-Calling Modes

The backend supports two OpenAI modes:

1. `function_fallback`
   Best for local development. The model calls Python-defined tools directly.

2. `remote_mcp`
   Best for production. The model connects to the deployed MCP server through the OpenAI Responses API.

Recommended production setting:

```env
OPENAI_TOOL_MODE=remote_mcp
```

## Validation

Frontend build:

```powershell
cd frontend
npm run build
```

Backend tests:

```powershell
cd ..
.\.venv\Scripts\python -m pytest backend\tests
```

## Submission Assets

- Final write-up: [docs/ASSIGNMENT_WRITEUP.md](C:/Users/YASH/OneDrive/Documents/Playground%202/docs/ASSIGNMENT_WRITEUP.md)
- Demo script/storyboard: [docs/DEMO_SCRIPT.md](C:/Users/YASH/OneDrive/Documents/Playground%202/docs/DEMO_SCRIPT.md)
- Deployment guide: [docs/DEPLOYMENT.md](C:/Users/YASH/OneDrive/Documents/Playground%202/docs/DEPLOYMENT.md)
- OpenAI integration notes: [docs/OPENAI_INTEGRATION.md](C:/Users/YASH/OneDrive/Documents/Playground%202/docs/OPENAI_INTEGRATION.md)
- GitHub push guide: [docs/GITHUB_PUSH.md](C:/Users/YASH/OneDrive/Documents/Playground%202/docs/GITHUB_PUSH.md)

## Notes

- The map is part of the reasoning workflow, not decoration.
- The AI layer exposes tool trace and uncertainty explicitly.
- The operator remains the approval layer before the morning briefing is treated as final.
