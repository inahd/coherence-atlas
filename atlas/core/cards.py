"""Graph-driven card projections for Atlas.

This module builds card artifacts directly from the canonical graph so the
card layer remains a thin projection of graph truth.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

DEFAULT_GRAPH_PATH = Path("memory/graphs/canonical_graph.json")
DEFAULT_OUT_PATH = Path("atlas/cards/cards.json")
CARD_TYPES = {"nakshatra", "graha", "deity", "plant", "rashi", "ritual"}


def _edge_list(graph: dict) -> list[dict]:
    if isinstance(graph.get("edges"), list):
        return graph["edges"]
    if isinstance(graph.get("links"), list):
        return graph["links"]
    return []


def _edge_source(edge: dict) -> str | None:
    return edge.get("source") or edge.get("from") or edge.get("from_id")


def _edge_target(edge: dict) -> str | None:
    return edge.get("target") or edge.get("to") or edge.get("to_id")


def _edge_relation(edge: dict) -> str:
    return edge.get("relation") or edge.get("type") or edge.get("label") or "related_to"


def load_graph(path: Path = DEFAULT_GRAPH_PATH) -> dict:
    return json.loads(path.read_text())


def build_cards(graph: dict, card_types: set[str] = CARD_TYPES) -> list[dict]:
    nodes = graph.get("nodes") if isinstance(graph.get("nodes"), list) else []
    edges = _edge_list(graph)

    by_id = {node.get("id"): node for node in nodes if node.get("id")}
    outgoing: dict[str, list[dict]] = defaultdict(list)
    for edge in edges:
        src = _edge_source(edge)
        if src:
            outgoing[src].append(edge)

    cards: list[dict] = []
    for node in nodes:
        node_type = node.get("type")
        node_id = node.get("id")
        if node_type not in card_types or not node_id:
            continue

        resonances = []
        for edge in outgoing.get(node_id, []):
            target_id = _edge_target(edge)
            if not target_id:
                continue
            target = by_id.get(target_id, {})
            resonances.append(
                {
                    "relation": _edge_relation(edge),
                    "target_id": target_id,
                    "target_label": target.get("label") or target_id,
                    "target_type": target.get("type") or "unknown",
                }
            )

        card = {
            "id": node_id,
            "name": node.get("label") or node_id,
            "type": node_type,
            "attributes": {
                k: v
                for k, v in node.items()
                if k not in {"id", "label", "type"}
            },
            "resonances": resonances,
        }
        cards.append(card)

    cards.sort(key=lambda c: (c["type"], c["name"]))
    return cards


def build(out_path: Path = DEFAULT_OUT_PATH, graph_path: Path = DEFAULT_GRAPH_PATH) -> int:
    graph = load_graph(graph_path)
    cards = build_cards(graph)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(cards, indent=2))
    print(f"Cards generated: {len(cards)}")
    print(f"Graph source: {graph_path}")
    print(f"Output: {out_path}")
    return len(cards)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Atlas cards from canonical graph")
    parser.add_argument("--graph", default=str(DEFAULT_GRAPH_PATH), help="Path to graph JSON")
    parser.add_argument("--out", default=str(DEFAULT_OUT_PATH), help="Path to output cards JSON")
    args = parser.parse_args()
    build(out_path=Path(args.out), graph_path=Path(args.graph))


if __name__ == "__main__":
    main()
