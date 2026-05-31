from datetime import datetime
from saaa.core.state import LearningState


class LearningStateEngine:
    """Estimate cognitive learning state from simple behavioral signals.

    This is an MVP heuristic, not a clinical model.
    """

    def estimate(
        self,
        response_latency_s: float,
        recall_score: float,
        self_reported_fatigue: float,
        session_minutes: int,
    ) -> LearningState:
        latency_penalty = min(response_latency_s / 10.0, 1.0)
        duration_penalty = min(session_minutes / 60.0, 1.0)

        attention = max(0.0, min(1.0, 1.0 - (0.45 * latency_penalty + 0.35 * self_reported_fatigue + 0.20 * duration_penalty)))
        fatigue = max(0.0, min(1.0, 0.50 * self_reported_fatigue + 0.30 * duration_penalty + 0.20 * latency_penalty))
        encoding_probability = max(0.0, min(1.0, 0.50 * attention + 0.35 * recall_score + 0.15 * (1.0 - fatigue)))
        recall_strength = max(0.0, min(1.0, recall_score))
        overload_risk = max(0.0, min(1.0, 0.60 * fatigue + 0.40 * (1.0 - attention)))

        return LearningState(
            timestamp=datetime.utcnow(),
            attention=attention,
            fatigue=fatigue,
            encoding_probability=encoding_probability,
            recall_strength=recall_strength,
            overload_risk=overload_risk,
        )
