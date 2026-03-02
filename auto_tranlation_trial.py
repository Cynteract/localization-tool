import json
from pathlib import Path
import tempfile
from googletrans import Translator
import subprocess
import tarfile
import io
import tempfile

CYNTERACT_REPO_ROOT = Path(r"D:\Cynteract\cynteract-app")

# paths to english and target language json
eng_json_path = Path(r"D:\Cynteract\cynteract-app\Assets\Locales\Tables\Achievements_en.json")
target_json_path = Path(r"D:\Cynteract\cynteract-app\Assets\Locales\Tables\Achievements_de.json")

# restoring previous english file
def get_previous_english(path, repo_root):
    try:
        relative_path = path.relative_to(repo_root)
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_process = subprocess.run(
                ["git", "-C", str(repo_root), "archive", "HEAD", str(relative_path)],
                stdout=subprocess.PIPE,
                check=True,
            )

        with tarfile.open(fileobj = io.BytesIO(archive_process.stdout)) as tar:
            tar.extractall(temp_dir)
        
        previous_english_path = Path(temp_dir) / path

        if previous_english_path.exists():
            with open(previous_english_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving previous english file: {e.stderr}")


def main():

    # loading current english file
    with open(eng_json_path, 'r', encoding='utf-8') as f:
        eng_data = json.load(f)
    
    # loading previous english file
    previous_eng_data = get_previous_english(
    eng_json_path,
    CYNTERACT_REPO_ROOT
    )
    previous_eng_keys = previous_eng_data.get("keys", {}) if previous_eng_data else {}

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
    
    translator = Translator()
    create, update, delete = [], [], []

    eng_keys = eng_data.get("keys", {})
    target_keys = target_data.get("keys", {})

    # changeset calculation with previous english as reference
    for key, value in eng_keys.items():
        current_value = value.get("value")

        if not isinstance(current_value, str):
            current_value = str(current_value)
        
        if key not in target_keys:
            create.append(key)
        
        elif previous_eng_keys.get(key, {}).get("value") != current_value:
            update.append(key)
        
    for key in target_keys:
        if key not in eng_keys:
            delete.append(key)

    
    changeset = {
        "create": create,
        "update": update,
        "delete": delete
    }

    for key in create + update:
        eng_value = eng_keys[key].get("value")
        if not isinstance(eng_value, str):
            eng_value = str(eng_value)

        try:
            translated_obj = translator.translate(eng_value, src='en', dest=target_data["language"])
            translated = translated_obj.text
            print(f"Translated '{eng_value}' to '{translated}'")
        except Exception as e:
            print(f"Error translating '{eng_value}': {e}")
            translated = eng_value
        
        target_data["keys"][key] = {
            "value": translated,
            "description": "",
            "reviewed": False
        }
    
    # saving target json
    with open(target_json_path, 'w', encoding='utf-8') as f:
        json.dump(target_data, f, indent=4, ensure_ascii=False)
    
    # saving changeset json
    changeset_path = Path(target_json_path.parent / f"{eng_data['table_name']}_{target_data['language']}_autotranslate_changeset.json")
    with open(changeset_path, 'w', encoding='utf-8') as f:
        json.dump(changeset, f, indent=4, ensure_ascii=False)
    
    print(f"Autotranslation complete. Updated JSON saved → {target_json_path}")
    print(f"Changeset saved → {changeset_path}")

if __name__ == "__main__":
    main()


# loading json files
# with open(eng_json_path, 'r', encoding='utf-8') as f:
#     eng_data = json.load(f)

# if target_json_path.exists():
#     with open(target_json_path, 'r', encoding='utf-8') as f:
#         target_data = json.load(f)
# else:
#     target_data = {
#         "table_name": eng_data["table_name"],
#         "language": "de",
#         "description": "",
#         "keys": {}
#     }

# # initialize translator
# translator = Translator()

# # calculating changeset
# create, update, delete = [], [], []

# eng_keys = eng_data.get("keys", {})
# target_keys = target_data.get("keys", {})

# # keys to create or update
# for k, v in eng_keys.items():
#     if k not in target_keys:
#         create.append(k)
#     elif v["value"] != target_keys[k].get("value"):
#         update.append(k)

# # keys to delete (optional: present in target but not in english)
# for k in target_keys:
#     if k not in eng_keys:
#         delete.append(k)

# changeset = {
#     "create": create,
#     "update": update,
#     "delete": delete
# }

# # autotranslate create and update keys
# for k in create + update:
#     eng_value = eng_keys[k]["value"]
#     translated = translator.translate(eng_value, src='en', dest=target_data["language"]).text
#     translated_obj = translator.translate(eng_value, src='en', dest=target_data["language"])
#     print("RAW:", translated_obj)
#     translated = translated_obj.text
#     target_data["keys"][k] = {
#         "value": translated,
#         "description": "",
#         "reviewed": False
#     }
#     print(f"Translated '{eng_value}' to '{translated}'")

# # save updated target json
# with open(target_json_path, 'w', encoding='utf-8') as f:
#     json.dump(target_data, f, indent=4, ensure_ascii=False)

# # save changeset json
# changeset_path = Path(target_json_path.parent / f"{eng_data['table_name']}_{target_data['language']}_autotranslate_changeset.json")
# with open(changeset_path, 'w', encoding='utf-8') as f:
#     json.dump(changeset, f, indent=4, ensure_ascii=False)

# print(f"Autotranslation complete. Updated JSON saved → {target_json_path}")
# print(f"Changeset saved → {changeset_path}")