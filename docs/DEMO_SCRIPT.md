# Demo Script and Storyboard

## Demo goal

Show that the product is not a dashboard with AI on the side. It is an AI-first investigation workflow where the map, tools, uncertainty handling, and human review all matter.

## Recommended video length

5 to 7 minutes

## Demo structure

### Scene 1: Problem setup

Duration: 30 to 45 seconds

Voiceover:

"It’s 6:10 AM at Ridgeway Site. Maya, the operations lead, has less than two hours before the morning review. Overnight, the site saw a fence alert, suspicious vehicle movement, failed badge swipes, and a drone patrol over the same area. The question isn’t whether signals exist. The question is what actually happened and what matters right now."

On screen:

- open the app landing view
- show the hero summary
- point out the current investigation mode and overnight signal count

### Scene 2: Spatial understanding

Duration: 45 to 60 seconds

Voiceover:

"The map is part of the workflow, not decoration. The operator can immediately see that Gate 3 and Block C are the hotspot zones, and the follow-up drone route is anchored to the likely ingress and egress path."

On screen:

- zoom or pan around the Leaflet map
- click Block C
- click Gate 3
- show the drone route overlay

### Scene 3: AI-first investigation

Duration: 60 to 90 seconds

Voiceover:

"Instead of asking the operator to manually stitch everything together, the AI layer investigates first. It can pull incident context, badge system anomalies, zone context, and a follow-up mission plan. The output is structured as a morning briefing draft, not just a raw answer."

On screen:

- show the operator note box
- click `Re-run investigation`
- wait for the refreshed result
- point to the updated mode label if OpenAI is configured

### Scene 4: Tool trace and trust

Duration: 45 to 60 seconds

Voiceover:

"A key design goal was trust. The system shows how it worked. Maya can inspect which tools were used, why they were used, and what they returned. This makes the agent challengeable instead of opaque."

On screen:

- scroll to the tool trace section
- highlight each tool card
- explain the difference between local function-calling mode and remote MCP mode

### Scene 5: Findings and uncertainty

Duration: 60 to 90 seconds

Voiceover:

"The system doesn’t flatten uncertainty into overconfidence. It proposes findings, gives confidence levels, and explicitly surfaces what still needs human judgment. In this case, the most likely story is a short reconnaissance or unauthorized inspection near Block C, but there isn’t enough evidence to claim a confirmed theft."

On screen:

- highlight the critical and high-severity findings
- scroll to the uncertainty section
- call out one uncertainty line explicitly

### Scene 6: Morning briefing and handoff

Duration: 45 to 60 seconds

Voiceover:

"The final step is not another dashboard interaction. It’s decision support. Maya gets a morning briefing draft with what happened, which signals were harmless, what deserves escalation, and what the team should do next."

On screen:

- show the briefing draft section
- point out escalation items
- point out follow-ups

### Scene 7: Deployment and architecture close

Duration: 30 to 45 seconds

Voiceover:

"Under the hood, the system uses a React frontend, a FastAPI backend, OpenAI Responses API tool-calling, and a formal MCP server. It is structured to run locally in function-calling mode and in production with a deployed remote MCP service."

On screen:

- briefly show repo tree or architecture diagram slide
- show deployment doc or code layout

## Optional architecture slide

You can include a single architecture slide with:

- Vercel hosting the React frontend
- Railway or Render hosting the FastAPI backend
- Railway or Render hosting the MCP server
- OpenAI Responses API calling either local functions or the deployed MCP endpoint

## Recording tips

- Keep the browser zoom high enough for labels to be readable
- Use seeded data consistently for repeatable takes
- If OpenAI is not configured live, explain that the deterministic fallback keeps the demo stable while the production path uses remote MCP mode
