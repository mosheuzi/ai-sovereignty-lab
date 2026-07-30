# Data Model

## Main entities

### Ecosystem

Represents a country, regional bloc or strategic ecosystem.

Required analytical fields:

- Capability stack
- Strengths
- External dependencies
- Research completeness
- Known gaps

### Node

Represents a capability, company, physical infrastructure asset, policy instrument or shared global chokepoint.

Important fields:

- `id`
- `label`
- `ecosystem`
- `capability_layer`
- `capability_status`
- `physical_locations`
- `operator`
- `ownership_countries`
- `jurisdictions`
- `national_control_class`
- `control_profile`
- `status`
- `source_ids`

### Edge

Represents a dependency, ownership relationship, supply relationship, policy influence or analytical inference.

Important fields:

- `from`
- `to`
- `category`
- `status`
- `claim_class`
- `confidence`
- `source_ids`
- `criticality`
- `substitutability`

### Source

Represents the evidence supporting a node, metric or edge.

Important fields:

- Publisher
- Title
- Date
- URL
- Source type
- Verification status
- Exact evidence or supported claim

## Three sovereignty dimensions

### Operational control

Can the ecosystem operate, prioritize, configure and maintain the capability?

### Legal and governance control

Which laws, contractual controls and governance bodies apply?

### Supply-chain control

Can the capability continue to operate if foreign suppliers, updates, components or export permissions are unavailable?

## Status distinction

The UI must visibly separate:

- Operational
- Under development
- Announced
- Committed
- Conditional
- Policy direction
- Analytical inference

## Contribution principle

A contributor should never add a number without a source, or add a source without specifying the exact claim it supports.
