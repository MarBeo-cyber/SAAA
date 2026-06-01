"""
SAAA — Safety Governor

Enforces hard limits on all SAAA outputs.
No diagnostic claims. No active neurostimulation without explicit override.
No performance pressure framing. No medicalized language.
"""

from dataclasses import dataclass, field
from typing import Optional
import re


FORBIDDEN_TERMS = [
    "diagnosis",
    "treats",
    "cures",
    "memory disorder",
    "neurological disease",
    "neurological disorder",
    "cognitive impairment",
    "cognitive disorder",
    "enhances memory",
    "memory enhancement",
    "clinical",
    "medical treatment",
    "therapeutic",
]

PRESSURE_TERMS = [
    "you failed",
    "poor performance",
    "below average",
    "you are worse",
    "declining",
    "deteriorating",
]


@dataclass
class SafetyCheckResult:
    passed: bool
    original_message: str
    sanitised_message: Optional[str] = None
    violations: list[str] = field(default_factory=list)


class SafetyGovernor:
    """
    Safety Governor for SAAA.

    Hard limits (not user-configurable):
    - No diagnostic or medicalized claims
    - No active neurostimulation without validated override
    - No performance pressure or deficit framing
    - Max session duration enforced
    - Full deletion on request (GDPR Art. 17)
    """

    MAX_SESSION_MINUTES = 90  # absolute ceiling

    def __init__(
        self,
        active_neurostimulation_enabled: bool = False,
        max_session_minutes: int = 45,
        strict_mode: bool = True,
    ):
        self.active_neurostimulation_enabled = active_neurostimulation_enabled
        self.max_session_minutes = min(max_session_minutes, self.MAX_SESSION_MINUTES)
        self.strict_mode = strict_mode
        self._forbidden = [t.lower() for t in FORBIDDEN_TERMS]
        self._pressure = [t.lower() for t in PRESSURE_TERMS]

    # ── Output validation ─────────────────────────────────────────

    def validate_feedback(self, message: str) -> str:
        """Validate a feedback message. Raises ValueError if unsafe."""
        result = self.check(message)
        if not result.passed:
            if self.strict_mode:
                raise ValueError(
                    f"SAAA Safety violation — forbidden terms: {result.violations}. "
                    f"All feedback must be framed as opportunities, never deficits or diagnoses."
                )
            return result.sanitised_message or message
        return message

    def check(self, message: str) -> SafetyCheckResult:
        """Check message for policy violations."""
        lower = message.lower()
        violations = [t for t in self._forbidden if t in lower]
        violations += [t for t in self._pressure if t in lower]
        if not violations:
            return SafetyCheckResult(passed=True, original_message=message)
        sanitised = self._sanitise(message)
        return SafetyCheckResult(
            passed=False,
            original_message=message,
            sanitised_message=sanitised,
            violations=violations,
        )

    def _sanitise(self, message: str) -> str:
        """Replace forbidden terms with safe alternatives."""
        replacements = {
            "diagnosis": "observation",
            "treats": "supports",
            "cures": "supports",
            "clinical": "personal",
            "therapeutic": "supportive",
            "you failed": "this was challenging",
            "poor performance": "a session with room for growth",
            "below average": "an area to develop",
            "declining": "showing variation",
        }
        safe = message
        for term, replacement in replacements.items():
            safe = re.sub(re.escape(term), replacement, safe, flags=re.IGNORECASE)
        return safe

    # ── Stimulation safety ────────────────────────────────────────

    def stimulation_allowed(self) -> bool:
        """Active neurostimulation requires explicit validated override."""
        return bool(self.active_neurostimulation_enabled)

    def check_session_duration(self, minutes: int) -> tuple[bool, str]:
        """Check if session duration is within safe limits."""
        if minutes > self.max_session_minutes:
            return False, (
                f"Session duration ({minutes} min) exceeds configured limit "
                f"({self.max_session_minutes} min). "
                f"Taking a break supports consolidation."
            )
        return True, ""

    # ── Report validation ────────────────────────────────────────

    def validate_report(self, report: dict) -> dict:
        """Validate all string values in a report dictionary."""
        def check_value(v):
            if isinstance(v, str):
                return self.validate_feedback(v)
            if isinstance(v, dict):
                return {k: check_value(val) for k, val in v.items()}
            if isinstance(v, list):
                return [check_value(item) for item in v]
            return v
        return {k: check_value(v) for k, v in report.items()}

    # ── Opportunity framing ───────────────────────────────────────

    def frame_as_opportunity(self, observation: str, area: str) -> str:
        """
        Convert a deficit observation into an opportunity framing.
        SAAA never frames learning gaps as failures.
        """
        return (
            f"Your data shows {observation} in {area}. "
            f"This is a useful signal: it points to an area where "
            f"a targeted review session could strengthen your retention."
        )
