from llm_ir.core import decode_document, encode_text


def test_encode_chinese_slang_creates_reaction_ir():
    document = encode_text("这事儿也太离谱了吧，真绷不住了。", source_language="zh-CN")

    assert document["schema"] == "llm-ir.v0"
    assert document["source"]["language"] == "zh-CN"
    assert document["intent"]["id"] == "act:express_reaction"
    assert document["meaning"]["glosses"]["zh-CN"] == "说话者强烈觉得这件事很离谱。"
    assert document["privacy"]["source_language_markers"][0]["id"] == "marker:source_language:zh_internet_slang"


def test_decode_chinese_slang_to_natural_english():
    document = encode_text("这事儿也太离谱了吧，真绷不住了。", source_language="zh-CN")

    assert decode_document(document, "en-US") == "This is honestly insane. I can't even."
