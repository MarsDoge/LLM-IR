from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LlmIrDocument:
    source_text: str
    source_language: Optional[str] = None
    intent_id: str = "act:communicate"
    meaning_glosses: dict[str, str] = field(default_factory=dict)
    affect_ids: list[str] = field(default_factory=list)
    intensity: Optional[float] = None
    register_id: Optional[str] = None
    tone_id: Optional[str] = None
    source_language_marker_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        document = {
            "schema": "llm-ir.v0",
            "source": {
                "text": self.source_text,
            },
            "intent": _concept(self.intent_id),
            "meaning": {
                "frames": [
                    {
                        "id": "m1",
                        "type": "utterance",
                        "predicate": _concept("meaning:communicated"),
                        "glosses": self.meaning_glosses or {"und": self.source_text},
                    }
                ],
                "glosses": self.meaning_glosses or {"und": self.source_text},
            },
        }

        if self.source_language:
            document["source"]["language"] = self.source_language

        if self.affect_ids or self.intensity is not None:
            affect = {}
            if self.affect_ids:
                affect["labels"] = [_concept(item) for item in self.affect_ids]
            if self.intensity is not None:
                affect["intensity"] = self.intensity
            document["affect"] = affect

        if self.register_id or self.tone_id:
            style = {}
            if self.register_id:
                style["register"] = _concept(self.register_id)
            if self.tone_id:
                style["tone"] = _concept(self.tone_id)
            document["style"] = style

        if self.source_language_marker_ids:
            document["privacy"] = {
                "source_language_markers": [_marker(item) for item in self.source_language_marker_ids],
                "recommended_transform": _concept("transform:neutralize_source_language_markers"),
            }

        return document


def encode_text(text: str, source_language: Optional[str] = None) -> dict:
    """Create a conservative prototype IR document without calling an LLM."""
    hints = _detect_simple_hints(text)
    document = LlmIrDocument(
        source_text=text,
        source_language=source_language,
        intent_id=hints.get("intent_id", "act:communicate"),
        meaning_glosses=hints.get("meaning_glosses", {"und": text}),
        affect_ids=hints.get("affect_ids", []),
        intensity=hints.get("intensity"),
        register_id=hints.get("register_id"),
        tone_id=hints.get("tone_id"),
        source_language_marker_ids=hints.get("source_language_marker_ids", []),
    )
    return document.to_dict()


def decode_document(document: dict, target_language: str) -> str:
    """Render a rough target expression from an IR document.

    This is deliberately simple. Real decoding should use a model adapter
    with schema-aware prompts and evaluation.
    """
    summary = _best_gloss(document.get("meaning", {}).get("glosses", {}), target_language)
    intent = _concept_id(document.get("intent", {}))
    affect_ids = {_concept_id(item) for item in document.get("affect", {}).get("labels", [])}
    tone = _concept_id(document.get("style", {}).get("tone", {}))

    if target_language.lower().startswith("en"):
        if intent == "act:express_reaction" and {"affect:disbelief", "affect:frustration"}.issubset(affect_ids):
            return "This is honestly insane. I can't even."
        return summary

    if target_language.lower().startswith("zh"):
        if intent == "act:disagree" and tone == "tone:respectful":
            return f"我尊重这个提案，但不同意其中的判断：{summary}"
        return summary

    return summary


def _detect_simple_hints(text: str) -> dict:
    if "离谱" in text or "绷不住" in text:
        return {
            "intent_id": "act:express_reaction",
            "meaning_glosses": {
                "zh-CN": "说话者强烈觉得这件事很离谱。",
                "en-US": "The speaker strongly feels that the situation is absurd.",
            },
            "affect_ids": ["affect:disbelief", "affect:frustration"],
            "intensity": 0.85,
            "register_id": "register:casual",
            "tone_id": "tone:internet_slang",
            "source_language_marker_ids": ["marker:source_language:zh_internet_slang"],
        }
    return {
        "meaning_glosses": {"und": text},
    }


def _concept(concept_id: str) -> dict:
    glosses = {
        "act:communicate": {"zh-CN": "交流", "en-US": "communicate"},
        "act:express_reaction": {"zh-CN": "表达强烈反应", "en-US": "express a strong reaction"},
        "meaning:communicated": {"zh-CN": "表达的含义", "en-US": "communicated meaning"},
        "affect:disbelief": {"zh-CN": "难以置信", "en-US": "disbelief"},
        "affect:frustration": {"zh-CN": "无语/受不了", "en-US": "frustration"},
        "register:casual": {"zh-CN": "口语", "en-US": "casual"},
        "tone:internet_slang": {"zh-CN": "网络语气", "en-US": "internet slang"},
        "transform:neutralize_source_language_markers": {
            "zh-CN": "弱化源语言痕迹",
            "en-US": "neutralize source-language markers",
        },
    }
    concept = {"id": concept_id}
    if concept_id in glosses:
        concept["glosses"] = glosses[concept_id]
    return concept


def _marker(marker_id: str) -> dict:
    glosses = {
        "marker:source_language:zh_internet_slang": {
            "zh-CN": "中文网络语痕迹",
            "en-US": "Chinese internet slang marker",
        }
    }
    marker = {"id": marker_id}
    if marker_id in glosses:
        marker["glosses"] = glosses[marker_id]
    return marker


def _concept_id(value: object) -> str:
    if isinstance(value, dict):
        raw_id = value.get("id", "")
        if isinstance(raw_id, str):
            return raw_id
    if isinstance(value, str):
        return value
    return ""


def _best_gloss(glosses: object, target_language: str) -> str:
    if not isinstance(glosses, dict):
        return ""
    target = target_language.lower()
    for key, value in glosses.items():
        if isinstance(key, str) and isinstance(value, str) and key.lower() == target:
            return value
    target_prefix = target.split("-")[0]
    for key, value in glosses.items():
        if isinstance(key, str) and isinstance(value, str) and key.lower().split("-")[0] == target_prefix:
            return value
    for fallback in ("und", "en-US", "zh-CN"):
        value = glosses.get(fallback)
        if isinstance(value, str):
            return value
    for value in glosses.values():
        if isinstance(value, str):
            return value
    return ""
