# Product Plan

## Product goal

Build a simple, front-end-only analytical experience that enables users to inspect AI capability stacks and test dependency scenarios themselves.

The product should feel like an interactive research article, not a commercial dashboard.

## Primary audience

- Government AI leaders
- Public-policy professionals
- Enterprise technology leaders
- AI infrastructure practitioners
- Researchers and students
- Open-source contributors

## Core user journey

1. Read the research question
2. Select a country or ecosystem
3. Inspect its capability stack
4. Distinguish domestic, local-foreign and external capabilities
5. Open a node to view evidence and limitations
6. Compare it with another ecosystem
7. Remove or restrict a dependency
8. Observe which capability paths are degraded
9. Form a personal conclusion about the realistic level of AI sovereignty

## MVP views

### 1. Capability Stack

A matrix with ecosystems as columns and capability layers as rows.

Cell states:

- Domestic capability
- Mixed ownership
- Foreign-owned local presence
- Allied access
- Import-dependent
- Planned
- Missing research

### 2. Dependency Map

A network view connecting:

- Energy
- Connectivity
- Materials
- Equipment
- Fabrication
- Memory
- Accelerators
- Data centers
- Cloud
- Models
- Data
- Applications
- State policy

### 3. Sovereignty Gap

For a selected ecosystem, show:

- Capabilities under domestic control
- Capabilities physically local but externally controlled
- Capabilities accessed through allies or vendors
- Capabilities with no credible domestic substitute

### 4. Scenario Explorer

The user can disable:

- A country
- A company
- A technology
- An infrastructure layer
- A regulatory access path

The system highlights broken and degraded dependency paths.

### 5. Evidence Panel

Every node and edge should expose:

- Claim
- Source
- Date
- Status
- Confidence
- Limitation
- Direct observation versus analysis

## What the MVP should not do

- Produce a black-box sovereignty score
- Predict geopolitical events
- Present company announcements as completed capacity
- Imply that physical data residency equals sovereignty
- Require login
- Store user data
- Use a backend database
- Become a generic commercial analytics platform

## Proposed technology

- Vite
- React
- TypeScript
- Cytoscape.js for dependency graphs
- A lightweight table or grid component for capability stacks
- Zod or JSON Schema validation at build time
- Static JSON in the repository
- Vercel for preview and production hosting
- GitHub Actions for validation and build checks

## Website integration

Recommended structure:

- The open-source application remains in its own repository and deployment.
- Moshe's website contains a server-rendered page at `/labs/ai-sovereignty`.
- The page explains the research question, methodology and contribution model.
- The interactive app is embedded below in a full-width iframe or mounted as a separately deployed application.
- A visible button links to the public GitHub repository.
- The page contains indexable explanatory text even if the application itself is client-rendered.

This preserves separation between the personal website and the open-source project while providing a coherent user experience.
