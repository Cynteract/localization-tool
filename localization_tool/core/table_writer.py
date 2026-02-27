import json
import yaml
from pathlib import Path


def write_json(json_path, data):
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def write_yaml(yaml_path, data):
    # converting json data to Unity yaml format and writing to file
    yaml_data = {
        "MonoBehaviour": {
            "m_TableData": []
        }
    }

    for key, val in data.get("keys", {}).items():
        yaml_data["MonoBehaviour"]["m_TableData"].append({
            "m_Id": key,
            "m_Localized": val["value"]
        })
    
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, allow_unicode=True)