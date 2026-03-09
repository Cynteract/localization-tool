MIN_CONFIDENCE_IF_IDENTICAL = 0.3

def estimate_confidence(source_text, translated_text):
    if source_text == translated_text:
        return MIN_CONFIDENCE_IF_IDENTICAL

    if '{' in source_text:
        source_placeholders = source_text.count('{')
        translated_placeholders = translated_text.count('{')

        if source_placeholders != translated_placeholders:
            return 0.0  # broken placeholder

        return 0.1  # placeholders preserved

    return 0.8