#!/usr/bin/env python3
"""Validate an AI Sovereignty Lab multipart research dataset candidate."""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_candidate(manifest_path: Path) -> tuple[dict[str, Any], dict[str, Any], bytes]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    base_dir = manifest_path.parent
    canonical = manifest["canonical_dataset"]

    encoded = "".join(
        (base_dir / part).read_text(encoding="ascii")
        for part in canonical["parts"]
    )
    compressed = base64.b64decode("".join(encoded.split()), validate=True)

    actual_gzip_hash = sha256_bytes(compressed)
    expected_gzip_hash = canonical["gzip_sha256"]
    if actual_gzip_hash != expected_gzip_hash:
        raise ValueError(
            f"Gzip checksum mismatch: expected {expected_gzip_hash}, got {actual_gzip_hash}"
        )

    raw = gzip.decompress(compressed)
    actual_json_hash = sha256_bytes(raw)
    expected_json_hash = canonical["decoded_json_sha256"]
    if actual_json_hash != expected_json_hash:
        raise ValueError(
            f"JSON checksum mismatch: expected {expected_json_hash}, got {actual_json_hash}"
        )

    expected_bytes = canonical.get("decoded_bytes")
    if expected_bytes is not None and len(raw) != expected_bytes:
        raise ValueError(
            f"Decoded byte count mismatch: expected {expected_bytes}, got {len(raw)}"
        )

    return manifest, json.loads(raw), raw


def validate_structure(manifest: dict[str, Any], dataset: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    sources = dataset.get("sources", [])
    nodes = dataset.get("nodes", [])
    edges = dataset.get("edges", [])
    ecosystems = dataset.get("ecosystems", [])

    source_ids = {source["id"] for source in sources}
    node_ids = {node["id"] for node in nodes}

    if len(source_ids) != len(sources):
        errors.append("Duplicate source IDs detected")
    if len(node_ids) != len(nodes):
        errors.append("Duplicate node IDs detected")

    edge_ids = [edge["id"] for edge in edges]
    if len(set(edge_ids)) != len(edge_ids):
        errors.append("Duplicate edge IDs detected")

    for node in nodes:
        for source_id in node.get("source_ids", []):
            if source_id not in source_ids:
                errors.append(f"Node {node['id']} references missing source {source_id}")
        for metric in node.get("metrics", []):
            for source_id in metric.get("source_ids", []):
                if source_id not in source_ids:
                    errors.append(
                        f"Metric in node {node['id']} references missing source {source_id}"
                    )

    incoming: Counter[str] = Counter()
    outgoing: Counter[str] = Counter()
    for edge in edges:
        if edge["from"] not in node_ids:
            errors.append(f"Edge {edge['id']} references missing source node {edge['from']}")
        if edge["to"] not in node_ids:
            errors.append(f"Edge {edge['id']} references missing target node {edge['to']}")
        for source_id in edge.get("source_ids", []):
            if source_id not in source_ids:
                errors.append(f"Edge {edge['id']} references missing source {source_id}")
        outgoing[edge["from"]] += 1
        incoming[edge["to"]] += 1

    isolated = sorted(
        node_id for node_id in node_ids if not incoming[node_id] and not outgoing[node_id]
    )
    if isolated:
        errors.append(f"Isolated nodes detected: {', '.join(isolated)}")

    capability_layers = {
        layer["id"] for layer in dataset.get("capability_schema", {}).get("layers", [])
    }
    for ecosystem in ecosystems:
        stack = ecosystem.get("capability_stack", {})
        missing_layers = sorted(capability_layers - set(stack))
        if missing_layers:
            errors.append(
                f"Ecosystem {ecosystem['id']} is missing capability layers: {missing_layers}"
            )
        for layer_id, entry in stack.items():
            for key in ("node_ids", "allied_access_node_ids"):
                for node_id in entry.get(key, []):
                    if node_id not in node_ids:
                        errors.append(
                            f"Ecosystem {ecosystem['id']} layer {layer_id} references missing node {node_id}"
                        )

    expected_counts = manifest.get("counts", {})
    actual_counts = {
        "ecosystems": len(ecosystems),
        "nodes": len(nodes),
        "edges": len(edges),
        "sources": len(sources),
        "capability_layers": len(capability_layers),
    }
    for key, expected in expected_counts.items():
        actual = actual_counts.get(key)
        if actual != expected:
            errors.append(f"Count mismatch for {key}: expected {expected}, got {actual}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "manifest",
        nargs="?",
        default="data/candidates/v0.4-rc1/manifest.json",
        type=Path,
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        help="Optional path for the validated decoded canonical JSON.",
    )
    args = parser.parse_args()

    manifest, dataset, raw = load_candidate(args.manifest)
    errors = validate_structure(manifest, dataset)

    if errors:
        print("Candidate validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_bytes(raw)
        print(f"Wrote validated canonical JSON to {args.output_json}")

    print(
        "Candidate validation passed: "
        f"{manifest['counts']['ecosystems']} ecosystems, "
        f"{manifest['counts']['nodes']} nodes, "
        f"{manifest['counts']['edges']} edges, "
        f"{manifest['counts']['sources']} sources."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
