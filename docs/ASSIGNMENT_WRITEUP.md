# Final Assignment Write-Up

## Project

Ridgeway Overnight Intelligence is an AI-first operator console for reviewing overnight site activity and preparing a trustworthy 8:00 AM morning briefing.

The product is designed for the exact moment described in the assignment: Maya arrives at 6:10 AM, knows something happened overnight, and needs a system that investigates before she manually stitches together logs, camera notes, access anomalies, and drone patrol context.

## Problem framing

The core product problem is not dashboarding. It is judgment under uncertainty.

Operators do not need a prettier log viewer. They need a system that:

- investigates first
- uses tools transparently
- exposes uncertainty honestly
- keeps the human in control
- helps produce an actionable briefing under time pressure

That framing drove the architecture and interface decisions.

## Tech approach

- Frontend: React + Vite + Leaflet
- Backend: FastAPI
- AI layer: OpenAI Responses API with real tool-calling
- MCP layer: formal FastMCP server over streamable HTTP
- Data: seeded/simulated incidents, zones, and patrol context

This matches the suggested stack while keeping the system realistic and deployable.

## Product workflow

1. The operator opens the console and sees the map, overnight signals, and the current AI-generated investigation state.
2. The AI layer investigates the overnight incident using tools instead of answering from raw prompt context alone.
3. The system produces a structured briefing draft, findings, uncertainties, and a follow-up drone mission.
4. Maya reviews the output, challenges it if needed, and decides what to escalate.

## Agent design

The agent has two execution modes:

### 1. Local function-calling mode

For local development, the backend exposes tools directly to the model through OpenAI function-calling. This avoids needing a public MCP endpoint while preserving the same reasoning contract.

### 2. Remote MCP mode

For production, the backend passes a remote MCP server into the OpenAI Responses API. The model can call the formal MCP tools directly over HTTP.

This gives the product a real MCP-backed architecture instead of a purely mocked interface.

## Tool design

The MCP server exposes four operator-relevant tools:

- `fetch_incident_log`
- `query_badge_system`
- `get_zone_context`
- `simulate_drone_followup`

These were chosen because they map directly to the assignment prompt:

- overnight incident investigation
- badge/access context
- spatial zone understanding
- lightweight drone follow-up simulation

## Why the map matters

The spatial interface is not decorative. It is part of the reasoning flow.

The operator needs to understand:

- where the initial anomaly happened
- how the suspicious activity moved
- which areas carry the most risk
- how the drone follow-up route relates to likely ingress and egress paths

Using Leaflet keeps the map interactive while staying lightweight and fast to deploy.

## Human review layer

The system explicitly avoids replacing the operator. The interface preserves human judgment by exposing:

- tool trace
- finding confidence
- surfaced uncertainty
- a reviewable morning briefing draft

That was intentional because the assignment emphasized trust, challengeability, and human control.

## Tradeoffs

### What I intentionally did not build

- real drone integration
- live video ingestion
- image processing
- physics-heavy flight simulation
- real sensor integrations

Those were explicitly out of scope, so I used seeded data and a lightweight mission simulation.

### Why simulated data was the right choice

It keeps the product deterministic for demos, easier to evaluate, and aligned with the assignment.

### Why two tool modes exist

Remote MCP is the strongest production architecture, but function-calling is much smoother for local development. Supporting both made the system practical to build and realistic to deploy.

## How AI tools were used during development

AI-assisted development was used to accelerate:

- initial product scaffolding
- refactoring to the exact requested stack
- structuring the investigation flow
- generating deployment and submission assets
- tightening validation and deployment ergonomics

The key principle was to use AI as a productivity multiplier while keeping the product decisions, system shape, and final implementation grounded in the assignment requirements.

## What I would do next with more time

- add authentication and session persistence
- store investigation runs for auditability
- support operator feedback loops that fine-tune future investigations
- add richer mission editing and route constraints
- deploy the remote MCP path and verify it against live OpenAI runs in production

## Summary

The final product aims to make AI feel like a working operational layer, not a chatbot bolted onto a dashboard.

It investigates first, uses tools transparently, keeps the human in control, and helps Maya answer the morning question that matters:

What happened, what matters, and what do I need to care about right now?
