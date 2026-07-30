# v0.4 Sprint 1 Findings

## What changed in the research approach

The project now distinguishes three separate questions for every capability:

1. Is the capability physically present?
2. Who owns, governs and operates it?
3. Can it continue when foreign supply, control planes, licenses or components are unavailable?

This prevents local data residency, a foreign-owned fab or a local corporate research lab from being treated as equivalent to full national sovereignty.

## Israel findings

### Cloud

Israel has substantial local hyperscaler infrastructure, but the evidence supports a classification of foreign-owned local presence rather than fully domestic cloud sovereignty.

- AWS Israel is open with three Availability Zones and local data storage.
- Google Cloud me-west1 is open in Tel Aviv and contains three documented zones.
- Azure Israel Central supports Availability Zones, but the reviewed source does not establish a precise zone count.
- Nimbus provides government procurement, policy, FinOps, CCoE and marketplace capabilities through AWS and Google.

### Models

AI21 establishes a genuine Israel-based model capability. Jamba models can be downloaded and self-hosted. This improves deployment and model control, but does not eliminate accelerator, component or maintenance dependencies.

A separate source is still required before the dataset makes a strict claim about domestic corporate ownership.

### Semiconductors and research

Intel Israel provides local manufacturing and processor, communications and AI development. NVIDIA operates an AI research lab in Tel Aviv. These are important local capabilities, but both remain within foreign corporate structures.

### National policy

The current official URL for Government Decision 4255 did not resolve in the audit process. A Knesset publication corroborates the existence and broad direction of the decision, but the full official text is still required before detailed claims are considered audited.

### Energy

The current 74 percent natural-gas electricity metric has not yet passed the line-level source audit. It remains a candidate claim rather than an approved v0.4 metric.

## Design consequence

The MVP should not ask only whether a capability exists. Every rendered capability should reveal:

- Location
- Operator
- Ownership
- Jurisdiction
- Operational status
- External supply dependencies
- Evidence

## Current working hypothesis

The evidence increasingly suggests that a country can build meaningful operational and legal control in selected layers, but complete supply-chain independence is a much stronger and less realistic requirement.

This remains a hypothesis for the interactive system to test, not the predetermined conclusion of the project.