# SAAA Technical Architecture

## 1. Cognitive Sensing Layer

Inputs:

- study session duration
- response latency
- recall score
- error rate
- reading speed
- typing rhythm
- optional heart rate / HRV
- optional eye-tracking
- optional EEG consumer data
- optional smartwatch signals

## 2. Learning State Engine

Estimates:

- attention score
- fatigue score
- encoding probability
- recall strength
- consolidation window
- overload risk
- optimal break timing

Example state:

```json
{
  "attention": 0.74,
  "fatigue": 0.31,
  "encoding_probability": 0.68,
  "recall_strength": 0.52,
  "learning_state": "productive"
}
```

## 3. Adaptive Feedback Layer

Possible feedback:

- short audio cues
- bone-conduction rhythmic cueing
- breathing guidance
- light-based timing cues
- haptic prompts
- pause recommendation
- change of learning modality
- active recall prompt
- spaced repetition scheduling

## 4. Memory Consolidation Engine

Tracks:

- what was studied
- when it was studied
- recall quality
- forgetting curves
- best review interval
- modality effectiveness
- time-of-day effectiveness
- fatigue impact on retention

## 5. Personal Learning Topology

SAAA builds a map of the user’s learning profile:

```text
time → attention → modality → recall → retention → fatigue
```

This is the core long-term knowledge of the system.

## 6. Safety Governor

Prevents:

- excessive session duration
- overstimulation
- unsafe experimental stimulation
- overconfidence in AI interpretation
- pseudo-medical claims
- feedback loops that increase anxiety

## 7. Local AI Assistant

Supports:

- summarization
- question generation
- active recall cards
- session reflection
- metacognitive coaching
- learning plan adaptation
