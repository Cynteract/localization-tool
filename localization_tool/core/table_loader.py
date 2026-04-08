import yaml
import json
from pathlib import Path

class UnitySafeLoader(yaml.SafeLoader):
    pass

def unknown_constructor(loader, tag_suffix, node):
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)
    elif isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    elif isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node)
    else:
        return None

UnitySafeLoader.add_multi_constructor('tag:unity3d.com,2011:', unknown_constructor)

def yaml_to_json(yaml_path, language=None):
    
    # converting Unty yaml file to json format
    with open(yaml_path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.load(f, Loader=UnitySafeLoader)
    
    table_name = yaml_path.stem.replace(f"_{language}", "") if language else yaml_path.stem
    table_language = language or "en"

    json_data = {
        "table_name": table_name,
        "language": table_language,
        "description": yaml_data.get("description", ""),
        "keys": yaml_data.get("keys", {})
    }

    table_data = yaml_data.get("MonoBehaviour", {}).get("m_TableData", [])
    for entry in table_data:
        key = str(entry.get("m_Id"))
        value = entry.get("m_Localized")

        if value:
            json_data["keys"][key] = {
                "value": value,
                "description": "",
                "reviewed": True
            }
        
    return json_data


def load_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)