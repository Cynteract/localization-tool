from pathlib import Path

def get_yaml_tables(folder):
    return list(folder.glob("*_en.asset"))