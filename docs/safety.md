# Safety and Misuse Boundaries

LLM-IR includes privacy-aware transforms because translation can reveal source-language identity.

That same capability can be misused if it is treated as identity laundering. The project should make privacy policy explicit and auditable.

## Supported Use Cases

- helping users communicate across language barriers
- reducing accidental source-language leakage
- adapting idioms for target audiences
- making translation choices inspectable
- improving accessibility and multilingual inclusion

## Unsupported Use Cases

- impersonating a person or community
- hiding coordinated manipulation
- generating deceptive political or financial messages
- removing accountability from harmful speech
- bypassing platform integrity systems

## Design Rules

- Privacy transforms should be named explicitly.
- Applications should expose whether source markers were preserved, adapted, or neutralized.
- High-risk domains should prefer conservative transforms.
- The IR should keep provenance metadata available to trusted systems when appropriate.
- Defaults should optimize for clarity and user control, not deception.
