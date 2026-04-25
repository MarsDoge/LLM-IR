# LLM-IR

**LLM-IR is an open intermediate representation for multilingual, privacy-aware human communication.**

It is not another translation model. LLM-IR defines a structured semantic layer between source language and target expression:

```text
source text -> meaning IR -> transforms -> target expression
```

The goal is to make language conversion more explainable, controllable, and fair across languages, cultures, and platforms.

## Why

Global communication is becoming easier, but language still leaks identity and creates asymmetry.

Most translation systems convert directly from one language to another. This works for literal content, but it often preserves translation artifacts, source-language markers, regional hints, and cultural assumptions.

LLM-IR proposes a different path:

- capture meaning before wording
- separate facts from tone, style, intent, and cultural markers
- allow privacy transforms before target-language generation
- provide a common protocol for LLMs, apps, and social platforms
- avoid treating English as the hidden intermediate language

## Design Analogy

LLVM provides a common intermediate representation for programming languages and machine targets.

LLM-IR aims to provide a common intermediate representation for human communication:

```text
Chinese / English / Japanese / Arabic / Spanish
        -> LLM-IR
        -> Chinese / English / Japanese / Arabic / Spanish
```

## Current Scope

This repository starts with a minimal protocol draft:

- JSON Schema for `llm-ir.v0`
- example IR documents
- a tiny CLI prototype
- project docs for roadmap and design principles
- safety notes for privacy-aware transforms

The first version is intentionally small. The schema should be easy to inspect, extend, and implement in different languages.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

llm-ir encode "这事儿也太离谱了吧，真绷不住了。"
llm-ir decode examples/zh_slang.llm-ir.json --target en-US
```

The current CLI is a deterministic prototype. It does not call an LLM yet.

## Example

Source:

```text
这事儿也太离谱了吧，真绷不住了。
```

LLM-IR:

```json
{
  "schema": "llm-ir.v0",
  "source": {
    "text": "这事儿也太离谱了吧，真绷不住了。",
    "language": "zh-CN"
  },
  "intent": {
    "id": "act:express_reaction",
    "glosses": {
      "zh-CN": "表达强烈反应",
      "en-US": "express a strong reaction"
    }
  },
  "meaning": {
    "frames": [
      {
        "id": "m1",
        "type": "evaluation",
        "predicate": {
          "id": "eval:absurd",
          "glosses": {
            "zh-CN": "离谱/荒谬",
            "en-US": "absurd"
          }
        },
        "glosses": {
          "zh-CN": "说话者强烈觉得这件事很离谱。",
          "en-US": "The speaker strongly feels that the situation is absurd."
        }
      }
    ]
  },
  "affect": {
    "labels": [
      {
        "id": "affect:disbelief",
        "glosses": {
          "zh-CN": "难以置信",
          "en-US": "disbelief"
        }
      },
      {
        "id": "affect:frustration",
        "glosses": {
          "zh-CN": "无语/受不了",
          "en-US": "frustration"
        }
      }
    ],
    "intensity": 0.85
  }
}
```

Target expression:

```text
This is honestly insane. I can't even.
```

## Repository Layout

```text
schema/              JSON Schema definitions
examples/            sample LLM-IR documents
docs/                design notes and roadmap
src/llm_ir/          Python CLI prototype
tests/               lightweight tests
```

## Status

Experimental. The project is at the protocol sketch stage.

## Safety

See [docs/safety.md](docs/safety.md). The privacy layer is intended to reduce accidental source-language leakage, not to enable impersonation or deceptive identity masking.

## License

MIT
