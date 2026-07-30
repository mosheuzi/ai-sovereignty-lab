# Methodology v0.4

## Purpose

AI Sovereignty Lab is not intended to rank countries or prove that full AI sovereignty is possible or impossible. It is intended to expose the capabilities, control relationships, external dependencies and uncertainties that shape national AI resilience.

The method therefore avoids a single opaque sovereignty score. It separates different kinds of control and allows users to inspect the evidence behind each classification.

## Unit of analysis

The primary unit is an **ecosystem capability**, not a company valuation and not a political declaration.

A capability may be:

- A physical asset, such as a data center, fab, power system or cable landing point
- A technology platform, such as a cloud region, accelerator stack or model family
- A national asset, such as language data, procurement power or research talent
- A policy instrument, such as export control, regulation or a government program
- A shared global chokepoint, such as EUV lithography, HBM supply or submarine connectivity

## Thirteen capability layers

Every ecosystem is examined through the same layers:

1. Energy and grid
2. International connectivity
3. Data centers and physical compute
4. Cloud regions and platforms
5. Semiconductor design
6. Semiconductor fabrication and packaging
7. Accelerators and memory
8. Model labs
9. Data and language assets
10. Applications and industrial AI
11. Talent and research
12. Capital and procurement
13. Regulation and export controls

An empty layer is not allowed. A missing capability must be explicitly marked as `absent`, `import_dependent`, `allied_access` or `research_required`.

## Sovereignty dimensions

### 1. Operational control

Can the ecosystem operate, prioritize, configure, monitor and maintain the capability during normal conditions and disruption?

Questions include:

- Who controls day-to-day operation?
- Can national authorities prioritize workloads?
- Can the capability run disconnected from a foreign control plane?
- Are trained personnel and spare parts locally available?
- Can the capability continue without external software updates?

### 2. Legal and governance control

Which legal, contractual and institutional authorities can govern the capability and its data?

Questions include:

- Which jurisdictions apply to the operator and owner?
- Who controls encryption keys, identities and access policy?
- Can a foreign court, regulator or parent company compel action?
- Can the national government audit and enforce the relevant obligations?
- Are data residency and data control being confused?

### 3. Supply-chain control

Can the capability continue when external suppliers, routes, licenses or components become unavailable?

Questions include:

- Which upstream materials, equipment, chips, memory, networking and energy components are required?
- How concentrated is the supply?
- How long would replacement take?
- Is there a domestic substitute, allied substitute or no realistic substitute?
- Do export controls or vendor decisions govern continued access?

### 4. Data and model control

This dimension is displayed separately rather than folded automatically into legal control.

Questions include:

- Who owns or licenses the training, evaluation and operational data?
- Is the data digitized, governed, model-ready and legally usable?
- Can the model be deployed locally or self-hosted?
- Are weights, tokenizer, safety controls and update processes accessible?
- Can the ecosystem evaluate, fine-tune and operate the model independently?

### 5. Resilience

Resilience is not identical to sovereignty. An ecosystem may have low ownership but high resilience through diversified allied access. Another may own a local asset that remains fragile because it depends on a single external supply chain.

The application should therefore show both:

- Control
- Continuity under disruption

## Capability status

Every capability receives one of the following statuses:

- `domestically_owned`
- `domestically_operated_mixed_ownership`
- `foreign_owned_locally_hosted`
- `foreign_owned_locally_operated`
- `allied_access`
- `import_dependent`
- `shared_global`
- `under_development`
- `policy_only`
- `partial`
- `research_required`
- `absent`

Physical presence does not determine sovereignty. A foreign-owned hyperscaler region located inside a country is classified as local infrastructure with foreign ownership and cross-border jurisdiction, not as fully sovereign cloud capacity.

## Claim classes

### Observed

Directly stated by a primary source.

### Observed aggregate

Primary sources support the aggregate relationship, but the map does not assert a specific disclosed agreement for every included company.

### Observed plus inference

The underlying facts are directly sourced and the analytical conclusion is explicitly marked.

### Analytical inference

A research interpretation that is not presented as a disclosed commercial, legal or technical relationship.

### Policy direction

A government decision, strategy or announced objective that does not itself establish operational capability.

## Operational status

The user interface must distinguish:

- Operational
- Contractually committed
- Under construction or deployment
- Announced agreement
- Conditional commitment
- Non-binding letter of intent
- Policy direction
- Research hypothesis

No planned capacity may be rendered with the same visual treatment as operating capacity.

## Evidence hierarchy

Preferred sources, in order:

1. Laws, government decisions and regulator publications
2. Securities filings and audited investor disclosures
3. Intergovernmental organizations and official statistical agencies
4. Official company infrastructure pages and joint announcements
5. Peer-reviewed research and recognized standards bodies
6. High-quality secondary reporting when primary evidence is unavailable

A source is not considered audited merely because its URL appears in the dataset.

## Source audit requirements

Each audited source must record:

- Source ID
- URL
- Publisher
- Publication or last-update date
- Access date
- Whether the URL resolved
- Exact supported claims
- Unsupported or overextended claims
- Source type
- Confidence
- Required dataset action
- Next review date

A page that confirms a product exists does not necessarily prove ownership, corporate nationality, capacity, availability in every zone or strategic independence.

## Numeric claims

Every numeric claim must:

- Reference at least one source
- Use the exact unit and time period in the source
- Distinguish maximum, minimum, approximate and forecast values
- Identify whether the number is operational, planned or conditional
- Avoid adding together incomparable values

Private post-money valuation, public market capitalization, contract value and future compute commitment are separate measures and must never be visually compared as though they represent the same thing.

## Dependency criticality

Criticality should be assessed transparently across five dimensions:

1. Substitutability
2. Supply concentration
3. Replacement time
4. Cross-ecosystem reach
5. Impact of disruption

The current 1-to-5 strategic dependency score is an analytical visualization aid, not an externally published index. The public application should expose the dimensions rather than display only the final number.

## Scenario analysis

A scenario removes or degrades a capability and traces downstream effects.

A scenario result may be:

- Unaffected
- Degraded
- Temporarily unavailable
- Strategically blocked
- Unknown due to missing research

The system must explain the path that produced the result. It must not claim geopolitical prediction.

## Publication gates

A dataset version is eligible for reviewed public release only when:

- Every rendered numeric claim is audited
- Every source URL has been checked
- Every ecosystem has all 13 layers classified
- Planned and operational assets are visually separated
- Foreign-owned local infrastructure is not labeled fully sovereign
- Direct evidence and analytical inference are visually distinct
- Known gaps are published
- Major ecosystems have received domain review
- Automated validation contains no structural errors

## Current interpretation

The project should test a more precise proposition than a binary question:

> Which forms of AI control can a country realistically obtain, which dependencies can it diversify, and which global chokepoints remain outside national control?

This allows the evidence to support conclusions ranging from full dependence, through resilient strategic autonomy, to limited domain-specific sovereignty, without forcing a predetermined answer.