# Vision

LLM-IR is a protocol for converting natural-language expression into a structured, language-neutral semantic representation.

The project is inspired by compiler intermediate representations. Instead of translating directly from one language to another, LLM-IR encourages systems to separate the communication pipeline into stages:

```text
parse -> represent -> transform -> generate
```

## Non-Goals

LLM-IR is not:

- a replacement for translation models
- a universal ontology of all human meaning
- a tool for hiding accountability or impersonating people
- a single canonical style for all speakers

## Core Questions

- What did the speaker intend?
- What factual claims are present?
- What emotions, tone, and register are present?
- Which cultural or source-language markers are meaningful?
- Which markers should be preserved, adapted, or neutralized?
- What should the target audience receive?

## Privacy-Aware Communication

Translation can leak source-language identity through literal phrasing, idioms, grammar, punctuation habits, and cultural references.

LLM-IR makes those markers explicit so applications can choose a policy:

- preserve them when they are part of identity or authorship
- adapt them when target readers need natural comprehension
- neutralize them when the user wants less source-language exposure

The default project stance is not total anonymization. It is explicit, user-controlled transformation.
