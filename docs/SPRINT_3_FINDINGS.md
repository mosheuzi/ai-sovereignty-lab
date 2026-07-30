# Sprint 3 Findings

## Scope

This sprint focused on the remaining Israel-specific questions that most directly affect the sovereignty model:

- Tower Semiconductor and domestic fabrication
- Large AI data-center planning and grid connection
- Government Decision 4255 corroboration
- Private-company control classification
- The remaining water, cooling and backup-power evidence gap

## 1. Tower changes the Israel semiconductor picture, but not the leading-edge gap

Tower Semiconductor's 2026 Form 20-F establishes a real Israel-headquartered and Israel-operated specialty foundry capability.

The filing supports the following current picture:

- Tower is incorporated in Israel and headquartered in Migdal HaEmek.
- Fab 2 in Migdal HaEmek is operational.
- Fab 1 ceased production operations during 2025.
- Fab 2 supports specialty processes including analog, RF, power, mixed signal and CMOS image-sensor technologies.

This capability should be visible in the Israel stack. It should not be presented as a domestic alternative to TSMC for leading-edge AI accelerators.

The correct conclusion is:

> Israel has domestic specialty-semiconductor fabrication, but remains externally dependent for leading-edge AI logic, HBM, EUV and much of the advanced-packaging stack.

## 2. Planning permission and electricity capacity are different capabilities

The Knesset committee approved a planning framework for AI server farms that uses a 50 MW processing-power threshold and allows a limited number of plans to advance through the national-infrastructure planning path.

The 50 MW figure is a legal definition threshold. It is not evidence that a 50 MW facility is operational, connected to the grid or supplied with accelerators.

The dataset therefore needs separate nodes for:

1. AI data-center planning and regulation
2. Physical data-center capacity
3. Electricity generation and grid connection
4. Accelerator access

A project can be legally approved while remaining blocked by electricity, location, cooling, financing or hardware supply.

## 3. Grid access is now an explicit sovereignty constraint

A November 2025 Knesset hearing summary attributes several figures to the Electricity Authority:

- Data centers represented approximately 0.5% of Israeli electricity consumption in 2024.
- The projected share for 2030 was approximately 5% to 7%.
- Connected capacity was reported at approximately 300 MVA in 2024.
- Requested connections through 2030 were reported at approximately 2,500 MVA.
- Approximately 40% of requests were concentrated in the Central district and Greater Tel Aviv.
- The average construction time for a power station was reported as approximately twelve years.

A July 2026 Knesset summary later reported approximately 20,000 MW of connection requests. The two figures cannot be silently combined or substituted. They may reflect different dates, definitions, project stages or scopes.

Until the underlying Electricity Authority and Noga materials are obtained, the UI should show both as dated and unresolved observations, with a visible warning.

## 4. Decision 4255 is officially corroborated, but the legal text is still missing

The Knesset's July 2026 summary of the National AI Directorate presentation corroborates the strategic direction of Government Decision 4255, including:

- A target of access to 100,000 AI processors
- Private-sector construction with the state acting as a customer
- Promotion of AI data-center legislation
- An ambition for an advanced semiconductor plant
- A national quantum-computing direction
- Human-capital and AI-literacy programs

The target must be represented as a policy objective. It is not installed capacity, a completed procurement or a funded operational program.

Detailed claims that appear only in notes about the full government decision remain pending until the official text is recovered.

## 5. AI21 should be represented as an Israeli capability, not automatically as nationally controlled

AI21's official material supports:

- Israeli origin and activity
- Foundation-model and enterprise-AI capability
- Jamba models
- Self-hosted and private deployment options

It does not disclose a complete capitalization table, voting rights or ultimate country of control.

The schema should therefore distinguish:

- `company_origin_country`
- `headquarters_country`
- `verified_control_country`
- `ownership_verification_status`

For AI21, the control field remains unverified rather than being inferred from its founders or offices.

## 6. The water and cooling question remains open

The search found historical government procurement evidence for water-cooled server racks, but not a current national source that quantifies:

- AI data-center water demand
- Cooling-water availability by location
- Required backup generation
- Fuel storage and continuity requirements
- Site-level environmental constraints

These capabilities should remain `research_required`. The system must not manufacture a national constraint score from generic global assumptions.

## Proposed v0.4-rc2 changes

The machine-readable plan is in `data/v0.4-rc2-patch-plan.json`.

The main additions are:

- Tower Semiconductor Israel node
- AI data-center planning-framework node
- Data-center grid-connection constraint node
- Stronger Decision 4255 evidence status
- Explicit AI21 control uncertainty
- Validation rules separating legislative thresholds, specialty fabrication and conflicting hearing metrics

## Current research conclusion

Israel's stack is stronger than a simple import-dependency narrative suggests. It includes domestic R&D, model development, specialty fabrication, local data centers, cloud regions and substantial energy resources.

However, the stack also shows why full sovereignty remains difficult:

- Leading-edge accelerators are imported.
- HBM and advanced packaging are externally concentrated.
- Cloud ownership is largely foreign.
- Domestic fabrication is not leading-edge AI logic fabrication.
- Grid connection may become a more immediate constraint than land or planning permission.
- Several strategic targets remain policy objectives rather than deployed capacity.
