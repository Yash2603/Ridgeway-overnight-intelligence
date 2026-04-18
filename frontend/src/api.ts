import type { InvestigationResponse, SiteContextResponse } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export async function fetchSiteContext(): Promise<SiteContextResponse> {
  const response = await fetch(`${API_BASE_URL}/api/site-context`);
  if (!response.ok) {
    throw new Error("Failed to load site context.");
  }
  return response.json();
}

export async function runInvestigation(operatorNote: string): Promise<InvestigationResponse> {
  const response = await fetch(`${API_BASE_URL}/api/investigate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ operator_note: operatorNote })
  });
  if (!response.ok) {
    throw new Error("Failed to run investigation.");
  }
  return response.json();
}
