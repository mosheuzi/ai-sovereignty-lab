import rawDataset from "../data/candidates/v0.4-rc2/ai-ecosystem-v0.4-rc2.json";
import type {
  CapabilityStackEntry,
  Ecosystem,
  ImpactedNode,
  ResearchDataset,
  ResearchEdge,
  ResearchNode,
  ResearchSource,
} from "./types";

export const dataset = rawDataset as ResearchDataset;

export const nodesById = new Map<string, ResearchNode>(
  dataset.nodes.map((node) => [node.id, node]),
);

export const sourcesById = new Map<string, ResearchSource>(
  dataset.sources.map((source) => [source.id, source]),
);

export const ecosystemsById = new Map<string, Ecosystem>(
  dataset.ecosystems.map((ecosystem) => [ecosystem.id, ecosystem]),
);

const ignoredImpactCategories = new Set([
  "aggregate_membership",
  "ownership_and_control",
  "aggregate_relationship",
]);

const outgoingEdges = new Map<string, ResearchEdge[]>();
for (const edge of dataset.edges) {
  const current = outgoingEdges.get(edge.from) ?? [];
  current.push(edge);
  outgoingEdges.set(edge.from, current);
}

export function formatIdentifier(value?: string | null): string {
  if (!value) return "Not specified";
  return value
    .replace(/_/g, " ")
    .replace(/\b\w/g, (character: string) => character.toUpperCase());
}

export function ecosystemLabel(ecosystem: Ecosystem | string): string {
  const item = typeof ecosystem === "string" ? ecosystemsById.get(ecosystem) : ecosystem;
  if (!item) return formatIdentifier(String(ecosystem));
  return item.label ?? item.name ?? formatIdentifier(item.id);
}

export function stackNodes(entry?: CapabilityStackEntry): ResearchNode[] {
  if (!entry) return [];
  const ids = [...(entry.node_ids ?? []), ...(entry.allied_access_node_ids ?? [])];
  return ids
    .map((id) => nodesById.get(id))
    .filter((node): node is ResearchNode => Boolean(node));
}

export function sourceRecords(ids?: string[]): ResearchSource[] {
  return (ids ?? [])
    .map((id) => sourcesById.get(id))
    .filter((source): source is ResearchSource => Boolean(source));
}

export function statusTone(status?: string):
  | "domestic"
  | "mixed"
  | "foreign"
  | "dependent"
  | "planned"
  | "research"
  | "neutral" {
  const value = status?.toLowerCase() ?? "";

  if (value.includes("research") || value.includes("unknown")) return "research";
  if (value.includes("import") || value.includes("absent") || value.includes("constrained")) {
    return "dependent";
  }
  if (
    value.includes("under_development") ||
    value.includes("under development") ||
    value.includes("policy") ||
    value.includes("legislative") ||
    value.includes("planned")
  ) {
    return "planned";
  }
  if (value.includes("foreign") || value.includes("allied")) return "foreign";
  if (value.includes("mixed") || value.includes("partial") || value.includes("shared")) {
    return "mixed";
  }
  if (value.includes("domestic") || value.includes("operational")) return "domestic";
  return "neutral";
}

export function computeDownstreamImpact(disruptedNodeIds: string[]): ImpactedNode[] {
  const disrupted = new Set(disruptedNodeIds);
  const visited = new Map<string, ImpactedNode>();
  const queue: Array<{ id: string; depth: number }> = disruptedNodeIds.map((id) => ({
    id,
    depth: 0,
  }));

  while (queue.length > 0) {
    const current = queue.shift();
    if (!current) break;

    for (const edge of outgoingEdges.get(current.id) ?? []) {
      if (ignoredImpactCategories.has(edge.category ?? "")) continue;
      if (disrupted.has(edge.to) || visited.has(edge.to)) continue;

      const node = nodesById.get(edge.to);
      if (!node) continue;

      const impacted: ImpactedNode = {
        node,
        depth: current.depth + 1,
        via: edge,
        parentId: current.id,
      };
      visited.set(edge.to, impacted);
      queue.push({ id: edge.to, depth: current.depth + 1 });
    }
  }

  return [...visited.values()].sort((left, right) => {
    if (left.depth !== right.depth) return left.depth - right.depth;
    return (
      (right.node.strategic_dependency_score ?? 0) -
      (left.node.strategic_dependency_score ?? 0)
    );
  });
}

export const disruptionPresets = [
  "advanced_ai_accelerators",
  "asml",
  "tsmc",
  "sk_hynix",
  "global_subsea_cables",
  "us_export_controls",
].filter((id) => nodesById.has(id));

export const disruptionCandidates = dataset.nodes
  .filter((node) =>
    disruptionPresets.includes(node.id) ||
    (node.strategic_dependency_score ?? 0) >= 4 ||
    node.ecosystem === "Global",
  )
  .sort((left, right) => {
    const scoreDifference =
      (right.strategic_dependency_score ?? 0) -
      (left.strategic_dependency_score ?? 0);
    if (scoreDifference !== 0) return scoreDifference;
    return left.label.localeCompare(right.label);
  });
