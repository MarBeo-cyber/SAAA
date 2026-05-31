from saaa.core.state import LearningState


class AdaptiveFeedbackEngine:
    """Generate safe, non-medical learning feedback."""

    def recommend(self, state: LearningState) -> list[str]:
        if state.label == "overloaded":
            return [
                "Stop the session for now.",
                "Take a 10-minute break.",
                "Resume with a short active recall exercise, not new material.",
            ]

        if state.label == "fatigued":
            return [
                "Take a 5-minute break.",
                "Use breathing guidance before continuing.",
                "Switch from reading to active recall.",
            ]

        if state.label == "productive":
            return [
                "Continue learning.",
                "Schedule a recall check in 1 hour.",
                "Mark this time window as potentially effective.",
            ]

        return [
            "Continue with a shorter block.",
            "Prefer active recall over passive reading.",
        ]
