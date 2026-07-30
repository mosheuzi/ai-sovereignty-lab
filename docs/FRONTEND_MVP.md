# Front-end MVP

## Goal

Create a front-only interactive research experience that helps users inspect whether national AI sovereignty is possible, partial or structurally dependent on external actors.

The application does not provide a single sovereignty score and does not predict geopolitical outcomes.

## Implemented views

### Capability stack

- Displays the same 13 capability layers for every ecosystem.
- Lets users show or hide ecosystems.
- Distinguishes domestic capability, mixed control, foreign local presence, external dependency, planned capacity and research gaps.
- Opens an evidence drawer for every ecosystem-layer cell.
- Shows linked nodes, control dimensions, limitations and source links.

### Dependency stress test

- Allows users to remove one or more high-dependency nodes.
- Traverses downstream graph edges in the browser.
- Shows direct and cascading exposure by ecosystem and capability layer.
- Preserves the distinction between a structural path and a forecast of actual failure.

## Data source

The MVP imports the validated direct JSON file:

```text
data/candidates/v0.4-rc2/ai-ecosystem-v0.4-rc2.json
```

No backend, database, account or analytics service is required.

## Technology

- Vite
- React
- TypeScript
- Static JSON
- CSS without a component framework
- GitHub Actions build validation
- Vercel-compatible static output

## Local development

```bash
npm install
npm run dev
```

Production validation:

```bash
npm run build
```

## Current limitations

- The dependency simulation follows documented directed edges and does not model substitution time, probability or capacity buffers.
- The graph does not yet provide a visual node-link canvas.
- Research completeness differs between ecosystems.
- The application is an English-language prototype.
- The project remains a research draft and is not ready for authoritative citation.

## Next product steps

1. Review the first interaction model with policy and infrastructure users.
2. Add a node-link dependency map only where it improves comprehension.
3. Add user-selected weights for operational, legal and supply-chain control without introducing an opaque default score.
4. Add shareable scenario URLs.
5. Add a compact mobile comparison mode.
6. Deploy a private Vercel preview.
