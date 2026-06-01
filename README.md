# SAAA — Sapient Autopoietic Adaptive Agent

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Research Prototype](https://img.shields.io/badge/status-research%20prototype-orange.svg)]()

> *SAAA does not store what the user learns. SAAA learns how the user learns.*

SAAA is a personal AI-assisted cognitive learning system that builds an individual learning topology — how this specific user learns, when they learn best, and how memory consolidates — and uses it to optimise every future session.

---

## Conceptual Genealogy

| Project | Core Function | Biological Analogy |
|---|---|---|
| WAAA | Weak autopoietic perception | Sensory reflex |
| MAAA | Metacognitive embodied cognition in emergency | Acute stress response |
| PAAA | Personal neurofunctional continuity | Homeostasis / immune system |
| **SAAA** | **Sapient learning consolidation** | **Myelination / synaptic plasticity** |

*The WAAA → MAAA → PAAA → SAAA progression constitutes an **artificial ontogenesis**: development by stages structurally analogous to biological cognitive maturation.*

---

## Six-Layer Architecture

```
L1  Cognitive Sensing         ← keystroke dynamics, response latency, eye-tracking (opt.)
L2  Learning State Estimation ← attention, fatigue, encoding probability, overload risk
L3  Adaptive Content & Rhythm ← spaced repetition, interleaving, desirable difficulties
L4  Multimodal Feedback       ← audio cues, breathing guidance, recall prompts
L5  Memory Consolidation      ← FSRS scheduler, personal forgetting curve, knowledge graph
L6  Sapient Synthesis         ← transfer bridge, metacognitive journaling, topology visualisation
```

Layer 6 — Sapient Synthesis — is what distinguishes SAAA from a sophisticated spaced repetition system. It connects domains, detects transfer opportunities, and facilitates structured reflection on the learning process itself.

---

## Core Principle

```
study session  →  cognitive sensing  →  learning state estimation
       ↓
adaptive feedback  →  recall scheduling  →  consolidation tracking
       ↓
knowledge graph update  →  sapient synthesis  →  personal learning model
       ↑_______________________________________________|
```

The cycle closes on itself: consolidation feeds the personal model that optimises the next session.

---

## What SAAA Does

- Estimates attention, fatigue and encoding probability in real time
- Schedules active recall at the individually optimal moment (FSRS + personal calibration)
- Builds a personal knowledge graph: how concepts are connected in this user's mind
- Detects transfer opportunities between different domains
- Facilitates metacognitive journaling via Socratic AI dialogue
- Adapts session rhythm to neurofunctional profile (integrates with PAAA)
- Exports a longitudinal learning biography

---

## Quick Start

```bash
git clone https://github.com/MarBeo-cyber/SAAA.git
cd SAAA
pip install -r requirements.txt
pip install -e .
python examples/run_demo.py
```

---

## Safety Boundaries

| Limit | Reason |
|---|---|
| No cognitive diagnosis | Not a medical device |
| No active neurostimulation (default) | Requires explicit validated override |
| No performance pressure language | Risk of learning anxiety |
| Full data deletion on request | GDPR Article 17 |

---

## Integration with PAAA and MAAA

**PAAA → SAAA:** SAAA accesses the PAAA neurofunctional profile (HRV, sleep, cognitive state) to propose study sessions when the profile indicates optimal recovery, and light recall sessions when it indicates fatigue.

**SAAA → MAAA:** For emergency operations professionals, SAAA feeds updated procedural knowledge into the MAAA knowledge base. MAAA can recall recently consolidated protocols during a crisis.

---

## Project Structure

```
SAAA/
├── saaa/
│   ├── core/state.py           LearningState dataclass
│   ├── feedback/               AdaptiveFeedbackEngine
│   ├── learning/               LearningStateEngine (FSRS + individual calibration)
│   ├── memory/                 ConsolidationScheduler, KnowledgeGraph
│   └── safety/governor.py      SafetyGovernor
├── docs/
│   ├── ARCHITECTURE.md         Six-layer technical architecture
│   ├── PHILOSOPHY.md           Sapientia and autopoietic learning
│   ├── ROADMAP.md              Development milestones
│   ├── SAFETY_AND_REGULATORY.md
│   └── references.md           Scientific foundations
├── config/default.yaml
└── tests/
```

---

## Citation

```bibtex
@software{saaa2025,
  title  = {SAAA: Sapient Autopoietic Adaptive Agent},
  author = {Beozzi, Marco Giuseppe},
  year   = {2025},
  url    = {https://github.com/MarBeo-cyber/SAAA},
  note   = {Part of the WAAA → MAAA → PAAA → SAAA artificial ontogenesis}
}
```
