# Deployment Guide

## Target architecture

- Frontend on Vercel
- Backend API on Railway or Render
- MCP server on a second Railway or Render service

This split matters because the production OpenAI MCP flow requires the MCP server to be publicly reachable.

## Vercel frontend

Create a new Vercel project and set the root directory to `frontend/`.

Settings:

- Framework preset: Vite
- Install command: `npm install`
- Build command: `npm run build`
- Output directory: `dist`

Environment variables:

- `VITE_API_BASE_URL=https://your-backend-service.example.com`

The file [frontend/vercel.json](C:/Users/YASH/OneDrive/Documents/Playground%202/frontend/vercel.json) is already included.

## Render deployment

You can deploy from [render.yaml](C:/Users/YASH/OneDrive/Documents/Playground%202/render.yaml).

Services created:

1. `ridgeway-api`
2. `ridgeway-mcp`

Backend env vars:

- `OPENAI_API_KEY`
- `OPENAI_MODEL=gpt-4.1`
- `OPENAI_TOOL_MODE=remote_mcp`
- `OPENAI_MCP_SERVER_URL=https://your-mcp-service.example.com/mcp`
- `BACKEND_CORS_ORIGINS=https://your-vercel-frontend.vercel.app`

MCP env vars:

- `MCP_PATH=/mcp`

After deploy:

1. copy the MCP URL
2. set it as `OPENAI_MCP_SERVER_URL` on the backend
3. copy the backend URL
4. set it as `VITE_API_BASE_URL` on Vercel
5. set the Vercel URL into `BACKEND_CORS_ORIGINS`

## Railway deployment

Railway works well, but each service should be deployed separately from the same repo.

### Railway service 1: backend API

Root directory: repo root

Build/install command:

```bash
pip install -r backend/requirements.txt
```

Start command:

```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

Environment variables:

- `OPENAI_API_KEY`
- `OPENAI_MODEL=gpt-4.1`
- `OPENAI_TOOL_MODE=remote_mcp`
- `OPENAI_MCP_SERVER_URL=https://your-mcp-service.example.com/mcp`
- `BACKEND_CORS_ORIGINS=https://your-vercel-frontend.vercel.app`

### Railway service 2: MCP server

Root directory: repo root

Build/install command:

```bash
pip install -r mcp_server/requirements.txt
```

Start command:

```bash
python -m mcp_server.server
```

Environment variables:

- `MCP_PATH=/mcp`

Health endpoint:

- `/health`

MCP endpoint:

- `/mcp`

## Recommended production sequence

1. Deploy the MCP server first.
2. Deploy the backend with `OPENAI_TOOL_MODE=remote_mcp`.
3. Deploy the frontend on Vercel.
4. Update frontend and backend env vars with the public URLs.
5. Run a live investigation with a real `OPENAI_API_KEY` to confirm the remote MCP path is active.
