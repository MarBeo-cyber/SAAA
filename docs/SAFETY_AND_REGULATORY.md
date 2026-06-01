# Safety and Regulatory Notes — SAAA

## What SAAA Is

SAAA is a **research and educational prototype** for AI-assisted learning support and memory consolidation optimisation.

It is a **personal cognitive augmentation tool**. It supports the conditions under which learning becomes more stable: attention, rhythm, recall, consolidation, metacognitive awareness.

---

## What SAAA Is Not

SAAA **must not** be positioned or marketed as:

- a cognitive enhancement medical device
- a treatment for cognitive impairment
- a neurological therapy system
- a substitute for educational professionals
- a clinical memory augmentation device
- a substitute for medical evaluation of cognitive conditions

---

## Permitted Positioning

SAAA may be described as:

- AI-assisted learning support framework
- personal spaced repetition and recall optimisation system
- metacognitive awareness support tool
- memory consolidation research prototype
- individual learning topology explorer

---

## Safety Governor — Hard Limits

| Limit | Implementation |
|---|---|
| No diagnostic claims | NLP filter on all outputs |
| No active neurostimulation (default) | `active_neurostimulation_enabled: false` hardcoded |
| No performance pressure framing | Outputs always framed as opportunities, never deficits |
| Max session duration enforced | Default 45 min; configurable within safe range |
| No claims of memory disorder treatment | Forbidden terms filter |

**Forbidden terms (partial list):**  
`diagnosis`, `treats`, `cures`, `memory disorder`, `neurological disease`, `cognitive impairment treated`, `clinical enhancement`

---

## Neurostimulation Safety

Active neurostimulation (including bone conduction beyond audio cueing) requires:

1. Explicit user consent with documented understanding of research status
2. Protocol validation by qualified researcher
3. Override flag set in config (`require_user_override: true`)
4. Session logging with stimulation parameters

Passive audio cueing (standard headphones or bone conduction at normal audio levels) does not require override.

---

## Data Governance

- All learning data stored on-device (encrypted)
- No content data (what the user studies) transmitted without explicit consent
- Anonymised behavioural signals for algorithm improvement: opt-in only
- GDPR Article 17 (right to erasure): full delete cascade implemented
- User owns their Knowledge Graph and Learning Biography — exportable at any time
