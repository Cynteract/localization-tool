from pathlib import Path
from localization_tool.pipeline.auto_translate import auto_translate_table
from localization_tool.utils.file_utils import get_yaml_tables
from localization_tool.core.table_writer import write_json
from localization_tool.core.table_loader import yaml_to_json


def main():
    tables_folder = Path(r"D:\Cynteract\cynteract-app\Assets\Locales\Tables")
    target_languages = ["de"]

    # folder to save json files
    json_output_folder = Path(r"D:\Cynteract\localization_tool\json_files")
    json_output_folder.mkdir(exist_ok=True, parents=True)

    # looping over all english tables
    yaml_files = get_yaml_tables(tables_folder)
    #print(yaml_files, " yaml files found in the tables folder")  # Debugging line to check found YAML files
    if not yaml_files:
        print(f"No English YAML tables found in the {tables_folder} folder.")
        return

    for yaml_file in yaml_files:
        print(f'\nProcessing table: {yaml_file.name}')
        try:
            english_json = yaml_to_json(yaml_file)
            updated_jsons = auto_translate_table(english_json, yaml_file, target_languages)
        except Exception as e:
            print(f"Error processing {yaml_file.name}: {e}")
            continue
        # print(updated_jsons, " updated jsons returned from auto_translate_table in auto_translate.py")

        # saving latest jsons in the dedicated json folder
        for language, json_data in updated_jsons.items():
            try:
                json_path = json_output_folder / f"{yaml_file.stem.replace('_en', '')}_{language}.json"
                write_json(json_path, json_data)
                print(f"Saved JSON for {language} at: {json_path}")
            except Exception as e:
                print(f"Error saving JSON for {language} from {yaml_file.name}: {e}")

    print("\n✅ Auto-translation pipeline completed for all tables. Latest JSON files saved in:", json_output_folder)

if __name__ == "__main__":
    main()