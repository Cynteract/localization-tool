from pathlib import Path
from localization_tool.core.changeset import calculate_changeset
from localization_tool.translation.google import GoogleTranslator
from localization_tool.translation.confidence import estimate_confidence
from localization_tool.core.table_loader import yaml_to_json, load_json
from localization_tool.core.table_writer import write_json, write_yaml
import time

translator = GoogleTranslator()
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


def safe_translate(text, target_language):
    if not text:
        return "", 1.0 
    
    for attempt in range(MAX_RETRIES):
        try:
            translation = translator.translate(text, target_language)
            if translation is not None and translation.text is not None:
                confidence = None
            if translation.extra_data and 'confidence' in translation.extra_data:
                confidence = translation.extra_data['confidence']
            return translation.text, confidence
        except Exception as e:
            print(f"Translation error on attempt {attempt + 1} for text: '{text}' to language: '{target_language}'. Error: {e}")
            time.sleep(RETRY_DELAY)
    
    print(f"Using original text after {MAX_RETRIES} failed attempts: '{text}' for language: '{target_language}")
    return text, 1.0



def auto_translate_table(yaml_path, target_languages):
    # loading english json
    english_json = yaml_to_json(yaml_path)
    # print(english_json, " english json loaded in auto_translate.py")
    target_jsons = {}

    # loading existing target jsons or initialize
    for langauge in target_languages:
        # print(yaml_path.parent, yaml_path.stem, langauge, " preparing target json paths in auto_translate.py")
        target_json_path = yaml_path.parent / f"{yaml_path.stem.replace('_en', '')}_{langauge}.json"
        # print(target_json_path, " target json path in auto_translate.py")
        if target_json_path.exists():
            target_jsons[langauge] = load_json(target_json_path)
        else:
            target_jsons[langauge] = {
                "table_name": english_json["table_name"],
                "language": langauge,
                "description": english_json.get("description", ""),
                "keys": {}
            }
    # print(target_jsons, " target jsons prepared in auto_translate.py")
        
    # processing each target language
    for language, target_json in target_jsons.items():
        changes = calculate_changeset(english_json, target_json)
        # print(changes, " changes calculated for language:", language, " in auto_translate.py")

        for entry in changes["create"] + changes["update"]:
            key = entry["key"]
            english_value = entry.get("value") or entry.get("new_value")
            # print(translator.translate(english_value, language), " auto_translate.py")
            # print(translator.translate(english_value, language).extra_data, " auto_translate.py")
            # translation = translator.translate(english_value, language)
            # translated_text, google_confidence = translation.text, translation.extra_data.get('confidence')
            # print(translated_text, " translated text in auto_translate.py")
            # print(google_confidence, " google confidence in auto_translate.py")
            translated_text, google_confidence = safe_translate(english_value, language)
            confidence = google_confidence if google_confidence else estimate_confidence(english_value, translated_text)


            target_json["keys"][key] = {
                "value": translated_text,
                "status": "machine",
                "confidence": confidence
            }

        # deleting onsolete keys
        for entry in changes["delete"]:
            target_json["keys"].pop(entry["key"], None)

        # saving JSON and YAML
        target_json_path = yaml_path.parent / f"{yaml_path.stem.replace('_en', '')}_{language}.json"
        write_json(target_json_path, target_json)
        target_yaml_path = yaml_path.parent / f"{yaml_path.stem.replace('_en', '')}_{language}.yaml"
        write_yaml(target_yaml_path, target_json)
    
    print(f"Auto-translation completed for {yaml_path.stem} to languages: {', '.join(target_languages)}")
    return target_jsons