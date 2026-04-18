export interface Zone {
  id: string;
  label: string;
  kind: string;
  x: number;
  y: number;
  width: number;
  height: number;
  risk_weight: number;
  description: string;
}

export interface Event {
  id: string;
  type: string;
  zone_id: string;
  started_at: string;
  ended_at?: string | null;
  title: string;
  detail: string;
  severity: "low" | "medium" | "high" | "critical";
  confidence: number;
  actor?: string | null;
  metadata: Record<string, unknown>;
}

export interface SiteContextResponse {
  site_name: string;
  shift_note: string;
  zones: Zone[];
  events: Event[];
}

export interface ToolTrace {
  tool: string;
  source: "mcp" | "function" | "system";
  reason: string;
  input_summary: string;
  output_summary: string;
}

export interface Finding {
  id: string;
  title: string;
  narrative: string;
  severity: "low" | "medium" | "high" | "critical";
  confidence: number;
  status: "pending" | "approved" | "needs-follow-up";
  supporting_event_ids: string[];
  recommended_action: string;
}

export interface MissionPlan {
  title: string;
  objective: string;
  rationale: string;
  eta_minutes: number;
  route_zone_ids: string[];
}

export interface Briefing {
  headline: string;
  summary: string;
  what_happened: string[];
  harmless_signals: string[];
  escalation_items: string[];
  follow_ups: string[];
}

export interface InvestigationResponse {
  mode: "openai_remote_mcp" | "openai_function_fallback" | "deterministic_fallback";
  generated_at: string;
  site_name: string;
  agent_summary: string;
  briefing: Briefing;
  findings: Finding[];
  mission: MissionPlan;
  uncertainties: string[];
  tool_trace: ToolTrace[];
  raw_output_text: string;
}
