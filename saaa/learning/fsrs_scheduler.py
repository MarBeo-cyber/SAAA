"""
SAAA — FSRS-based Spaced Repetition Scheduler

Implements Free Spaced Repetition Scheduler (FSRS) with individual
calibration on top of the base algorithm.

Reference: Ye et al. (2024) "A Stochastic Shortest Path Algorithm
for Optimizing Spaced Repetition"
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import IntEnum
from typing import Optional
import math


class Rating(IntEnum):
    AGAIN = 1   # complete blackout
    HARD  = 2   # significant difficulty
    GOOD  = 3   # correct with effort
    EASY  = 4   # correct, trivial


@dataclass
class CardState:
    """State of a single study item (flashcard, concept, procedure)."""
    item_id: str
    topic: str
    stability: float = 1.0          # S: how long memory lasts (days)
    difficulty: float = 5.0         # D: item difficulty [1–10]
    retrievability: float = 1.0     # R: current recall probability
    reviews: int = 0
    last_review: Optional[datetime] = None
    next_review: Optional[datetime] = None
    lapsed: bool = False

    # Individual calibration
    user_ease_modifier: float = 1.0  # personal difficulty adjustment
    time_of_day_modifier: float = 1.0  # peak-hour adjustment

    @property
    def days_since_review(self) -> float:
        if self.last_review is None:
            return 0.0
        return (datetime.utcnow() - self.last_review).total_seconds() / 86400

    @property
    def current_retrievability(self) -> float:
        """R(t) = e^(-t/S) — exponential decay model."""
        if self.stability <= 0:
            return 0.0
        return math.exp(-self.days_since_review / self.stability)

    def is_due(self) -> bool:
        if self.next_review is None:
            return True
        return datetime.utcnow() >= self.next_review


class FSRSScheduler:
    """
    FSRS scheduler with individual calibration.

    Base algorithm from Ye et al. (2024), extended with:
    - per-user difficulty modifier
    - time-of-day performance modifier
    - topic-category calibration
    """

    # FSRS default weights (w0–w17)
    DEFAULT_WEIGHTS = [
        0.4072, 1.1829, 3.1262, 15.4722,
        7.2102, 0.5316, 1.0651, 0.0589,
        1.4576, 0.1549, 1.0147, 1.9306,
        0.1115, 0.2900, 2.2700, 0.1550,
        2.9898, 0.5100,
    ]

    def __init__(
        self,
        request_retention: float = 0.90,
        weights: Optional[list[float]] = None,
    ):
        self.request_retention = request_retention
        self.w = weights or self.DEFAULT_WEIGHTS

    def _init_stability(self, rating: Rating) -> float:
        """Initial stability after first review."""
        return self.w[rating - 1]

    def _init_difficulty(self, rating: Rating) -> float:
        """Initial difficulty estimate."""
        return self.w[4] - (rating - 3) * self.w[5]

    def _next_interval(self, stability: float) -> int:
        """Compute next review interval in days for target retention."""
        interval = (stability / self.w[17]) * (
            math.pow(self.request_retention, 1 / self.w[16]) - 1
        )
        return max(1, round(interval))

    def _update_stability(
        self,
        state: CardState,
        rating: Rating,
        retrievability: float,
    ) -> float:
        """Update stability after a review."""
        if rating == Rating.AGAIN:
            # Lapse: stability decreases
            return (
                self.w[11] *
                math.pow(state.difficulty, -self.w[12]) *
                (math.pow(state.stability + 1, self.w[13]) - 1) *
                math.exp(self.w[14] * (1 - retrievability))
            )
        # Recall: stability increases
        hard_penalty = self.w[15] if rating == Rating.HARD else 1.0
        easy_bonus   = self.w[16] if rating == Rating.EASY  else 1.0
        return (
            state.stability *
            (math.exp(self.w[8]) *
             (11 - state.difficulty) *
             math.pow(state.stability, -self.w[9]) *
             (math.exp(self.w[10] * (1 - retrievability)) - 1) *
             hard_penalty * easy_bonus + 1)
        )

    def _update_difficulty(self, state: CardState, rating: Rating) -> float:
        mean_reversion = self.w[7] * (self.w[4] - state.difficulty)
        delta = -self.w[6] * (rating - 3)
        return max(1.0, min(10.0, state.difficulty + mean_reversion + delta))

    def review(self, state: CardState, rating: Rating) -> CardState:
        """Process a review and update card state."""
        now = datetime.utcnow()
        r = state.current_retrievability

        if state.reviews == 0:
            # First review
            new_stability   = self._init_stability(rating)
            new_difficulty  = self._init_difficulty(rating)
        else:
            new_stability   = self._update_stability(state, rating, r)
            new_difficulty  = self._update_difficulty(state, rating)

        # Apply individual modifiers
        effective_stability = (
            new_stability
            * state.user_ease_modifier
            * state.time_of_day_modifier
        )

        interval_days = self._next_interval(effective_stability)

        state.stability     = new_stability
        state.difficulty    = new_difficulty
        state.retrievability = r
        state.reviews      += 1
        state.last_review   = now
        state.next_review   = now + timedelta(days=interval_days)
        state.lapsed        = (rating == Rating.AGAIN)

        return state

    def get_due_items(self, states: list[CardState]) -> list[CardState]:
        """Return items due for review, sorted by urgency."""
        due = [s for s in states if s.is_due()]
        # Sort: lapsed first, then by lowest retrievability
        return sorted(due, key=lambda s: (not s.lapsed, s.current_retrievability))

    def retention_summary(self, states: list[CardState]) -> dict:
        """Summary statistics for a set of items."""
        if not states:
            return {}
        retrievabilities = [s.current_retrievability for s in states]
        return {
            "total_items": len(states),
            "due_now": sum(1 for s in states if s.is_due()),
            "mean_retention": sum(retrievabilities) / len(retrievabilities),
            "at_risk": sum(1 for r in retrievabilities if r < 0.7),
            "mature": sum(1 for s in states if s.stability > 21),
        }
