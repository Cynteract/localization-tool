import json
from pathlib import Path
from googletrans import Translator

# paths to english and target language json
eng_json_path = Path(r"D:\Cynteract\cynteract-app\Assets\Locales\Tables\Achievements_en.json")
target_json_path = Path(r"D:\Cynteract\cynteract-app\Assets\Locales\Tables\Achievements_de.json")

# loading json files
with open(eng_json_path, 'r', encoding='utf-8') as f:
    eng_data = json.load(f)

if target_json_path.exists():
    with open(target_json_path, 'r', encoding='utf-8') as f:
        target_data = json.load(f)
else:
    target_data = {
        "table_name": eng_data["table_name"],
        "language": "de",
        "description": "",
        "keys": {}
    }

# initialize translator
translator = Translator()

# calculating changeset
create, update, delete = [], [], []

eng_keys = eng_data.get("keys", {})
target_keys = target_data.get("keys", {})

# keys to create or update
for k, v in eng_keys.items():
    if k not in target_keys:
        create.append(k)
    elif v["value"] != target_keys[k].get("value"):
        update.append(k)

# keys to delete (optional: present in target but not in english)
for k in target_keys:
    if k not in eng_keys:
        delete.append(k)

changeset = {
    "create": create,
    "update": update,
    "delete": delete
}

# autotranslate create and update keys
for k in create + update:
    eng_value = eng_keys[k]["value"]
    translated = translator.translate(eng_value, src='en', dest=target_data["language"]).text
    translated_obj = translator.translate(eng_value, src='en', dest=target_data["language"])
    print("RAW:", translated_obj)
    translated = translated_obj.text
    target_data["keys"][k] = {
        "value": translated,
        "description": "",
        "reviewed": False
    }
    print(f"Translated '{eng_value}' to '{translated}'")

# save updated target json
with open(target_json_path, 'w', encoding='utf-8') as f:
    json.dump(target_data, f, indent=4, ensure_ascii=False)

# save changeset json
changeset_path = Path(target_json_path.parent / f"{eng_data['table_name']}_{target_data['language']}_autotranslate_changeset.json")
with open(changeset_path, 'w', encoding='utf-8') as f:
    json.dump(changeset, f, indent=4, ensure_ascii=False)

print(f"Autotranslation complete. Updated JSON saved → {target_json_path}")
print(f"Changeset saved → {changeset_path}")