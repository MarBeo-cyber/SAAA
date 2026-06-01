# SAAA — Technical Architecture Reference

## Six-Layer Architecture

SAAA extends the five-layer pattern of MAAA/PAAA with a sixth layer — Sapient Synthesis — that produces the distinctive capability of the system.

---

### L1 — Cognitive Sensing

Non-intrusive acquisition of behavioural signals during the study session:

| Signal | Method | Sensitivity |
|---|---|---|
| Response latency | Recall test timing | High |
| Keystroke dynamics | Inter-key interval, error rate | Medium |
| Reading speed | Page/scroll tracking | Medium |
| Self-reported fatigue | Calibrated 1–5 scale | Low |
| HRV (opt.) | Smartwatch | High |
| Eye tracking (opt.) | Tobii / consumer device | High |

---

### L2 — Learning State Estimation

```python
# Composite state estimation (MVP heuristic — replace with learned model in v2)
attention  = 1.0 - (0.45 * latency_penalty + 0.35 * fatigue + 0.20 * duration_penalty)
fatigue    = 0.50 * self_fatigue + 0.30 * duration_penalty + 0.20 * latency_penalty
enc_prob   = 0.50 * attention + 0.35 * recall_score + 0.15 * (1.0 - fatigue)
overload   = 0.60 * fatigue + 0.40 * (1.0 - attention)
```

State labels: `productive` | `neutral` | `fatigued` | `overloaded`

---

### L3 — Adaptive Content & Rhythm

**FSRS — Free Spaced Repetition Scheduler (default algorithm):**

Four-parameter memory model per item:
- **Stability (S):** how long the memory lasts
- **Difficulty (D):** how hard this concept is for this user
- **Retrievability (R):** probability of recall at a given moment
- **Interval (I):** optimal days until next review

**Individual calibrations on top of FSRS:**

| Factor | Effect |
|---|---|
| Time-of-day | Schedules intensive sessions at user's peak performance window |
| Learning modality | Increases preferred modality; challenges non-preferred |
| Semantic interference | Increases interleaving for confused concept pairs |
| Session length | Adapts to user's optimal block duration |

---

### L4 — Multimodal Feedback

Output modalities (all configurable):

- **Audio cues** — rhythm, pacing, break signals
- **Bone conduction** (optional) — non-intrusive during reading
- **Breathing guidance** — pre-session protocol for optimal cognitive state
- **Visual micro-feedback** — subtle progress indicators
- **Recall prompts** — timed to optimal retrievability window

**Feedback calibration principle:** minimum intervention for maximum effect. No interruption of flow state.

---

### L5 — Memory Consolidation Tracking

**Memory model levels:**

| Level | Type | Content | Retention |
|---|---|---|---|
| M1 Working | Current session | Items studied, recall score, state | Session only |
| M2 Item | Per concept | Forgetting curve, difficulty, recall history | Unlimited |
| M3 Topic | Semantic clusters | Mastery score, internal coherence | Unlimited |
| M4 Knowledge Graph | Semantic network | Connections, distances, transfer bridges | Unlimited |
| M5 Learning Biography | Longitudinal profile | Learning style, excellence patterns, fragility | Unlimited + export |

**Personal forgetting curve:**  
SAAA calibrates a separate forgetting curve per user and per concept category. Visual learner vs abstract thinker profiles produce structurally different curves and different optimal intervals.

---

### L6 — Sapient Synthesis

The layer that transforms information accumulation into structured wisdom:

**Metacognitive Journaling**  
Socratic dialogue via local LLM. The system asks — does not answer.  
Example: *"You consistently recall this concept better when you connect it to a personal example. Can you find one for [concept X]?"*

**Transfer Bridge Detection**  
Automatic semantic similarity detection between concepts from different domains.  
Example: *"The negative feedback loop in physiology and the mean-reversion concept in finance have structural similarities. Worth exploring?"*

**Learning Topology Visualisation**  
Interactive map of mastery areas, fragility zones, cross-domain connections, preferred cognitive pathways. Tool for metacognition: see how you learn, not just what you know.

**Knowledge Gap Detection**  
Identifies isolated or weakly-connected concepts that may indicate fragile understanding (learned by rote without semantic integration).

---

## Technology Stack

| Domain | Tools |
|---|---|
| Spaced Repetition | FSRS (py-fsrs), SM-18 reference |
| Learning State ML | scikit-learn, River (online ML), tsfresh |
| NLP / Embeddings | sentence-transformers, spaCy |
| Knowledge Graph | NetworkX (embedded), Neo4j (enterprise) |
| LLM (Synthesis) | LLaMA 3.2 3B quantised (local) / API opt-in |
| VectorDB | LanceDB embedded / Qdrant server |
| UI | Flutter (mobile), React (web) |
| Storage | SQLCipher + AES-256 filesystem |

---

## Processing Pipeline

```
Pre-session:  neurofunctional profile (PAAA) → recommended duration, modality, topics
        ↓
Session:      sensing → state estimation → micro-adaptations → recall prompts
        ↓
Post-session: recall score → forgetting curve update → next review scheduling
        ↓
Async recall: spaced micro-review at optimal retrievability window
        ↓
Monthly:      knowledge graph synthesis → metacognitive journaling → topology update
```

---

## Non-Functional Requirements

| Requirement | Target |
|---|---|
| In-session feedback latency | <500ms |
| Offline operability | 100% core functions |
| Storage (5 years) | <500 MB |
| Availability | 99.5% |
| GDPR compliance | Consent, portability, erasure |
