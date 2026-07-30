import { useMemo, useState } from "react";
import {
  computeDownstreamImpact,
  dataset,
  disruptionCandidates,
  disruptionPresets,
  ecosystemLabel,
  formatIdentifier,
  nodesById,
  sourceRecords,
  stackNodes,
  statusTone,
} from "./data";
import type {
  CapabilityStackEntry,
  Ecosystem,
  ImpactedNode,
  ResearchNode,
  ResearchSource,
} from "./types";

const layerDescriptions: Record<string, string> = {
  energy_and_grid: "Electricity generation, transmission and grid connection for AI infrastructure.",
  international_connectivity: "Subsea cables, terrestrial networks and cross-border connectivity.",
  data_centers_physical_compute: "Physical facilities, servers, cooling and operational compute capacity.",
  cloud_regions_platforms: "Cloud regions, control planes and managed infrastructure platforms.",
  semiconductor_design: "Domestic or locally operated chip architecture and design capability.",
  semiconductor_fabrication_packaging: "Foundries, process technology, packaging and manufacturing equipment.",
  accelerators_memory: "AI accelerators, HBM and the memory systems required for advanced compute.",
  model_labs: "Organizations able to develop, train, adapt or privately deploy foundation models.",
  data_language_assets: "Governed, licensed and model-ready national, language and sector data.",
  applications_industrial_ai: "The ability to translate infrastructure and models into useful products and systems.",
  talent_research: "Researchers, engineers, universities and corporate R&D capabilities.",
  capital_procurement: "Public and private capital, procurement mechanisms and demand aggregation.",
  regulation_export_controls: "Laws, planning rules, export controls and national governance instruments.",
};

const toneLabels = {
  domestic: "Domestic or operational",
  mixed: "Partial or mixed control",
  foreign: "Foreign or allied access",
  dependent: "Constrained or import-dependent",
  planned: "Planned or policy-stage",
  research: "Research gap",
  neutral: "Other",
};

type View = "stack" | "scenario";

interface SelectedCell {
  ecosystemId: string;
  layerId: string;
}

function uniqueSources(nodes: ResearchNode[]): ResearchSource[] {
  const ids = new Set(nodes.flatMap((node) => node.source_ids ?? []));
  return sourceRecords([...ids]);
}

function Metric({ value, label }: { value: string | number; label: string }) {
  return (
    <div className="metric">
      <strong>{value}</strong>
      <span>{label}</span>
    </div>
  );
}

function StatusBadge({ status }: { status?: string }) {
  const tone = statusTone(status);
  return (
    <span className={`status-badge status-${tone}`} title={toneLabels[tone]}>
      {formatIdentifier(status)}
    </span>
  );
}

function SourceList({ sources }: { sources: ResearchSource[] }) {
  if (sources.length === 0) {
    return <p className="muted small">No source record is attached to this selection.</p>;
  }

  return (
    <div className="source-list">
      {sources.map((source) => (
        <article className="source-card" key={source.id}>
          <div>
            <p className="source-publisher">{source.publisher ?? "Unknown publisher"}</p>
            <h4>{source.title ?? formatIdentifier(source.id)}</h4>
          </div>
          <div className="source-meta">
            <span>{source.date ?? "Date unavailable"}</span>
            <span>{formatIdentifier(source.verification_status ?? source.source_type)}</span>
          </div>
          {source.evidence ? <p>{source.evidence}</p> : null}
          {source.url ? (
            <a href={source.url} target="_blank" rel="noreferrer">
              Open primary source <span aria-hidden="true">↗</span>
            </a>
          ) : null}
        </article>
      ))}
    </div>
  );
}

function ControlProfile({ node }: { node: ResearchNode }) {
  const profile = node.control_profile;
  if (!profile) return null;

  const dimensions = [
    ["Operational", profile.operational_control],
    ["Legal & governance", profile.legal_governance_control],
    ["Supply chain", profile.supply_chain_control],
  ];

  return (
    <div className="control-grid">
      {dimensions.map(([label, value]) => (
        <div key={label}>
          <span>{label}</span>
          <strong>{formatIdentifier(value)}</strong>
        </div>
      ))}
    </div>
  );
}

function NodeCard({ node }: { node: ResearchNode }) {
  const sources = sourceRecords(node.source_ids);
  const ownership = node.verified_control_country
    ? `Verified control: ${node.verified_control_country}`
    : node.ownership_verification_status
      ? formatIdentifier(node.ownership_verification_status)
      : formatIdentifier(node.national_control_class);

  return (
    <article className="node-card">
      <div className="node-card-heading">
        <div>
          <p className="eyebrow">{formatIdentifier(node.type)}</p>
          <h3>{node.label}</h3>
        </div>
        <StatusBadge status={node.capability_status ?? node.status} />
      </div>

      <dl className="node-facts">
        <div>
          <dt>Operator</dt>
          <dd>{node.operator ?? "Not specified"}</dd>
        </div>
        <div>
          <dt>Location</dt>
          <dd>{node.physical_locations?.join(", ") ?? node.country ?? "Not specified"}</dd>
        </div>
        <div>
          <dt>Ownership or control</dt>
          <dd>{ownership}</dd>
        </div>
      </dl>

      <ControlProfile node={node} />

      {node.capabilities?.length ? (
        <div className="tag-list" aria-label="Capabilities">
          {node.capabilities.slice(0, 8).map((capability) => (
            <span key={capability}>{capability}</span>
          ))}
        </div>
      ) : null}

      {node.limitations?.length ? (
        <details>
          <summary>Limitations and caveats</summary>
          <ul>
            {node.limitations.map((limitation) => (
              <li key={limitation}>{limitation}</li>
            ))}
          </ul>
        </details>
      ) : null}

      {sources.length ? (
        <div className="node-source-links">
          {sources.slice(0, 3).map((source) => (
            <a href={source.url} target="_blank" rel="noreferrer" key={source.id}>
              {source.publisher ?? source.id} ↗
            </a>
          ))}
        </div>
      ) : null}
    </article>
  );
}

function EvidenceDrawer({
  selected,
  onClose,
}: {
  selected: SelectedCell | null;
  onClose: () => void;
}) {
  if (!selected) return null;

  const ecosystem = dataset.ecosystems.find((item) => item.id === selected.ecosystemId);
  const layer = dataset.capability_schema.layers.find((item) => item.id === selected.layerId);
  const entry = ecosystem?.capability_stack[selected.layerId];
  const nodes = stackNodes(entry);
  const sources = uniqueSources(nodes);

  return (
    <>
      <button className="drawer-backdrop" aria-label="Close evidence panel" onClick={onClose} />
      <aside className="evidence-drawer" aria-label="Evidence panel">
        <div className="drawer-header">
          <div>
            <p className="eyebrow">Evidence and limitations</p>
            <h2>{ecosystem ? ecosystemLabel(ecosystem) : selected.ecosystemId}</h2>
            <p>{layer?.label ?? formatIdentifier(selected.layerId)}</p>
          </div>
          <button className="icon-button" onClick={onClose} aria-label="Close evidence panel">
            ×
          </button>
        </div>

        <div className="drawer-content">
          <section className="drawer-summary">
            <StatusBadge status={entry?.status} />
            <p>{layerDescriptions[selected.layerId]}</p>
            {entry?.gap ? (
              <div className="research-note">
                <strong>Known gap</strong>
                <p>{entry.gap}</p>
              </div>
            ) : null}
            {entry?.external_dependencies?.length ? (
              <div>
                <h3>External dependencies</h3>
                <div className="tag-list">
                  {entry.external_dependencies.map((dependency) => (
                    <span key={dependency}>{dependency}</span>
                  ))}
                </div>
              </div>
            ) : null}
          </section>

          <section>
            <div className="section-heading compact">
              <div>
                <p className="eyebrow">Capabilities in this layer</p>
                <h2>{nodes.length} linked node{nodes.length === 1 ? "" : "s"}</h2>
              </div>
            </div>
            {nodes.length ? (
              <div className="node-list">
                {nodes.map((node) => (
                  <NodeCard key={node.id} node={node} />
                ))}
              </div>
            ) : (
              <div className="empty-state">
                <h3>No linked operational node</h3>
                <p>
                  This may represent a genuine capability gap, an import dependency or an area where
                  research is still incomplete.
                </p>
              </div>
            )}
          </section>

          <section>
            <div className="section-heading compact">
              <div>
                <p className="eyebrow">Source ledger</p>
                <h2>{sources.length} supporting source{sources.length === 1 ? "" : "s"}</h2>
              </div>
            </div>
            <SourceList sources={sources} />
          </section>
        </div>
      </aside>
    </>
  );
}

function CapabilityStack({ onSelect }: { onSelect: (selection: SelectedCell) => void }) {
  const [query, setQuery] = useState("");
  const [selectedEcosystems, setSelectedEcosystems] = useState<string[]>(
    dataset.ecosystems.map((ecosystem) => ecosystem.id),
  );

  const visibleLayers = dataset.capability_schema.layers.filter((layer) => {
    const haystack = `${layer.label} ${layerDescriptions[layer.id] ?? ""}`.toLowerCase();
    return haystack.includes(query.toLowerCase());
  });

  const visibleEcosystems = dataset.ecosystems.filter((ecosystem) =>
    selectedEcosystems.includes(ecosystem.id),
  );

  const toggleEcosystem = (id: string) => {
    setSelectedEcosystems((current) => {
      if (current.includes(id)) {
        if (current.length === 1) return current;
        return current.filter((item) => item !== id);
      }
      return [...current, id];
    });
  };

  return (
    <section className="workspace" aria-labelledby="stack-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">National capability stack</p>
          <h2 id="stack-title">What exists locally, and who actually controls it?</h2>
          <p>
            Each cell separates domestic capability, foreign-owned local presence, external access,
            planned capacity and unresolved research.
          </p>
        </div>
        <label className="search-field">
          <span>Find a layer</span>
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Energy, models, chips..."
          />
        </label>
      </div>

      <div className="ecosystem-filter" aria-label="Visible ecosystems">
        {dataset.ecosystems.map((ecosystem) => (
          <button
            key={ecosystem.id}
            className={selectedEcosystems.includes(ecosystem.id) ? "selected" : ""}
            onClick={() => toggleEcosystem(ecosystem.id)}
          >
            {ecosystemLabel(ecosystem)}
          </button>
        ))}
      </div>

      <div className="legend" aria-label="Status legend">
        {Object.entries(toneLabels).map(([tone, label]) => (
          <span key={tone}>
            <i className={`legend-dot status-${tone}`} />
            {label}
          </span>
        ))}
      </div>

      <div className="matrix-shell">
        <table className="capability-matrix">
          <thead>
            <tr>
              <th className="layer-column">Capability layer</th>
              {visibleEcosystems.map((ecosystem) => (
                <th key={ecosystem.id}>
                  <span>{ecosystemLabel(ecosystem)}</span>
                  <small>
                    {Math.round((ecosystem.research_completeness_score ?? 0) * 100)}% researched
                  </small>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {visibleLayers.map((layer, index) => (
              <tr key={layer.id}>
                <th className="layer-column">
                  <span className="layer-index">{String(index + 1).padStart(2, "0")}</span>
                  <div>
                    <strong>{layer.label}</strong>
                    <small>{layerDescriptions[layer.id]}</small>
                  </div>
                </th>
                {visibleEcosystems.map((ecosystem) => {
                  const entry = ecosystem.capability_stack[layer.id];
                  const nodes = stackNodes(entry);
                  const tone = statusTone(entry?.status);
                  return (
                    <td key={`${ecosystem.id}-${layer.id}`}>
                      <button
                        className={`matrix-cell status-${tone}`}
                        onClick={() =>
                          onSelect({ ecosystemId: ecosystem.id, layerId: layer.id })
                        }
                      >
                        <span>{formatIdentifier(entry?.status)}</span>
                        <small>
                          {nodes.length} node{nodes.length === 1 ? "" : "s"}
                          {entry?.external_dependencies?.length
                            ? ` · ${entry.external_dependencies.length} external`
                            : ""}
                        </small>
                      </button>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function ImpactSummary({ impacted }: { impacted: ImpactedNode[] }) {
  const byEcosystem = useMemo(() => {
    const counts = new Map<string, number>();
    for (const item of impacted) {
      const key = item.node.ecosystem ?? "Global";
      counts.set(key, (counts.get(key) ?? 0) + 1);
    }
    return [...counts.entries()].sort((left, right) => right[1] - left[1]);
  }, [impacted]);

  const byLayer = useMemo(() => {
    const counts = new Map<string, number>();
    for (const item of impacted) {
      const key = item.node.capability_layer ?? item.node.layer ?? "unclassified";
      counts.set(key, (counts.get(key) ?? 0) + 1);
    }
    return [...counts.entries()].sort((left, right) => right[1] - left[1]);
  }, [impacted]);

  if (!impacted.length) {
    return (
      <div className="empty-state large">
        <h3>No downstream impact is visible yet</h3>
        <p>
          Select one or more dependencies. The lab will traverse documented downstream edges and
          show the capabilities that become exposed.
        </p>
      </div>
    );
  }

  return (
    <div className="impact-layout">
      <div className="impact-summary-card">
        <p className="eyebrow">Structural exposure</p>
        <strong className="impact-number">{impacted.length}</strong>
        <p>downstream nodes connected through documented dependency paths</p>

        <h3>Affected ecosystems</h3>
        <div className="bar-list">
          {byEcosystem.slice(0, 8).map(([id, count]) => (
            <div key={id}>
              <span>{ecosystemLabel(id)}</span>
              <strong>{count}</strong>
            </div>
          ))}
        </div>

        <h3>Affected capability layers</h3>
        <div className="tag-list">
          {byLayer.slice(0, 8).map(([layer, count]) => (
            <span key={layer}>
              {formatIdentifier(layer)} · {count}
            </span>
          ))}
        </div>
      </div>

      <div className="impact-list">
        {impacted.slice(0, 30).map((item) => {
          const parent = item.parentId ? nodesById.get(item.parentId) : undefined;
          return (
            <article key={item.node.id}>
              <div>
                <span className="depth-badge">
                  {item.depth === 1 ? "Direct" : `Cascade ${item.depth}`}
                </span>
                <h3>{item.node.label}</h3>
                <p>
                  {ecosystemLabel(item.node.ecosystem ?? "Global")} ·{" "}
                  {formatIdentifier(item.node.capability_layer ?? item.node.layer)}
                </p>
              </div>
              <div className="impact-path">
                <span>{parent?.label ?? item.parentId}</span>
                <i aria-hidden="true">→</i>
                <span>{item.via?.label ?? formatIdentifier(item.via?.category)}</span>
              </div>
            </article>
          );
        })}
      </div>
    </div>
  );
}

function ScenarioExplorer() {
  const [selected, setSelected] = useState<string[]>([]);
  const [query, setQuery] = useState("");

  const impacted = useMemo(() => computeDownstreamImpact(selected), [selected]);
  const candidates = disruptionCandidates.filter((node) => {
    const haystack = `${node.label} ${node.ecosystem ?? ""} ${node.type ?? ""}`.toLowerCase();
    return haystack.includes(query.toLowerCase());
  });

  const toggle = (id: string) => {
    setSelected((current) =>
      current.includes(id) ? current.filter((item) => item !== id) : [...current, id],
    );
  };

  return (
    <section className="workspace scenario-workspace" aria-labelledby="scenario-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Dependency stress test</p>
          <h2 id="scenario-title">Remove a dependency and follow the cascade</h2>
          <p>
            This is graph traversal over documented relationships, not a geopolitical forecast. It
            shows where the current evidence model contains a downstream path.
          </p>
        </div>
        <button className="secondary-button" onClick={() => setSelected([])} disabled={!selected.length}>
          Reset scenario
        </button>
      </div>

      <div className="scenario-grid">
        <aside className="scenario-controls">
          <div>
            <p className="eyebrow">Suggested disruptions</p>
            <div className="preset-list">
              {disruptionPresets.map((id) => {
                const node = nodesById.get(id);
                if (!node) return null;
                return (
                  <button
                    className={selected.includes(id) ? "selected" : ""}
                    key={id}
                    onClick={() => toggle(id)}
                  >
                    <span>{node.label}</span>
                    <small>{formatIdentifier(node.type)}</small>
                  </button>
                );
              })}
            </div>
          </div>

          <label className="search-field full-width">
            <span>Search high-dependency nodes</span>
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="TSMC, energy, cloud..."
            />
          </label>

          <div className="candidate-list">
            {candidates.slice(0, 18).map((node) => (
              <label key={node.id}>
                <input
                  type="checkbox"
                  checked={selected.includes(node.id)}
                  onChange={() => toggle(node.id)}
                />
                <span>
                  <strong>{node.label}</strong>
                  <small>
                    {ecosystemLabel(node.ecosystem ?? "Global")} · score {node.strategic_dependency_score ?? "n/a"}
                  </small>
                </span>
              </label>
            ))}
          </div>
        </aside>

        <div className="scenario-results">
          {selected.length ? (
            <div className="active-scenario">
              <strong>Removed from scenario</strong>
              <div className="tag-list removable-tags">
                {selected.map((id) => (
                  <button key={id} onClick={() => toggle(id)}>
                    {nodesById.get(id)?.label ?? id} ×
                  </button>
                ))}
              </div>
            </div>
          ) : null}
          <ImpactSummary impacted={impacted} />
        </div>
      </div>
    </section>
  );
}

function App() {
  const [view, setView] = useState<View>("stack");
  const [selectedCell, setSelectedCell] = useState<SelectedCell | null>(null);

  return (
    <div className="app-shell">
      <header className="site-header">
        <a className="brand" href="#top" aria-label="AI Sovereignty Lab home">
          <span className="brand-mark">AI</span>
          <span>
            <strong>Sovereignty Lab</strong>
            <small>Open research prototype</small>
          </span>
        </a>
        <a
          className="github-link"
          href="https://github.com/mosheuzi/ai-sovereignty-lab"
          target="_blank"
          rel="noreferrer"
        >
          View research on GitHub ↗
        </a>
      </header>

      <main id="top">
        <section className="hero">
          <div className="hero-copy">
            <p className="eyebrow">An evidence-backed question, not a predetermined answer</p>
            <h1>Can artificial intelligence ever be truly sovereign?</h1>
            <p className="hero-lede">
              Explore national AI capability stacks, distinguish local presence from real control,
              and test what happens when a critical supplier, technology or infrastructure layer is
              removed.
            </p>
            <div className="hero-actions">
              <button className="primary-button" onClick={() => setView("stack")}>
                Compare capability stacks
              </button>
              <button className="secondary-button" onClick={() => setView("scenario")}>
                Run a dependency scenario
              </button>
            </div>
          </div>

          <div className="hero-panel">
            <div className="metrics-grid">
              <Metric value={dataset.ecosystems.length} label="ecosystems" />
              <Metric value={dataset.capability_schema.layers.length} label="capability layers" />
              <Metric value={dataset.nodes.length} label="capability nodes" />
              <Metric value={dataset.sources.length} label="research sources" />
            </div>
            <div className="version-note">
              <span>Dataset {dataset.metadata.version}</span>
              <span>Audited through {dataset.metadata.audited_as_of ?? dataset.metadata.as_of}</span>
            </div>
          </div>
        </section>

        <section className="principle-strip" aria-label="Research principles">
          <div>
            <strong>Local is not automatically sovereign.</strong>
            <span>Physical location, ownership, operation and supply-chain control are separate.</span>
          </div>
          <div>
            <strong>Plans are not deployed capacity.</strong>
            <span>Policy targets and announced infrastructure remain visibly distinct.</span>
          </div>
          <div>
            <strong>Every claim should be inspectable.</strong>
            <span>Open a cell to see nodes, limitations and source links.</span>
          </div>
        </section>

        <nav className="view-tabs" aria-label="Research views">
          <button className={view === "stack" ? "active" : ""} onClick={() => setView("stack")}>
            <span>01</span>
            Capability stack
          </button>
          <button
            className={view === "scenario" ? "active" : ""}
            onClick={() => setView("scenario")}
          >
            <span>02</span>
            Dependency stress test
          </button>
        </nav>

        {view === "stack" ? <CapabilityStack onSelect={setSelectedCell} /> : <ScenarioExplorer />}

        <section className="methodology-callout">
          <div>
            <p className="eyebrow">How to read the lab</p>
            <h2>There is no single sovereignty score.</h2>
          </div>
          <p>
            A country may operate a capability without owning it, govern data without controlling
            the underlying supply chain, or possess strong research talent while depending on foreign
            accelerators and cloud control planes. The lab exposes those dimensions rather than hiding
            them inside one number.
          </p>
        </section>
      </main>

      <footer>
        <div>
          <strong>AI Sovereignty Lab</strong>
          <p>Research draft initiated by Moshe Uziel. Contributions should be evidence-backed.</p>
        </div>
        <div>
          <a href="https://github.com/mosheuzi/ai-sovereignty-lab" target="_blank" rel="noreferrer">
            GitHub repository ↗
          </a>
          <a
            href="https://github.com/mosheuzi/ai-sovereignty-lab/blob/main/CONTRIBUTING.md"
            target="_blank"
            rel="noreferrer"
          >
            Contribution guide ↗
          </a>
        </div>
      </footer>

      <EvidenceDrawer selected={selectedCell} onClose={() => setSelectedCell(null)} />
    </div>
  );
}

export default App;
