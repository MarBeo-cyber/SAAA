"""
SAAA — Test Suite
"""

import pytest
from datetime import datetime
from saaa.core.state import LearningState
from saaa.learning.state_engine import LearningStateEngine
from saaa.learning.fsrs_scheduler import FSRSScheduler, CardState, Rating
from saaa.feedback.adaptive_feedback import AdaptiveFeedbackEngine
from saaa.memory.consolidation import ConsolidationScheduler, StudyItem
from saaa.memory.knowledge_graph import KnowledgeGraph, ConceptNode, ConceptEdge
from saaa.safety.governor import SafetyGovernor


# ── LearningStateEngine ──────────────────────────────────────────

class TestLearningStateEngine:

    def setup_method(self):
        self.engine = LearningStateEngine()

    def test_outputs_valid_range(self):
        state = self.engine.estimate(3.0, 0.8, 0.2, 20)
        assert 0.0 <= state.attention <= 1.0
        assert 0.0 <= state.fatigue <= 1.0
        assert 0.0 <= state.encoding_probability <= 1.0
        assert 0.0 <= state.overload_risk <= 1.0

    def test_productive_state(self):
        state = self.engine.estimate(1.5, 0.90, 0.10, 15)
        assert state.label == "productive"

    def test_fatigued_state(self):
        state = self.engine.estimate(7.0, 0.50, 0.85, 55)
        assert state.label in ("fatigued", "overloaded")

    def test_overloaded_state(self):
        state = self.engine.estimate(9.0, 0.30, 0.95, 70)
        assert state.label == "overloaded"

    def test_has_timestamp(self):
        state = self.engine.estimate(3.0, 0.7, 0.3, 25)
        assert isinstance(state.timestamp, datetime)


# ── FSRSScheduler ─────────────────────────────────────────────────

class TestFSRSScheduler:

    def setup_method(self):
        self.sched = FSRSScheduler(request_retention=0.90)
        self.card  = CardState(item_id="t001", topic="Test concept")

    def test_first_review_sets_stability(self):
        card = self.sched.review(self.card, Rating.GOOD)
        assert card.stability > 0
        assert card.reviews == 1

    def test_easy_rating_higher_stability(self):
        c_good = self.sched.review(CardState("a", "a"), Rating.GOOD)
        c_easy = self.sched.review(CardState("b", "b"), Rating.EASY)
        assert c_easy.stability >= c_good.stability

    def test_again_marks_lapsed(self):
        card = self.sched.review(self.card, Rating.AGAIN)
        assert card.lapsed

    def test_next_review_set(self):
        card = self.sched.review(self.card, Rating.GOOD)
        assert card.next_review is not None
        assert card.next_review > datetime.utcnow()

    def test_retention_summary(self):
        cards = [self.sched.review(CardState(f"c{i}", "t"), Rating.GOOD) for i in range(5)]
        summary = self.sched.retention_summary(cards)
        assert "total_items" in summary
        assert summary["total_items"] == 5


# ── KnowledgeGraph ────────────────────────────────────────────────

class TestKnowledgeGraph:

    def setup_method(self):
        self.kg = KnowledgeGraph()
        self.kg.add_concept(ConceptNode("n1", "Autopoiesis", "biology", mastery_score=0.8))
        self.kg.add_concept(ConceptNode("n2", "Closure",     "biology", mastery_score=0.7))
        self.kg.add_concept(ConceptNode("n3", "Feedback",    "economics", mastery_score=0.6))
        self.kg.add_edge(ConceptEdge("n1", "n2", "requires"))

    def test_add_and_count_nodes(self):
        summary = self.kg.topology_summary()
        assert summary["total_concepts"] == 3

    def test_edge_creates_connection(self):
        assert self.kg.neighbour_count("n1") == 1
        assert self.kg.neighbour_count("n2") == 1

    def test_isolated_concept_detected(self):
        isolated = self.kg.gap_concepts()
        assert any(n.concept_id == "n3" for n in isolated)

    def test_mastery_update(self):
        self.kg.update_mastery("n1", 0.95)
        node = self.kg._nodes["n1"]
        assert node.mastery_score > 0.8  # EMA moved up

    def test_fragile_detection(self):
        # n3 has high mastery but no connections
        self.kg.update_mastery("n3", 0.95)
        fragile = self.kg.fragile_concepts()
        assert any(n.concept_id == "n3" for n in fragile)

    def test_transfer_candidates(self):
        self.kg.add_edge(ConceptEdge("n1", "n2", "requires"))
        self.kg.add_edge(ConceptEdge("n3", "n3", "requires"))  # self-edge for test
        candidates = self.kg.transfer_candidates("biology", "economics")
        # candidates may be empty — just check it runs
        assert isinstance(candidates, list)

    def test_to_dict_structure(self):
        d = self.kg.to_dict()
        assert "nodes" in d
        assert "edges" in d


# ── SafetyGovernor ────────────────────────────────────────────────

class TestSafetyGovernor:

    def setup_method(self):
        self.gov = SafetyGovernor(strict_mode=True)

    def test_safe_message_passes(self):
        msg = "Great recall — strong encoding this session."
        assert self.gov.validate_feedback(msg) == msg

    def test_diagnosis_blocked(self):
        with pytest.raises(ValueError):
            self.gov.validate_feedback("Diagnosis: memory disorder detected")

    def test_treats_blocked(self):
        with pytest.raises(ValueError):
            self.gov.validate_feedback("SAAA treats cognitive impairment")

    def test_pressure_framing_blocked(self):
        with pytest.raises(ValueError):
            self.gov.validate_feedback("Poor performance — below average result")

    def test_session_duration_limit(self):
        ok, msg = self.gov.check_session_duration(30)
        assert ok
        not_ok, msg2 = self.gov.check_session_duration(60)
        assert not not_ok
        assert "break" in msg2.lower()

    def test_neurostimulation_disabled_by_default(self):
        assert not self.gov.stimulation_allowed()

    def test_neurostimulation_enabled_with_override(self):
        gov = SafetyGovernor(active_neurostimulation_enabled=True)
        assert gov.stimulation_allowed()

    def test_opportunity_framing(self):
        msg = self.gov.frame_as_opportunity("lower recall scores", "abstract concepts")
        assert "opportunity" in msg.lower() or "strengthen" in msg.lower()
        validated = self.gov.validate_feedback(msg)
        assert validated  # must not raise
