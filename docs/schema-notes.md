# Schema Notes

`llm-ir.v0` is intentionally small. It is a starting point for discussion, not a claim that human meaning can be fully captured in JSON.

## Top-Level Areas

- `source`: metadata about the original text.
- `intent`: the communicative act as a language-neutral concept id.
- `meaning`: semantic frames plus optional language-tagged glosses.
- `affect`: emotion and intensity.
- `style`: tone, register, formality, and rhetorical shape.
- `culture`: idioms, references, and localization notes.
- `privacy`: source-language markers and requested transforms.
- `targets`: generation preferences for target audiences.

## Language Neutrality

Protocol keys are written in English because JSON APIs need stable field names, but semantic values should not be English-only strings.

LLM-IR v0 uses two patterns to avoid English-first meaning:

- stable concept ids, such as `affect:frustration` or `act:express_reaction`
- `glosses`, a map of BCP 47 language tags to human-readable explanations

No gloss language is canonical. A Chinese source can carry a Chinese gloss first, an English gloss for debugging, and later Japanese or Arabic glosses without changing the underlying concept id.

Example:

```json
{
  "id": "affect:frustration",
  "glosses": {
    "zh-CN": "无语/受不了",
    "en-US": "frustration"
  }
}
```

This keeps the IR inspectable without making English the hidden intermediate language.

## Versioning

Schema identifiers use `llm-ir.vN`.

Breaking changes increment the schema version. Additive fields should be preferred while the protocol is experimental.
