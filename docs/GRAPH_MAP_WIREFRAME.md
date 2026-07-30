# AI Sovereignty Map Wireframe

Status: design exploration only. Do not merge to `main` and do not integrate into mosheuziel.com without explicit approval.

Preview: https://ai-sovereignty-map-wireframe.vercel.app

## Product hypothesis

The public experience should begin as an interactive map rather than a dashboard or analytical system.

A visitor should understand the core idea within seconds:

> Countries may control parts of the AI stack while remaining dependent on shared global chokepoints.

## First interaction

The opening view contains only:

- countries or major ecosystems;
- a small set of global chokepoints;
- the most important relationships between them.

Clicking a country opens a short plain-language conclusion. A second action expands the country into domestic capabilities, locally hosted but foreign-controlled capabilities, and critical external dependencies.

## Wireframe states

1. Global map
2. Israel summary panel
3. Israel expanded capability and dependency map
4. Node detail panel
5. Zoom, pan and reset

## Visual alignment with mosheuziel.com

The wireframe uses the site's existing design language:

- background `#0a0a0a`;
- card background `#111111`;
- border `#27272a`;
- white and zinc typography;
- gold accent `#fbbf24`;
- approximately 1200px content width;
- editorial heading before the interactive element.

## Guardrails

- No sovereignty score.
- No dense matrix as the default view.
- No full graph on first load.
- No system terminology such as `downstream traversal` in the public interface.
- Local presence, ownership and control remain separate concepts.
- Policy targets and announced capacity remain separate from deployed capability.
- The final implementation must load evidence from the validated research dataset.

## Decision needed after review

Determine whether the map is immediately understandable and visually strong enough to become the primary public experience. Only then should it be rebuilt with a graph library and connected to the canonical dataset.