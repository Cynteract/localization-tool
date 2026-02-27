def estimate_confidence(source_text, translated_text):
    if source_text == translated_text:
        return 0.0
    if '{' in source_text and source_text.count('{') == translated_text.count('{'):
        return 0.1
    return 0.8