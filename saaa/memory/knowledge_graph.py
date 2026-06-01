"""
SAAA — Personal Knowledge Graph

Builds and maintains a semantic network of concepts as learned
by this specific user. Not an encyclopaedia — a personal topology.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import json


@dataclass
class ConceptNode:
    """A concept in the user's personal knowledge graph."""
    concept_id: str
    label: str
    domain: str
    mastery_score: float = 0.0      # [0, 1] — how well the user knows this
    first_seen: datetime = field(default_factory=datetime.utcnow)
    last_reviewed: Optional[datetime] = None
    review_count: int = 0
    fragile: bool = False           # True if learned by rote without connections

    def update_mastery(self, recall_score: float) -> None:
        alpha = 0.3  # EMA smoothing
        self.mastery_score = alpha * recall_score + (1 - alpha) * self.mastery_score
        self.last_reviewed = datetime.utcnow()
        self.review_count += 1
        # Concept is fragile if mastery is high but connections are few
        # (set externally by KnowledgeGraph after edge count check)


@dataclass
class ConceptEdge:
    """A relationship between two concepts."""
    source_id: str
    target_id: str
    relation_type: str          # e.g. "is-part-of", "causes", "contrasts-with", "analogous-to"
    weight: float = 1.0         # strength of the connection for this user
    user_discovered: bool = True  # True if user identified this connection
    created: datetime = field(default_factory=datetime.utcnow)


class KnowledgeGraph:
    """
    Personal knowledge graph for SAAA.

    Tracks how this specific user organises and connects their knowledge.
    Two users studying the same material will develop different graphs.
    """

    def __init__(self):
        self._nodes: dict[str, ConceptNode] = {}
        self._edges: list[ConceptEdge] = []

    # ── Node management ──────────────────────────────────────────

    def add_concept(self, node: ConceptNode) -> None:
        self._nodes[node.concept_id] = node

    def update_mastery(self, concept_id: str, recall_score: float) -> None:
        if concept_id in self._nodes:
            self._nodes[concept_id].update_mastery(recall_score)
            self._update_fragility(concept_id)

    def _update_fragility(self, concept_id: str) -> None:
        """Mark concept as fragile if highly known but poorly connected."""
        node = self._nodes.get(concept_id)
        if node is None:
            return
        connections = self.neighbour_count(concept_id)
        node.fragile = node.mastery_score > 0.7 and connections < 2

    # ── Edge management ──────────────────────────────────────────

    def add_edge(self, edge: ConceptEdge) -> None:
        self._edges.append(edge)
        # Reinforce both endpoints
        for cid in [edge.source_id, edge.target_id]:
            if cid in self._nodes:
                self._update_fragility(cid)

    def neighbour_count(self, concept_id: str) -> int:
        return sum(
            1 for e in self._edges
            if e.source_id == concept_id or e.target_id == concept_id
        )

    def neighbours(self, concept_id: str) -> list[str]:
        result = set()
        for e in self._edges:
            if e.source_id == concept_id:
                result.add(e.target_id)
            elif e.target_id == concept_id:
                result.add(e.source_id)
        return list(result)

    # ── Analysis ─────────────────────────────────────────────────

    def fragile_concepts(self) -> list[ConceptNode]:
        """Concepts with high mastery but few connections — rote learning risk."""
        return [n for n in self._nodes.values() if n.fragile]

    def gap_concepts(self) -> list[ConceptNode]:
        """Concepts with zero connections — isolated, unintegrated."""
        return [n for n in self._nodes.values() if self.neighbour_count(n.concept_id) == 0]

    def transfer_candidates(
        self, domain_a: str, domain_b: str, min_weight: float = 0.6
    ) -> list[tuple[ConceptNode, ConceptNode]]:
        """
        Find concept pairs from different domains that might be analogous.
        Used by Sapient Synthesis Layer (L6) for transfer bridge detection.
        """
        nodes_a = [n for n in self._nodes.values() if n.domain == domain_a]
        nodes_b = [n for n in self._nodes.values() if n.domain == domain_b]
        candidates = []
        for na in nodes_a:
            for nb in nodes_b:
                # Simple heuristic: same relation type edges in both nodes
                edges_a = {e.relation_type for e in self._edges
                           if e.source_id == na.concept_id or e.target_id == na.concept_id}
                edges_b = {e.relation_type for e in self._edges
                           if e.source_id == nb.concept_id or e.target_id == nb.concept_id}
                if edges_a & edges_b:  # shared relation types
                    candidates.append((na, nb))
        return candidates

    def topology_summary(self) -> dict:
        """Summary of the current knowledge topology."""
        domains = {}
        for n in self._nodes.values():
            domains.setdefault(n.domain, []).append(n.mastery_score)

        return {
            "total_concepts": len(self._nodes),
            "total_connections": len(self._edges),
            "fragile_concepts": len(self.fragile_concepts()),
            "isolated_concepts": len(self.gap_concepts()),
            "domains": {
                d: {
                    "count": len(scores),
                    "mean_mastery": round(sum(scores) / len(scores), 3),
                }
                for d, scores in domains.items()
            },
        }

    def to_dict(self) -> dict:
        return {
            "nodes": [
                {
                    "id": n.concept_id,
                    "label": n.label,
                    "domain": n.domain,
                    "mastery": round(n.mastery_score, 3),
                    "fragile": n.fragile,
                    "connections": self.neighbour_count(n.concept_id),
                }
                for n in self._nodes.values()
            ],
            "edges": [
                {
                    "source": e.source_id,
                    "target": e.target_id,
                    "relation": e.relation_type,
                    "weight": round(e.weight, 3),
                    "user_discovered": e.user_discovered,
                }
                for e in self._edges
            ],
        }
