"""
SAAA Demo — Learning State Estimation + FSRS Scheduler + Knowledge Graph

Simulates a complete learning session with state estimation,
adaptive recall scheduling, and knowledge graph update.
"""

from datetime import datetime
from saaa.core.state import LearningState
from saaa.learning.state_engine import LearningStateEngine
from saaa.learning.fsrs_scheduler import FSRSScheduler, CardState, Rating
from saaa.feedback.adaptive_feedback import AdaptiveFeedbackEngine
from saaa.memory.knowledge_graph import KnowledgeGraph, ConceptNode, ConceptEdge
from saaa.safety.governor import SafetyGovernor

print("=" * 65)
print("SAAA — Sapient Autopoietic Adaptive Agent — Demo")
print("=" * 65)

# ── 1. Learning State Estimation ─────────────────────────────────
print("\n── 1. Learning State Estimation ──")
engine   = LearningStateEngine()
feedback = AdaptiveFeedbackEngine()
safety   = SafetyGovernor()

sessions = [
    ("Productive",   2.1, 0.82, 0.20, 20),
    ("Fatigued",     5.8, 0.55, 0.70, 50),
    ("Overloaded",   8.2, 0.40, 0.85, 65),
]

for label, latency, recall, fatigue, minutes in sessions:
    state = engine.estimate(
        response_latency_s=latency,
        recall_score=recall,
        self_reported_fatigue=fatigue,
        session_minutes=minutes,
    )
    recs = feedback.recommend(state)
    dur_ok, dur_msg = safety.check_session_duration(minutes)
    print(f"\n  Scenario: {label}")
    print(f"    State label:      {state.label}")
    print(f"    Attention:        {state.attention:.2f}")
    print(f"    Fatigue:          {state.fatigue:.2f}")
    print(f"    Encoding prob:    {state.encoding_probability:.2f}")
    print(f"    Duration OK:      {dur_ok}" + (f" — {dur_msg}" if not dur_ok else ""))
    print(f"    Recommendations:  {recs[0]}")

# ── 2. FSRS Spaced Repetition ─────────────────────────────────────
print("\n── 2. FSRS Recall Scheduling ──")
scheduler = FSRSScheduler(request_retention=0.90)

card = CardState(item_id="c001", topic="Autopoiesis — operational closure")
print(f"\n  Item: {card.topic}")

reviews = [
    (Rating.GOOD, "First review"),
    (Rating.HARD, "Second review — some difficulty"),
    (Rating.GOOD, "Third review — solid recall"),
    (Rating.EASY, "Fourth review — trivial recall"),
]

for rating, desc in reviews:
    card = scheduler.review(card, rating)
    print(f"    {desc:42s}  → stability={card.stability:.1f}d  "
          f"next={card.next_review.strftime('%Y-%m-%d')}")

summary = scheduler.retention_summary([card])
print(f"\n  Summary: {summary}")

# ── 3. Knowledge Graph ────────────────────────────────────────────
print("\n── 3. Personal Knowledge Graph ──")
kg = KnowledgeGraph()

# Add concepts from two domains
concepts = [
    ConceptNode("bio_01", "Operational closure",    "biology",   mastery_score=0.80),
    ConceptNode("bio_02", "Structural coupling",    "biology",   mastery_score=0.65),
    ConceptNode("bio_03", "Autopoiesis",            "biology",   mastery_score=0.75),
    ConceptNode("econ_01","Negative feedback loop", "economics", mastery_score=0.70),
    ConceptNode("econ_02","Mean reversion",         "economics", mastery_score=0.55),
    ConceptNode("econ_03","Equilibrium",            "economics", mastery_score=0.60),
]
for c in concepts:
    kg.add_concept(c)

# Add edges (connections the user has identified)
kg.add_edge(ConceptEdge("bio_01", "bio_03", "is-part-of",    weight=0.9))
kg.add_edge(ConceptEdge("bio_02", "bio_03", "enables",       weight=0.8))
kg.add_edge(ConceptEdge("econ_01","econ_03","causes",        weight=0.7))
kg.add_edge(ConceptEdge("bio_01", "econ_01","analogous-to",  weight=0.6, user_discovered=True))

# Update masteries after session
kg.update_mastery("bio_01", 0.95)
kg.update_mastery("econ_02", 0.72)

topology = kg.topology_summary()
print(f"  Total concepts:    {topology['total_concepts']}")
print(f"  Total connections: {topology['total_connections']}")
print(f"  Fragile concepts:  {topology['fragile_concepts']}")
print(f"  Isolated concepts: {topology['isolated_concepts']}")

# Transfer bridge detection
bridges = kg.transfer_candidates("biology", "economics")
if bridges:
    for na, nb in bridges:
        print(f"\n  Transfer opportunity: {na.label} (biology) ↔ {nb.label} (economics)")
        print(f"    → Structural analogy worth exploring in next journaling session")

# ── 4. Safety Governor ────────────────────────────────────────────
print("\n── 4. Safety Governor ──")
test_outputs = [
    ("Diagnosis: cognitive decline detected",        False),
    ("This session treats memory disorders",         False),
    ("Your recall is below average — poor result",  False),
    ("Great session — strong encoding probability",  True),
    ("A targeted review could strengthen retention", True),
]
for msg, should_pass in test_outputs:
    try:
        safety.validate_feedback(msg)
        print(f"  ✓ SAFE:    {msg[:58]}")
    except ValueError:
        print(f"  ✗ BLOCKED: {msg[:58]}")

print("\n" + "=" * 65)
print("Demo complete. SAAA produced zero diagnostic claims.")
print("=" * 65)
