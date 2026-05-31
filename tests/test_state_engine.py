from saaa.learning.state_engine import LearningStateEngine


def test_state_engine_outputs_valid_range():
    engine = LearningStateEngine()
    state = engine.estimate(
        response_latency_s=3.0,
        recall_score=0.8,
        self_reported_fatigue=0.2,
        session_minutes=20,
    )
    assert 0.0 <= state.attention <= 1.0
    assert 0.0 <= state.fatigue <= 1.0
    assert state.label in {"productive", "neutral", "fatigued", "overloaded"}
