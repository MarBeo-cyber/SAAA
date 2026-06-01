"""SAAA — Sapient Autopoietic Adaptive Agent.

An AI-assisted cognitive learning system that builds a personal
learning topology and uses it to optimise memory consolidation.

NOT a diagnostic device. Does not claim memory enhancement.
Supports the conditions under which learning becomes stable.

The SAAA is the fourth agent in the artificial ontogenesis:
WAAA (perception) → MAAA (emergency cognition) →
PAAA (neurofunctional continuity) → SAAA (sapient consolidation)
"""
__version__ = "0.2.0"
__author__ = "Marco Giuseppe Beozzi"
__license__ = "MIT"

from saaa.core.state import LearningState
from saaa.learning.state_engine import LearningStateEngine
from saaa.learning.fsrs_scheduler import FSRSScheduler, CardState, Rating
from saaa.feedback.adaptive_feedback import AdaptiveFeedbackEngine
from saaa.memory.consolidation import ConsolidationScheduler, StudyItem
from saaa.memory.knowledge_graph import KnowledgeGraph, ConceptNode, ConceptEdge
from saaa.safety.governor import SafetyGovernor

__all__ = [
    "LearningState",
    "LearningStateEngine",
    "FSRSScheduler", "CardState", "Rating",
    "AdaptiveFeedbackEngine",
    "ConsolidationScheduler", "StudyItem",
    "KnowledgeGraph", "ConceptNode", "ConceptEdge",
    "SafetyGovernor",
]
