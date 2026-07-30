export interface CapabilityLayer {
  id: string;
  label: string;
  description?: string;
}

export interface ControlProfile {
  operational_control?: string;
  legal_governance_control?: string;
  supply_chain_control?: string;
}

export interface ResearchSource {
  id: string;
  publisher?: string;
  title?: string;
  date?: string;
  url?: string;
  source_type?: string;
  verification_status?: string;
  evidence?: string;
}

export interface ResearchNode {
  id: string;
  label: string;
  ecosystem?: string;
  country?: string;
  capability_layer?: string;
  layer?: string;
  type?: string;
  capability_status?: string;
  national_control_class?: string;
  status?: string;
  strategic_dependency_score?: number;
  source_ids?: string[];
  physical_locations?: string[];
  ownership_countries?: string[];
  jurisdictions?: string[];
  operator?: string;
  company_origin_country?: string | null;
  headquarters_country?: string | null;
  verified_control_country?: string | null;
  ownership_verification_status?: string;
  control_profile?: ControlProfile;
  capabilities?: string[];
  limitations?: string[];
  notes?: string | string[];
  metrics?: Array<Record<string, unknown>>;
  [key: string]: unknown;
}

export interface ResearchEdge {
  id: string;
  from: string;
  to: string;
  category?: string;
  label?: string;
  status?: string;
  claim_class?: string;
  confidence?: string;
  source_ids?: string[];
  criticality?: number;
  substitutability?: string;
  [key: string]: unknown;
}

export interface CapabilityStackEntry {
  status: string;
  node_ids?: string[];
  allied_access_node_ids?: string[];
  external_dependencies?: string[];
  gap?: string | null;
  confidence?: string;
  [key: string]: unknown;
}

export interface Ecosystem {
  id: string;
  label?: string;
  name?: string;
  capability_stack: Record<string, CapabilityStackEntry>;
  research_completeness_score?: number;
  capability_presence_score_unweighted?: number;
  [key: string]: unknown;
}

export interface ResearchDataset {
  metadata: {
    title?: string;
    version?: string;
    as_of?: string;
    audited_as_of?: string;
    purpose?: string;
    [key: string]: unknown;
  };
  capability_schema: {
    layers: CapabilityLayer[];
    [key: string]: unknown;
  };
  ecosystems: Ecosystem[];
  nodes: ResearchNode[];
  edges: ResearchEdge[];
  sources: ResearchSource[];
  validation_rules?: string[];
  [key: string]: unknown;
}

export interface ImpactedNode {
  node: ResearchNode;
  depth: number;
  via?: ResearchEdge;
  parentId?: string;
}
