from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LlmIrDocument:
    source_text: str
    source_language: Optional[str] = None
    intent: str = "communicate"
    summary: Optional[str] = None
    emotion: list[str] = field(default_factory=list)
    intensity: Optional[float] = None
    register: Optional[str] = None
    tone: Optional[str] = None
    source_language_markers: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        document = {
            "schema": "llm-ir.v0",
            "source": {
                "text": self.source_text,
            },
            "intent": self.intent,
            "meaning": {
                "summary": self.summary or self.source_text,
            },
        }

        if self.source_language:
            document["source"]["language"] = self.source_language

        if self.emotion or self.intensity is not None:
            affect = {}
            if self.emotion:
                affect["emotion"] = self.emotion
            if self.intensity is not None:
                affect["intensity"] = self.intensity
            document["affect"] = affect

        if self.register or self.tone:
            style = {}
            if self.register:
                style["register"] = self.register
            if self.tone:
                style["tone"] = self.tone
            document["style"] = style

        if self.source_language_markers:
            document["privacy"] = {
                "source_language_markers": self.source_language_markers,
                "recommended_transform": "neutralize_source_language_markers",
            }

        return document


def encode_text(text: str, source_language: Optional[str] = None) -> dict:
    """Create a conservative prototype IR document without calling an LLM."""
    hints = _detect_simple_hints(text)
    document = LlmIrDocument(
        source_text=text,
        source_language=source_language,
        intent=hints.get("intent", "communicate"),
        summary=hints.get("summary"),
        emotion=hints.get("emotion", []),
        intensity=hints.get("intensity"),
        register=hints.get("register"),
        tone=hints.get("tone"),
        source_language_markers=hints.get("source_language_markers", []),
    )
    return document.to_dict()


def decode_document(document: dict, target_language: str) -> str:
    """Render a rough target expression from an IR document.

    This is deliberately simple. Real decoding should use a model adapter
    with schema-aware prompts and evaluation.
    """
    summary = document.get("meaning", {}).get("summary", "")
    intent = document.get("intent", "communicate")
    emotion = document.get("affect", {}).get("emotion", [])
    tone = document.get("style", {}).get("tone", "")

    if target_language.lower().startswith("en"):
        if intent == "express_reaction" and {"disbelief", "frustration"}.issubset(set(emotion)):
            return "This is honestly insane. I can't even."
        return summary

    if target_language.lower().startswith("zh"):
        if intent == "disagree" and "respectful" in tone:
            return f"我尊重这个提案，但不同意其中的判断：{summary}"
        return summary

    return summary


def _detect_simple_hints(text: str) -> dict:
    if "离谱" in text or "绷不住" in text:
        return {
            "intent": "express_reaction",
            "summary": "The speaker strongly feels that the situation is absurd.",
            "emotion": ["disbelief", "frustration"],
            "intensity": 0.85,
            "register": "casual",
            "tone": "internet_slang",
            "source_language_markers": ["Chinese internet slang"],
        }
    return {
        "summary": text,
    }
