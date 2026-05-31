# Safety and Regulatory Notes

SAAA is a research and educational prototype.

It is not a medical device.

It must not be marketed as:

- a treatment
- a diagnostic system
- a cognitive disorder therapy
- a guaranteed memory enhancement device
- a neurostimulation therapy

## Stimulation Safety

The initial MVP should use only low-risk feedback:

- audio
- bone-conduction audio
- haptic cues
- visual cues
- breathing guidance
- study rhythm adaptation

Any active electrical, magnetic or optical stimulation must be considered experimental and must require:

- professional supervision
- safety limits
- informed consent
- device certification
- ethical review where applicable

## AI Safety

SAAA should never infer medical conditions.

Allowed:

```text
Your recall score was lower than your personal baseline.
```

Not allowed:

```text
You may have a memory disorder.
```

Allowed:

```text
This learning session shows signs of fatigue.
```

Not allowed:

```text
Your brain is not consolidating properly.
```

## Human Override

The user must always be able to:

- pause
- stop
- disable feedback
- delete data
- export data
- opt out of stimulation modules
