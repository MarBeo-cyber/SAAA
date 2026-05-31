class SafetyGovernor:
    """Safety checks for SAAA feedback and stimulation modules."""

    def __init__(self, active_neurostimulation_enabled: bool = False):
        self.active_neurostimulation_enabled = active_neurostimulation_enabled

    def validate_feedback(self, message: str) -> str:
        forbidden = [
            "diagnosis",
            "treats",
            "cures",
            "memory disorder",
            "neurological disease",
        ]
        lower = message.lower()
        if any(term in lower for term in forbidden):
            raise ValueError("Unsafe or medicalized claim detected.")
        return message

    def stimulation_allowed(self) -> bool:
        return bool(self.active_neurostimulation_enabled)
