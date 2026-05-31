from dataclasses import dataclass
from datetime import datetime


@dataclass
class LearningState:
    timestamp: datetime
    attention: float
    fatigue: float
    encoding_probability: float
    recall_strength: float
    overload_risk: float

    @property
    def label(self) -> str:
        if self.overload_risk > 0.75:
            return "overloaded"
        if self.fatigue > 0.70:
            return "fatigued"
        if self.attention > 0.65 and self.encoding_probability > 0.60:
            return "productive"
        return "neutral"
