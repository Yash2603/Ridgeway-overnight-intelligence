import { useEffect, useMemo, useState } from "react";
import { CRS, LatLngBoundsExpression } from "leaflet";
import { CircleMarker, MapContainer, Polygon, Polyline, Popup, Rectangle, TileLayer } from "react-leaflet";

import { fetchSiteContext, runInvestigation } from "./api";
import type { Event, InvestigationResponse, SiteContextResponse, Zone } from "./types";

const severityClass: Record<Event["severity"], string> = {
  low: "low",
  medium: "medium",
  high: "high",
  critical: "critical"
};

const mapBounds: LatLngBoundsExpression = [
  [0, 0],
  [100, 100]
];

function formatTime(value: string) {
  return new Intl.DateTimeFormat("en-IN", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
    timeZone: "UTC"
  }).format(new Date(value));
}

function zoneBounds(zone: Zone): LatLngBoundsExpression {
  const south = 100 - (zone.y + zone.height);
  const north = 100 - zone.y;
  return [
    [south, zone.x],
    [north, zone.x + zone.width]
  ];
}

function zoneCenter(zone: Zone): [number, number] {
  return [100 - (zone.y + zone.height / 2), zone.x + zone.width / 2];
}

export function App() {
  const [context, setContext] = useState<SiteContextResponse | null>(null);
  const [investigation, setInvestigation] = useState<InvestigationResponse | null>(null);
  const [operatorNote, setOperatorNote] = useState("Escalate anything related to Block C and surface uncertainty clearly.");
  const [isLoading, setIsLoading] = useState(true);
  const [isInvestigating, setIsInvestigating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function bootstrap() {
      try {
        const siteContext = await fetchSiteContext();
        setContext(siteContext);
        const initialInvestigation = await runInvestigation(operatorNote);
        setInvestigation(initialInvestigation);
      } catch (caughtError) {
        setError(caughtError instanceof Error ? caughtError.message : "Unable to load application.");
      } finally {
        setIsLoading(false);
      }
    }

    void bootstrap();
  }, []);

  const sortedEvents = useMemo(() => {
    return [...(context?.events ?? [])].sort(
      (left, right) => new Date(left.started_at).getTime() - new Date(right.started_at).getTime()
    );
  }, [context?.events]);

  async function handleInvestigate() {
    setIsInvestigating(true);
    setError(null);
    try {
      const response = await runInvestigation(operatorNote);
      setInvestigation(response);
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Investigation failed.");
    } finally {
      setIsInvestigating(false);
    }
  }

  if (isLoading) {
    return <main className="screen center">Loading Ridgeway overnight intelligence...</main>;
  }

  if (!context || !investigation) {
    return <main className="screen center">{error ?? "Missing application data."}</main>;
  }

  const route = investigation.mission.route_zone_ids
    .map((zoneId) => context.zones.find((zone) => zone.id === zoneId))
    .filter((zone): zone is Zone => Boolean(zone))
    .map(zoneCenter);

  return (
    <main className="screen">
      <section className="hero card">
        <div>
          <p className="eyebrow">React frontend + Python API + MCP server</p>
          <h1>Morning clarity before the 8:00 AM review.</h1>
          <p className="lede">
            Maya gets one surface that combines map context, AI investigation, tool traces, and a human approval flow.
          </p>
          <div className="chips">
            <span>AI-first workflow</span>
            <span>Formal MCP tool layer</span>
            <span>Leaflet spatial review</span>
          </div>
        </div>
        <div className="hero-stats">
          <div>
            <strong>{context.events.length}</strong>
            <span>overnight signals</span>
          </div>
          <div>
            <strong>{investigation.findings.length}</strong>
            <span>active findings</span>
          </div>
          <div>
            <strong>{investigation.mission.eta_minutes} min</strong>
            <span>follow-up sweep</span>
          </div>
        </div>
      </section>

      <section className="layout">
        <div className="left-column">
          <article className="card">
            <div className="section-head">
              <div>
                <p className="eyebrow">Spatial view</p>
                <h2>Ridgeway incident map</h2>
              </div>
              <span className="mode-pill">{investigation.mode}</span>
            </div>
            <p className="muted">
              Gate 3 and Block C are the primary hotspot zones. The orange route is the recommended follow-up mission.
            </p>
            <div className="map-shell">
              <MapContainer
                crs={CRS.Simple}
                bounds={mapBounds}
                maxBounds={mapBounds}
                zoom={0}
                minZoom={-1}
                scrollWheelZoom={false}
                style={{ height: "100%", width: "100%" }}
              >
                <TileLayer url="data:image/gif;base64,R0lGODlhAQABAAAAACwAAAAAAQABAAA=" />
                {context.zones.map((zone) => (
                  <Rectangle
                    key={zone.id}
                    bounds={zoneBounds(zone)}
                    pathOptions={{
                      color: zone.id === "block-c" || zone.id === "gate-3" ? "#d56d23" : "#3c7f65",
                      weight: 2,
                      fillOpacity: 0.25
                    }}
                  >
                    <Popup>
                      <strong>{zone.label}</strong>
                      <div>{zone.description}</div>
                    </Popup>
                  </Rectangle>
                ))}
                <Polyline positions={route} pathOptions={{ color: "#d56d23", weight: 3, dashArray: "6 6" }} />
                {context.zones.map((zone) => (
                  <CircleMarker
                    key={`${zone.id}-marker`}
                    center={zoneCenter(zone)}
                    radius={5}
                    pathOptions={{ color: "#241a14", weight: 2, fillColor: "#fffaf3", fillOpacity: 1 }}
                  >
                    <Popup>{zone.label}</Popup>
                  </CircleMarker>
                ))}
                <Polygon
                  positions={[
                    [72, 6],
                    [90, 6],
                    [90, 22],
                    [72, 22]
                  ]}
                  pathOptions={{ color: "#6b5a4a", weight: 1, dashArray: "4 4", fillOpacity: 0 }}
                />
              </MapContainer>
            </div>
          </article>

          <article className="card">
            <div className="section-head">
              <div>
                <p className="eyebrow">Operator review</p>
                <h2>Morning briefing draft</h2>
              </div>
            </div>
            <p className="briefing-headline">{investigation.briefing.headline}</p>
            <p className="muted">{investigation.briefing.summary}</p>
            <div className="grid">
              <ListCard title="What happened" items={investigation.briefing.what_happened} />
              <ListCard title="Harmless signals" items={investigation.briefing.harmless_signals} />
              <ListCard title="Escalation items" items={investigation.briefing.escalation_items} />
              <ListCard title="Follow-ups" items={investigation.briefing.follow_ups} />
            </div>
          </article>
        </div>

        <div className="right-column">
          <article className="card">
            <div className="section-head">
              <div>
                <p className="eyebrow">AI layer</p>
                <h2>Investigation controls</h2>
              </div>
            </div>
            <p className="muted">{investigation.agent_summary}</p>
            <label className="stacked-field">
              Operator note
              <textarea value={operatorNote} onChange={(event) => setOperatorNote(event.target.value)} />
            </label>
            <button className="primary-button" onClick={handleInvestigate} disabled={isInvestigating}>
              {isInvestigating ? "Investigating..." : "Re-run investigation"}
            </button>
            {error ? <p className="error-text">{error}</p> : null}
            <p className="muted small">Generated at {formatTime(investigation.generated_at)} UTC.</p>
          </article>

          <article className="card">
            <div className="section-head">
              <div>
                <p className="eyebrow">Tool trace</p>
                <h2>How the agent worked</h2>
              </div>
            </div>
            <div className="stack">
              {investigation.tool_trace.map((trace, index) => (
                <div className="trace-card" key={`${trace.tool}-${index}`}>
                  <div className="trace-top">
                    <strong>{trace.tool}</strong>
                    <span>{trace.source}</span>
                  </div>
                  <p>{trace.reason}</p>
                  <p className="small muted">Input: {trace.input_summary}</p>
                  <p className="small muted">Output: {trace.output_summary}</p>
                </div>
              ))}
            </div>
          </article>

          <article className="card">
            <div className="section-head">
              <div>
                <p className="eyebrow">Findings</p>
                <h2>Escalation review</h2>
              </div>
            </div>
            <div className="stack">
              {investigation.findings.map((finding) => (
                <div className="finding-card" key={finding.id}>
                  <div className="trace-top">
                    <strong>{finding.title}</strong>
                    <span className={`severity ${finding.severity}`}>{finding.severity}</span>
                  </div>
                  <p>{finding.narrative}</p>
                  <p className="small muted">Action: {finding.recommended_action}</p>
                  <p className="small muted">Confidence: {(finding.confidence * 100).toFixed(0)}%</p>
                </div>
              ))}
            </div>
          </article>

          <article className="card">
            <div className="section-head">
              <div>
                <p className="eyebrow">Timeline</p>
                <h2>Overnight signals</h2>
              </div>
            </div>
            <div className="stack">
              {sortedEvents.map((event) => (
                <div className="timeline-card" key={event.id}>
                  <div className="trace-top">
                    <strong>{event.title}</strong>
                    <span className={`severity ${severityClass[event.severity]}`}>{event.severity}</span>
                  </div>
                  <p>{event.detail}</p>
                  <p className="small muted">{formatTime(event.started_at)} UTC</p>
                </div>
              ))}
            </div>
          </article>

          <article className="card">
            <div className="section-head">
              <div>
                <p className="eyebrow">Mission</p>
                <h2>Drone follow-up plan</h2>
              </div>
            </div>
            <p><strong>{investigation.mission.title}</strong></p>
            <p className="muted">{investigation.mission.objective}</p>
            <p className="muted">{investigation.mission.rationale}</p>
            <div className="chips">
              {investigation.mission.route_zone_ids.map((zoneId) => (
                <span key={zoneId}>{context.zones.find((zone) => zone.id === zoneId)?.label ?? zoneId}</span>
              ))}
            </div>
          </article>

          <article className="card">
            <div className="section-head">
              <div>
                <p className="eyebrow">Uncertainty</p>
                <h2>What still needs human judgment</h2>
              </div>
            </div>
            <ul className="uncertainty-list">
              {investigation.uncertainties.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </article>
        </div>
      </section>
    </main>
  );
}

function ListCard({ title, items }: { title: string; items: string[] }) {
  return (
    <article className="list-card">
      <strong>{title}</strong>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </article>
  );
}
