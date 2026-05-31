from saaa.learning.state_engine import LearningStateEngine
from saaa.feedback.adaptive_feedback import AdaptiveFeedbackEngine


engine = LearningStateEngine()
feedback = AdaptiveFeedbackEngine()

state = engine.estimate(
    response_latency_s=4.2,
    recall_score=0.68,
    self_reported_fatigue=0.35,
    session_minutes=25,
)

print("Learning state:", state.label)
print("Attention:", round(state.attention, 2))
print("Fatigue:", round(state.fatigue, 2))
print("Recommendations:")
for item in feedback.recommend(state):
    print("-", item)
