# AI Sovereignty Lab

An open, source-backed interactive research project for exploring a difficult question:

> Can a country achieve sovereign AI, or is every national AI capability necessarily dependent on foreign infrastructure, supply chains, companies and jurisdictions?

This project does not begin with a predetermined answer. It provides a transparent dataset and, in the next phase, an interactive front-end that allows users to inspect the evidence, compare ecosystems and test dependency scenarios.

## Current status

**Public research draft. Not ready for authoritative citation.**

The repository currently contains the research dataset, source catalogue, methodology and product plan. The interactive application has not yet been implemented.

Structural validation means that references, node identifiers and capability layers are internally consistent. It does **not** mean that the research is complete or that every factual claim has received final editorial review.

## Research model

The dataset separates:

- Physical location
- Ownership and corporate control
- Operational control
- Legal and governance jurisdiction
- Supply-chain control
- Operational capacity
- Announced or planned capacity
- Directly observed claims
- Analytical inferences

Company valuation is excluded from node sizing. Strategic importance is modeled through dependency, substitutability, concentration and disruption impact.

## National capability stack

Each ecosystem is assessed against the same 13 layers:

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

A capability located inside a country is not automatically considered sovereign. For example, a foreign-owned cloud region physically located in a country is classified separately from domestically owned infrastructure.

## Repository structure

```text
data/
  manifest.json
  config.json
  sources.json
  audit.json
  validation-report-v0.3.json
  canonical/
    ai-ecosystem-v0.3.json.gz.b64.part-01
    ai-ecosystem-v0.3.json.gz.b64.part-02
    ai-ecosystem-v0.3.json.gz.b64.part-03
    ai-ecosystem-v0.3.json.gz.b64.part-04
  ecosystems/
    us.json
    israel.json

docs/
  RESEARCH_PLAN.md
  PRODUCT_PLAN.md
  EXECUTION_PLAN.md
  DATA_MODEL.md
  SOURCES.md

schema/
  ai-ecosystem.schema.json

CONTRIBUTING.md
LICENSE
DATA_LICENSE.md
```

## Data snapshot

- Dataset version: `0.3-capability-stacks`
- Ecosystems: `7`
- Capability layers: `13`
- Nodes: `52`
- Edges: `60`
- Sources: `52`

## Loading the canonical dataset

The complete research dataset is stored as a deterministic gzip archive, encoded as base64 and split into four text files. The manifest contains the ordered list and the SHA-256 checksum of the gzip payload.

A future browser client can load it without a backend:

```js
const manifest = await fetch('/data/manifest.json').then((response) => response.json());

const chunks = await Promise.all(
  manifest.canonical_dataset.parts.map((path) =>
    fetch(`/data/${path}`).then((response) => response.text())
  )
);

const base64 = chunks.join('').replace(/\s/g, '');
const compressed = Uint8Array.from(atob(base64), (character) => character.charCodeAt(0));
const stream = new Blob([compressed])
  .stream()
  .pipeThrough(new DecompressionStream('gzip'));

const dataset = await new Response(stream).json();
```

The expanded ecosystem files are currently partial and intended to become a contribution-friendly representation of the canonical data during the implementation phase.

## Source policy

The project prioritizes:

1. Government and regulator publications
2. Securities filings and investor disclosures
3. Intergovernmental organizations
4. Official company announcements and technical documentation
5. Secondary sources only when primary evidence is unavailable

Every numeric claim should reference a source. Future commitments must be visually separated from operational capacity. Analytical inferences must never be presented as disclosed agreements.

The full source catalogue is available in [`docs/SOURCES.md`](docs/SOURCES.md) and [`data/sources.json`](data/sources.json).

Representative primary sources include:

- International Energy Agency, *Energy and AI*
- International Telecommunication Union, submarine cable resilience publications
- U.S. Geological Survey, *Mineral Commodity Summaries*
- U.S. Department of Energy, data-center electricity demand
- European Commission, AI Factories and the EU AI Act
- Government of Israel, Government Decision 4255 and Nimbus publications
- Official infrastructure and financing disclosures from ASML, TSMC, Intel, Micron, NVIDIA, AWS, Google Cloud, Microsoft, OpenAI, Anthropic, AI21 and Cerebras

## Planned interactive experience

The first MVP will be front-end only. Users will be able to:

- Compare national capability stacks
- Switch between operational, planned and policy-only capabilities
- Inspect every node and edge with its supporting source
- Distinguish domestic ownership from foreign-owned local infrastructure
- Hide a supplier, country or technology and observe which capability paths break
- Explore operational, legal and supply-chain sovereignty separately
- Reach their own conclusion rather than receiving a single opaque sovereignty score

## Work phases

### Research

Audit the sources, refine the definitions, complete the capability stacks and produce evidence-backed disruption scenarios.

### Planning

Design the information architecture, visual language, graph interactions, comparison flow and website integration.

### Execution

Build a static React and TypeScript front-end, validate the dataset in CI, publish it on Vercel and integrate it into `mosheuziel.com/labs/ai-sovereignty`.

See the detailed plans in the [`docs`](docs/) directory.

## Project principle

> No country should be presented as fully sovereign merely because infrastructure is physically located within its borders.

## Author

Initiated by Moshe Uziel as a public research and knowledge-sharing project about national AI capability, infrastructure dependencies and AI sovereignty.
