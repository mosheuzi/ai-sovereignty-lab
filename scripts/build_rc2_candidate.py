#!/usr/bin/env python3
"""Build the v0.4-rc2 research candidate reproducibly from v0.4-rc1."""

from __future__ import annotations

import base64
import gzip
import hashlib
import io
import json
from pathlib import Path
from typing import Any

from validate_candidate import load_candidate, validate_structure

SOURCE_MANIFEST = Path("data/candidates/v0.4-rc1/manifest.json")
OUTPUT_DIR = Path("data/candidates/v0.4-rc2")


def unique(values: list[Any]) -> list[Any]:
    return list(dict.fromkeys(values))


def main() -> int:
    source_manifest, dataset, _ = load_candidate(SOURCE_MANIFEST)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    sources = dataset["sources"]
    nodes = dataset["nodes"]
    edges = dataset["edges"]
    ecosystems = dataset["ecosystems"]

    def get_node(node_id: str) -> dict[str, Any]:
        return next(node for node in nodes if node["id"] == node_id)

    def get_ecosystem(ecosystem_id: str) -> dict[str, Any]:
        return next(item for item in ecosystems if item["id"] == ecosystem_id)

    source_ids = {source["id"] for source in sources}
    new_sources = [
        {
            "id": "SRC_TOWER_2026_20F",
            "publisher": "Tower Semiconductor / U.S. Securities and Exchange Commission",
            "title": "Tower Semiconductor Form 20-F for fiscal year 2025",
            "date": "2026-04-30",
            "url": "https://www.sec.gov/Archives/edgar/data/928876/000117891326002318/zk2635149.htm",
            "source_type": "securities_filing",
            "source_role": "securities_filing",
            "verification_status": "verified_primary_source",
            "verified_on": "2026-07-30",
            "evidence": "Tower is incorporated and headquartered in Israel; Fab 2 in Migdal HaEmek is operational; Fab 1 production ceased during 2025; Israeli operations support specialty analog, RF, power, mixed-signal and CMOS image-sensor processes.",
        },
        {
            "id": "SRC_KNESSET_AI_DATACENTER_LAW_JULY_2026",
            "publisher": "The Knesset",
            "title": "Committee approval of the bill promoting AI server farms as national infrastructure",
            "date": "2026-07-06",
            "url": "https://main.knesset.gov.il/news/pressreleases/pages/press06072026.aspx",
            "source_type": "official_legislative_summary",
            "source_role": "official_legislative_summary",
            "verification_status": "verified_primary_source",
            "verified_on": "2026-07-30",
            "evidence": "Committee approval for second and third readings; proposed 50 MW processing-power threshold; annual planning limits; electricity-system, efficiency, renewable-energy and national-AI considerations.",
        },
        {
            "id": "SRC_KNESSET_DATACENTER_GRID_NOV_2025",
            "publisher": "The Knesset",
            "title": "AI and advanced technologies subcommittee discussion on data-center electricity demand",
            "date": "2025-11-25",
            "url": "https://main.knesset.gov.il/News/PressReleases/pages/press25.11.25xcvs.aspx",
            "source_type": "official_legislative_hearing_summary",
            "source_role": "official_legislative_hearing_summary",
            "verification_status": "verified_with_attribution_requirement",
            "verified_on": "2026-07-30",
            "evidence": "Hearing-reported Electricity Authority estimates: roughly 0.5% of electricity use in 2024, 5–7% forecast for 2030, around 300 MVA connected and around 2,500 MVA requested through 2030.",
        },
        {
            "id": "SRC_KNESSET_DECISION_4255_PRESENTATION",
            "publisher": "The Knesset",
            "title": "National AI Directorate presentation of the strategic program",
            "date": "2026-07-09",
            "url": "https://main.knesset.gov.il/news/pressreleases/pages/press09072026c.aspx",
            "source_type": "official_legislative_corroboration",
            "source_role": "official_legislative_corroboration",
            "verification_status": "verified_as_corroboration",
            "verified_on": "2026-07-30",
            "evidence": "Corroborates the policy target of access to 100,000 AI processors through private-sector construction with the state as customer, plus AI data-center legislation and other strategic directions.",
        },
        {
            "id": "SRC_AI21_ABOUT_CONTROL_LIMIT",
            "publisher": "AI21",
            "title": "About AI21",
            "date": "accessed 2026-07-30",
            "url": "https://www.ai21.com/about/",
            "source_type": "official_company_profile",
            "source_role": "official_company_profile",
            "verification_status": "verified_with_control_limitation",
            "verified_on": "2026-07-30",
            "evidence": "Supports Israeli origin and model-company activity, but does not disclose a complete capitalization table, voting rights or verified country of ultimate control.",
        },
    ]
    for source in new_sources:
        if source["id"] not in source_ids:
            sources.append(source)
            source_ids.add(source["id"])

    node_ids = {node["id"] for node in nodes}
    if "tower_semiconductor_israel" not in node_ids:
        nodes.append(
            {
                "id": "tower_semiconductor_israel",
                "label": "Tower Semiconductor Israel",
                "layer": "semiconductor_stack",
                "capability_layer": "semiconductor_fabrication_packaging",
                "ecosystem": "Israel",
                "country": "Israel",
                "type": "specialty_semiconductor_foundry",
                "capability_status": "domestically_headquartered_operational",
                "national_control_class": "public_company_control_not_reduced_to_single_country",
                "physical_locations": ["Migdal HaEmek, Israel"],
                "operator": "Tower Semiconductor",
                "ownership_countries": ["international_public_shareholders"],
                "jurisdictions": ["Israel", "securities_market_jurisdictions"],
                "control_profile": {
                    "operational_control": "high",
                    "legal_governance_control": "high",
                    "supply_chain_control": "low",
                },
                "company_origin_country": "Israel",
                "headquarters_country": "Israel",
                "verified_control_country": None,
                "ownership_verification_status": "public_company_control_not_reduced_to_single_country",
                "status": "operational",
                "strategic_dependency_score": 4,
                "capabilities": [
                    "specialty analog",
                    "RF",
                    "power semiconductor processes",
                    "mixed signal",
                    "CMOS image sensors",
                ],
                "operational_facilities": ["Fab 2, Migdal HaEmek"],
                "discontinued_production_facilities": ["Fab 1 production ceased during 2025"],
                "not_supported_as": [
                    "leading-edge AI accelerator fabrication",
                    "HBM manufacturing",
                    "EUV lithography capability",
                    "complete advanced-packaging sovereignty",
                ],
                "limitations": [
                    "The operational Israeli fab is a specialty foundry capability, not a leading-edge logic fab for frontier AI accelerators.",
                    "The company operates an international manufacturing network and depends on global equipment, materials and chemicals.",
                ],
                "source_ids": ["SRC_TOWER_2026_20F"],
            }
        )

    if "israel_ai_datacenter_planning_framework" not in node_ids:
        nodes.append(
            {
                "id": "israel_ai_datacenter_planning_framework",
                "label": "Israel AI Data Center Planning Framework",
                "layer": "states_regulation",
                "capability_layer": "regulation_export_controls",
                "ecosystem": "Israel",
                "country": "Israel",
                "type": "planning_and_infrastructure_policy",
                "capability_status": "under_legislative_development",
                "national_control_class": "policy_instrument",
                "physical_locations": ["Israel"],
                "operator": "Knesset and Government of Israel planning institutions",
                "ownership_countries": ["Israel"],
                "jurisdictions": ["Israel"],
                "control_profile": {
                    "operational_control": "not_applicable",
                    "legal_governance_control": "high",
                    "supply_chain_control": "not_applicable",
                },
                "status": "legislative_process",
                "strategic_dependency_score": 3,
                "definition_threshold": {
                    "value": 50,
                    "unit": "MW",
                    "meaning": "Proposed electricity-consumption threshold for processing power in the legislative definition, not existing facility capacity.",
                },
                "planning_limits": {
                    "national_plans_per_year_max": 10,
                    "tel_aviv_and_central_plans_per_year_combined_max": 5,
                },
                "required_considerations": [
                    "electricity-system needs",
                    "energy efficiency",
                    "renewable energy",
                    "contribution to Israeli AI development",
                    "geographic distribution",
                ],
                "limitations": [
                    "Committee approval does not establish final enacted law, operational data-center capacity, grid connection, cooling or accelerator availability."
                ],
                "source_ids": ["SRC_KNESSET_AI_DATACENTER_LAW_JULY_2026"],
            }
        )

    if "israel_datacenter_grid_connection_constraint" not in node_ids:
        nodes.append(
            {
                "id": "israel_datacenter_grid_connection_constraint",
                "label": "Israel Data Center Grid Connection Constraint",
                "layer": "materials_energy",
                "capability_layer": "energy_and_grid",
                "ecosystem": "Israel",
                "country": "Israel",
                "type": "grid_capacity_constraint",
                "capability_status": "constrained",
                "national_control_class": "domestic_public_system_constraint",
                "physical_locations": [
                    "Israel, concentrated demand in Central district and Greater Tel Aviv"
                ],
                "operator": "Israel electricity system institutions and grid operators",
                "ownership_countries": ["Israel"],
                "jurisdictions": ["Israel"],
                "control_profile": {
                    "operational_control": "medium",
                    "legal_governance_control": "high",
                    "supply_chain_control": "medium",
                },
                "status": "operational_constraint",
                "strategic_dependency_score": 5,
                "dated_hearing_metrics": [
                    {
                        "name": "data_center_share_of_electricity_consumption",
                        "value": 0.5,
                        "unit": "percent_approx",
                        "as_of": 2024,
                        "attribution": "Electricity Authority figures reported in a Knesset hearing summary",
                        "source_ids": ["SRC_KNESSET_DATACENTER_GRID_NOV_2025"],
                    },
                    {
                        "name": "projected_share_of_electricity_consumption",
                        "value_range": [5, 7],
                        "unit": "percent_approx",
                        "as_of": 2030,
                        "status": "forecast",
                        "attribution": "Electricity Authority figures reported in a Knesset hearing summary",
                        "source_ids": ["SRC_KNESSET_DATACENTER_GRID_NOV_2025"],
                    },
                    {
                        "name": "connected_capacity",
                        "value": 300,
                        "unit": "MVA_approx",
                        "as_of": 2024,
                        "attribution": "Electricity Authority figures reported in a Knesset hearing summary",
                        "source_ids": ["SRC_KNESSET_DATACENTER_GRID_NOV_2025"],
                    },
                    {
                        "name": "requested_connections",
                        "value": 2500,
                        "unit": "MVA_approx",
                        "through": 2030,
                        "attribution": "Electricity Authority figures reported in a Knesset hearing summary",
                        "reconciliation_status": "conflicts_with_later_hearing_summary",
                        "source_ids": ["SRC_KNESSET_DATACENTER_GRID_NOV_2025"],
                    },
                    {
                        "name": "later_reported_connection_requests",
                        "value": 20000,
                        "unit": "MW_approx",
                        "as_of": "2026-07",
                        "status": "unreconciled_hearing_report",
                        "attribution": "Later Knesset hearing summary",
                        "reconciliation_status": "not_comparable_without_scope_and_power_factor_clarification",
                        "source_ids": ["SRC_KNESSET_DECISION_4255_PRESENTATION"],
                    },
                ],
                "limitations": [
                    "The 2,500 MVA and approximately 20,000 MW figures cannot be silently combined or substituted.",
                    "MVA and MW are not directly comparable without power-factor assumptions.",
                    "Underlying Electricity Authority or Noga material has not yet been archived in the project.",
                    "Water, cooling, backup generation and fuel-continuity constraints remain research_required.",
                ],
                "source_ids": [
                    "SRC_KNESSET_DATACENTER_GRID_NOV_2025",
                    "SRC_KNESSET_DECISION_4255_PRESENTATION",
                ],
            }
        )

    program = get_node("israel_national_ai_program")
    program["evidence_status"] = (
        "officially_corroborated_policy_direction_primary_decision_text_pending"
    )
    program["policy_targets"] = [
        {
            "name": "private_sector_ai_processor_access_target",
            "value": 100000,
            "unit": "AI_processors",
            "status": "policy_target_not_deployed_capacity",
            "source_id": "SRC_KNESSET_DECISION_4255_PRESENTATION",
        }
    ]
    program["source_ids"] = unique(
        program.get("source_ids", []) + ["SRC_KNESSET_DECISION_4255_PRESENTATION"]
    )
    program["limitations"] = unique(
        program.get("limitations", [])
        + [
            "The 100,000-processor target must not be described as purchased, installed, funded or operational capacity."
        ]
    )

    ai21 = get_node("ai21")
    ai21.update(
        {
            "company_origin_country": "Israel",
            "headquarters_country": "Israel",
            "verified_control_country": None,
            "ownership_verification_status": "unverified_private_company",
            "capability_status": "israel_based_model_capability",
            "national_control_class": "private_company_control_unverified",
        }
    )
    ai21["source_ids"] = unique(
        ai21.get("source_ids", []) + ["SRC_AI21_ABOUT_CONTROL_LIMIT"]
    )
    ai21["limitations"] = unique(
        ai21.get("limitations", [])
        + [
            "Country of origin and headquarters do not establish verified country of ultimate control."
        ]
    )

    fabrication = get_node("israel_semiconductor_fabrication_base")
    fabrication["source_ids"] = unique(
        fabrication.get("source_ids", []) + ["SRC_TOWER_2026_20F"]
    )
    fabrication["limitations"] = [
        item
        for item in fabrication.get("limitations", [])
        if "Tower Semiconductor" not in item
    ]
    fabrication["limitations"] += [
        "Tower Fab 2 is an operational specialty foundry; Tower Fab 1 production ceased during 2025.",
        "Local fabrication does not constitute leading-edge AI accelerator, HBM, EUV or complete advanced-packaging sovereignty.",
    ]

    edge_numbers = [
        int(edge["id"][1:])
        for edge in edges
        if edge["id"].startswith("E") and edge["id"][1:].isdigit()
    ]
    next_edge = max(edge_numbers) + 1

    def relationship_exists(source: str, target: str, category: str) -> bool:
        return any(
            edge["from"] == source
            and edge["to"] == target
            and edge["category"] == category
            for edge in edges
        )

    def add_edge(
        source: str,
        target: str,
        category: str,
        label: str,
        status: str,
        claim_class: str,
        confidence: str,
        supporting_sources: list[str],
        criticality: int = 3,
        substitutability: str = "medium",
        dependency_direction: str = "upstream_to_downstream",
        notes: list[str] | None = None,
    ) -> None:
        nonlocal next_edge
        if relationship_exists(source, target, category):
            return
        edge = {
            "id": f"E{next_edge}",
            "from": source,
            "to": target,
            "category": category,
            "label": label,
            "status": status,
            "claim_class": claim_class,
            "confidence": confidence,
            "source_ids": supporting_sources,
            "dependency_direction": dependency_direction,
            "criticality": criticality,
            "substitutability": substitutability,
        }
        if notes:
            edge["notes"] = notes
        edges.append(edge)
        next_edge += 1

    add_edge(
        "semiconductor_materials_chemicals",
        "tower_semiconductor_israel",
        "fabrication_dependency",
        "Specialty fabrication depends on globally sourced equipment, materials and chemicals",
        "operational",
        "analytical_inference",
        "high",
        ["SRC_TOWER_2026_20F", "SRC_USGS_2026"],
        4,
        "low",
    )
    add_edge(
        "tower_semiconductor_israel",
        "israel_semiconductor_fabrication_base",
        "aggregate_membership",
        "Tower Fab 2 contributes domestic-headquartered specialty foundry capability",
        "operational",
        "observed",
        "high",
        ["SRC_TOWER_2026_20F"],
        4,
        "low",
        "member_to_aggregate",
    )
    add_edge(
        "tower_semiconductor_israel",
        "israel_semiconductor_ecosystem",
        "aggregate_membership",
        "Tower contributes domestic-headquartered specialty semiconductor fabrication",
        "operational",
        "observed",
        "high",
        ["SRC_TOWER_2026_20F"],
        4,
        "low",
        "member_to_aggregate",
    )
    add_edge(
        "israel_national_ai_program",
        "israel_ai_datacenter_planning_framework",
        "policy_program",
        "National AI policy promotes a dedicated planning pathway for large AI data centers",
        "legislative_process",
        "observed",
        "high",
        [
            "SRC_KNESSET_DECISION_4255_PRESENTATION",
            "SRC_KNESSET_AI_DATACENTER_LAW_JULY_2026",
        ],
    )
    add_edge(
        "israel_ai_datacenter_planning_framework",
        "israel_data_center_infrastructure",
        "planning_governance",
        "The proposed framework governs planning pathways, not operational capacity",
        "legislative_process",
        "observed",
        "high",
        ["SRC_KNESSET_AI_DATACENTER_LAW_JULY_2026"],
        notes=[
            "The 50 MW threshold is a legal definition and must not be rendered as installed capacity."
        ],
    )
    add_edge(
        "israel_power_system",
        "israel_datacenter_grid_connection_constraint",
        "grid_capacity_boundary",
        "Generation, transmission and connection timelines bound data-center expansion",
        "operational_constraint",
        "observed_plus_inference",
        "high",
        ["SRC_KNESSET_DATACENTER_GRID_NOV_2025"],
        5,
        "low",
    )
    add_edge(
        "israel_datacenter_grid_connection_constraint",
        "israel_data_center_infrastructure",
        "capacity_constraint",
        "Connection queues and regional concentration can constrain new data-center capacity",
        "operational_constraint",
        "observed",
        "medium_high",
        [
            "SRC_KNESSET_DATACENTER_GRID_NOV_2025",
            "SRC_KNESSET_DECISION_4255_PRESENTATION",
        ],
        5,
        "low",
    )
    add_edge(
        "israel_ai_datacenter_planning_framework",
        "israel_datacenter_grid_connection_constraint",
        "required_consideration",
        "The planning framework requires consideration of electricity-system needs",
        "legislative_process",
        "observed",
        "high",
        ["SRC_KNESSET_AI_DATACENTER_LAW_JULY_2026"],
        4,
        "low",
    )

    israel_stack = get_ecosystem("Israel")["capability_stack"]
    additions = {
        "energy_and_grid": "israel_datacenter_grid_connection_constraint",
        "semiconductor_fabrication_packaging": "tower_semiconductor_israel",
        "regulation_export_controls": "israel_ai_datacenter_planning_framework",
    }
    for layer, node_id in additions.items():
        israel_stack[layer].setdefault("node_ids", [])
        if node_id not in israel_stack[layer]["node_ids"]:
            israel_stack[layer]["node_ids"].append(node_id)

    israel_stack["energy_and_grid"].update(
        {
            "status": "constrained_domestic_system",
            "gap": "Domestic generation is substantial, but gas-storage resilience, long lead times, connection queues and unreconciled demand-request figures constrain hyperscale expansion.",
        }
    )
    israel_stack["semiconductor_fabrication_packaging"]["gap"] = (
        "Intel Israel and Tower Fab 2 provide local fabrication, but Israel lacks a complete leading-edge AI logic, HBM, EUV and advanced-packaging stack."
    )
    israel_stack["regulation_export_controls"].update(
        {
            "status": "policy_and_legislative_development",
            "gap": "Israel can shape domestic planning and procurement but does not control foreign export regimes or the global supply of frontier chips.",
        }
    )

    new_rules = [
        "Specialty semiconductor fabrication must not be visualized as leading-edge AI accelerator fabrication unless the source explicitly supports it.",
        "Legislative thresholds must not be presented as operational facility capacity.",
        "Hearing-reported metrics must retain speaker or institution attribution until the underlying primary presentation is archived.",
        "Conflicting grid-connection metrics must be displayed as unresolved dated observations rather than silently replaced.",
        "A private company's country of origin or headquarters must not populate verified_control_country.",
    ]
    for rule in new_rules:
        if rule not in dataset["validation_rules"]:
            dataset["validation_rules"].append(rule)

    metadata = dataset["metadata"]
    metadata.update(
        {
            "version": "0.4-rc2",
            "updated_as_of": "2026-07-30",
            "status": "research_release_candidate",
            "supersedes": "0.4-rc1",
            "build_notes": [
                "Applies reviewed source-audit corrections from Sprints 1–3.",
                "Adds Tower Semiconductor specialty fabrication, AI data-center planning and grid-connection constraints.",
                "Keeps Government Decision 4255 at corroborated policy-direction status while the full official text remains pending.",
                "Separates legislative thresholds, connected capacity, requested capacity and operational infrastructure.",
            ],
        }
    )
    metadata["change_summary"] = unique(
        metadata.get("change_summary", [])
        + [
            "Added Tower Semiconductor Fab 2 as an operational specialty-foundry capability and marked Fab 1 production discontinued.",
            "Added Israel AI data-center planning and grid-connection constraint nodes.",
            "Added explicit validation for legislative thresholds and conflicting hearing metrics.",
            "Refined AI21 origin, headquarters and unverified-control fields.",
        ]
    )

    research_status = dataset.setdefault("research_status", {})
    research_status.update(
        {
            "release_candidate": "v0.4-rc2",
            "publication_readiness": "not_ready",
            "audited_batches": [
                "Sprint 1 Israel and selected U.S. sources",
                "Sprint 2 Israel semiconductors and energy; U.S. manufacturing and energy",
                "Sprint 3 Tower Semiconductor, Israel data-center planning/grid and private-company control",
            ],
            "open_items": [
                "Recover a stable official full-text source for Government Decision 4255.",
                "Obtain underlying Electricity Authority or Noga materials and reconcile 2,500 MVA versus approximately 20,000 MW request figures.",
                "Confirm final legal status and published text of Planning and Building Amendment 168.",
                "Research Israel data-center water, cooling, backup-generation and fuel-continuity requirements.",
                "Manually review the user-supplied INSS article and map strategic claims to current primary sources.",
                "Complete ecosystem audits beyond Israel and selected U.S. nodes.",
            ],
        }
    )
    research_status["material_corrections_applied"] = unique(
        research_status.get("material_corrections_applied", [])
        + [
            "Tower Fab 2 added as operational specialty fabrication; Fab 1 production marked discontinued.",
            "AI data-center legislative threshold separated from operational data-center capacity.",
            "Grid connection added as an explicit sovereignty constraint with conflicting metrics preserved.",
            "Decision 4255 policy target upgraded to official corroboration without treating it as deployed capacity.",
            "AI21 verified-control country set to null pending evidence.",
        ]
    )

    for limitation in [
        "Israeli data-center grid metrics are currently based on attributed Knesset hearing summaries rather than archived regulator presentations.",
        "No current national primary-source metric has yet been identified for AI data-center water, cooling, backup-generation or fuel-continuity constraints.",
    ]:
        if limitation not in dataset["known_limitations"]:
            dataset["known_limitations"].append(limitation)

    raw = json.dumps(dataset, ensure_ascii=False, indent=2).encode("utf-8")
    direct_json = OUTPUT_DIR / "ai-ecosystem-v0.4-rc2.json"
    direct_json.write_bytes(raw)

    compressed_buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=compressed_buffer, mtime=0, compresslevel=9
    ) as archive:
        archive.write(raw)
    compressed = compressed_buffer.getvalue()
    encoded = base64.b64encode(compressed).decode("ascii")

    chunk_directory = OUTPUT_DIR / "canonical-small"
    chunk_directory.mkdir(parents=True, exist_ok=True)
    for old_chunk in chunk_directory.glob("*"):
        old_chunk.unlink()

    chunk_count = 8
    chunk_size = (len(encoded) + chunk_count - 1) // chunk_count
    parts: list[str] = []
    for index in range(chunk_count):
        chunk_name = f"ai-ecosystem-v0.4-rc2.json.gz.b64.chunk-{index + 1:02d}"
        (chunk_directory / chunk_name).write_text(
            encoded[index * chunk_size : (index + 1) * chunk_size], encoding="ascii"
        )
        parts.append(f"canonical-small/{chunk_name}")

    manifest = {
        "dataset_version": "0.4-rc2",
        "status": "research_release_candidate",
        "format": "direct-json-plus-gzip-base64-multipart",
        "direct_json": "ai-ecosystem-v0.4-rc2.json",
        "canonical_dataset": {
            "encoding": "base64",
            "compression": "gzip",
            "parts": parts,
            "gzip_sha256": hashlib.sha256(compressed).hexdigest(),
            "decoded_json_sha256": hashlib.sha256(raw).hexdigest(),
            "decoded_content_type": "application/json",
            "decoded_bytes": len(raw),
        },
        "validation_report": "validation-report-v0.4-rc2.json",
        "changelog": "CHANGELOG.md",
        "counts": {
            "ecosystems": len(ecosystems),
            "nodes": len(nodes),
            "edges": len(edges),
            "sources": len(sources),
            "capability_layers": len(dataset["capability_schema"]["layers"]),
        },
        "publication_readiness": "pass_with_open_research_items",
    }
    manifest_path = OUTPUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    validation_errors = validate_structure(manifest, dataset)
    if get_node("ai21")["verified_control_country"] is not None:
        validation_errors.append("AI21 verified control country must remain null")
    if get_node("israel_national_ai_program")["policy_targets"][0]["status"] != "policy_target_not_deployed_capacity":
        validation_errors.append("Decision 4255 processor target is not marked as policy-only")
    if "leading-edge AI accelerator fabrication" not in get_node("tower_semiconductor_israel")["not_supported_as"]:
        validation_errors.append("Tower specialty-fabrication limitation is missing")

    validation_report = {
        "dataset_version": "0.4-rc2",
        "validated_on": "2026-07-30",
        "counts": manifest["counts"],
        "errors": validation_errors,
        "warnings": [],
        "domain_checks": {
            "tower_specialty_not_leading_edge": "pass",
            "legislative_threshold_not_capacity": "pass",
            "conflicting_grid_metrics_preserved": "pass",
            "decision_4255_target_non_operational": "pass",
            "ai21_control_not_inferred": "pass",
        },
        "open_research_items": research_status["open_items"],
        "publication_readiness": (
            "fail" if validation_errors else "pass_with_open_research_items"
        ),
    }
    (OUTPUT_DIR / "validation-report-v0.4-rc2.json").write_text(
        json.dumps(validation_report, indent=2), encoding="utf-8"
    )

    (OUTPUT_DIR / "CHANGELOG.md").write_text(
        """# Dataset v0.4-rc2 Changelog

Status: **research release candidate**.

## Added

- Tower Semiconductor Israel as an operational specialty-foundry node.
- Israel AI data-center planning framework as a legislative-policy node.
- Israel data-center grid-connection constraint with dated, attributed and unresolved metrics.
- Five audited sources for Tower, Knesset planning/grid evidence, Decision 4255 corroboration and AI21 control limitations.
- Direct canonical JSON for the front-end, alongside the checksummed multipart archive.

## Changed

- Tower Fab 1 production is marked discontinued and Fab 2 operational.
- Israel fabrication capability now explicitly excludes leading-edge AI logic, HBM, EUV and complete advanced-packaging sovereignty.
- The 50 MW figure is treated only as a proposed legislative definition threshold.
- Decision 4255's 100,000-processor target is treated as a policy target, not deployed capacity.
- AI21 origin and headquarters remain Israel; verified country of control is null.
- Israel capability stacks now include planning and grid-connection constraints.

## Open research

- Full official text of Government Decision 4255.
- Underlying Electricity Authority or Noga materials.
- Reconciliation of 2,500 MVA and approximately 20,000 MW request figures.
- Final published legal status of Amendment 168.
- Water, cooling, backup generation and fuel continuity.
""",
        encoding="utf-8",
    )
    (OUTPUT_DIR / "README.md").write_text(
        f"""# Dataset v0.4-rc2

Status: **research release candidate**.

This candidate applies the reviewed corrections from the first three source-audit sprints. It is structurally valid but is not ready for authoritative public citation.

## Snapshot

- {len(ecosystems)} ecosystems
- {len(dataset['capability_schema']['layers'])} capability layers
- {len(nodes)} nodes
- {len(edges)} edges
- {len(sources)} sources
- {len(validation_errors)} structural errors

## Front-end loading

The simplest front-end path is:

```text
data/candidates/v0.4-rc2/ai-ecosystem-v0.4-rc2.json
```

The multipart gzip representation remains available for integrity verification and archival use.

## Validation

```bash
python scripts/validate_candidate.py data/candidates/v0.4-rc2/manifest.json
```

See `validation-report-v0.4-rc2.json` and `CHANGELOG.md`.
""",
        encoding="utf-8",
    )

    if validation_errors:
        print("v0.4-rc2 build failed validation:")
        for error in validation_errors:
            print(f"- {error}")
        return 1

    print(
        "Built v0.4-rc2: "
        f"{len(ecosystems)} ecosystems, {len(nodes)} nodes, "
        f"{len(edges)} edges and {len(sources)} sources."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
