# Schema Notes

`llm-ir.v0` is intentionally small. It is a starting point for discussion, not a claim that human meaning can be fully captured in JSON.

## Top-Level Areas

- `source`: metadata about the original text.
- `intent`: the communicative act.
- `meaning`: facts, summary, and implied context.
- `affect`: emotion and intensity.
- `style`: tone, register, formality, and rhetorical shape.
- `culture`: idioms, references, and localization notes.
- `privacy`: source-language markers and requested transforms.
- `targets`: generation preferences for target audiences.

## Versioning

Schema identifiers use `llm-ir.vN`.

Breaking changes increment the schema version. Additive fields should be preferred while the protocol is experimental.
