from pathlib import Path
from localization_tool.pipeline.auto_translate import auto_translate_table
from localization_tool.utils.file_utils import get_yaml_tables
from localization_tool.core.table_writer import write_json


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
        print("No English YAML tables found in the {tables_folder} folder.")
        return

    for yaml_file in yaml_files:
        print(f'\nProcessing table: {yaml_file.name}')
        updated_jsons = auto_translate_table(yaml_file, target_languages)
        # print(updated_jsons, " updated jsons returned from auto_translate_table in auto_translate.py")

        # saving latest jsons in the dedicated json folder
        for language, json_data in updated_jsons.items():
            json_path = json_output_folder / f"{yaml_file.stem.replace('_en', '')}_{language}.json"
            write_json(json_path, json_data)
            print(f"Saved JSON for {language} at: {json_path}")

    print("\n✅ Auto-translation pipeline completed for all tables. Latest JSON files saved in:", json_output_folder)

if __name__ == "__main__":
    main()