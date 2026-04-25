# Contributing

LLM-IR is at the protocol design stage. Useful contributions include:

- schema improvements
- examples from different languages and cultures
- privacy transform proposals
- evaluation cases for meaning preservation and source-language marker removal
- adapters for LLM providers and applications

## Principles

- Keep the IR inspectable by humans.
- Separate meaning from wording.
- Preserve user intent before optimizing style.
- Treat privacy transforms as explicit policy, not hidden behavior.
- Avoid features that make deception or impersonation easier by default.

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python -m pytest
```
