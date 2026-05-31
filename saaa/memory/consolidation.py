from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class StudyItem:
    topic: str
    first_seen: datetime
    last_recall_score: float
    reviews: int = 0


class ConsolidationScheduler:
    """Simple spaced repetition scheduler."""

    intervals = [1, 8, 24, 72, 168]  # hours

    def next_review(self, item: StudyItem) -> datetime:
        idx = min(item.reviews, len(self.intervals) - 1)
        base = item.first_seen
        return base + timedelta(hours=self.intervals[idx])
