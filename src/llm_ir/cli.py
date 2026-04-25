from __future__ import annotations

import argparse
import json
from pathlib import Path

from llm_ir.core import decode_document, encode_text


def main() -> int:
    parser = argparse.ArgumentParser(prog="llm-ir")
    subparsers = parser.add_subparsers(dest="command", required=True)

    encode_parser = subparsers.add_parser("encode", help="Encode text into a prototype LLM-IR document.")
    encode_parser.add_argument("text")
    encode_parser.add_argument("--source-language")

    decode_parser = subparsers.add_parser("decode", help="Decode an LLM-IR JSON document into target text.")
    decode_parser.add_argument("path", type=Path)
    decode_parser.add_argument("--target", required=True, help="Target language tag, such as en-US or zh-CN.")

    args = parser.parse_args()

    if args.command == "encode":
        document = encode_text(args.text, source_language=args.source_language)
        print(json.dumps(document, ensure_ascii=False, indent=2))
        return 0

    if args.command == "decode":
        with args.path.open("r", encoding="utf-8") as handle:
            document = json.load(handle)
        print(decode_document(document, args.target))
        return 0

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
