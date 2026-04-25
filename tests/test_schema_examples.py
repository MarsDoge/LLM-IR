import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def test_examples_match_schema():
    schema = json.loads((ROOT / "schema" / "llm-ir.v0.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    for path in sorted((ROOT / "examples").glob("*.llm-ir.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))

        assert errors == [], f"{path.name}: {[error.message for error in errors]}"
