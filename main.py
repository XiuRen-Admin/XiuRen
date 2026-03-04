import json
import os
import winshell

# Dict Paths
meta_paths = {}
series_paths = {}

lnk = ".lnk"

with open('.data.json', encoding='utf-8-sig') as data_json:
    xr_db = json.load(data_json)

    # Create Meta folders
    for meta_folder_name, meta_folder_path in xr_db['meta_folders'].items():
        os.makedirs(meta_folder_path, exist_ok=True)
        meta_paths[meta_folder_name] = os.path.abspath(meta_folder_path)

    root = meta_paths["all"]
    models = meta_paths["model"]
    unknown_models = meta_paths["unknown_model"]
    photographers = meta_paths["photographer"]
    unknown_photographers = meta_paths["unknown_photographer"]

    # Create Personal folders
    for personal_folder_name, personal_folder_path in xr_db['personal_folders'].items():
        os.makedirs(personal_folder_path, exist_ok=True)

    # Create Labels and Series
    for series_folder_name, series_folder_path in xr_db['series_folders'].items():
        full_series_folder_path = os.path.join(root, series_folder_path)
        os.makedirs(full_series_folder_path, exist_ok=True)
        series_paths[series_folder_name] = os.path.abspath(full_series_folder_path)

    # Create Photographers
    # First name is folder, other names aliases used as links to that folder
    for photographer in xr_db['photographers']:
        full_photographer_name_path = os.path.join(photographers, photographer[0])
        os.makedirs(full_photographer_name_path, exist_ok=True)

        for alias in photographer[1:]:
            full_photographer_alias_path = os.path.join(photographers, alias+lnk)
            with winshell.shortcut(full_photographer_name_path) as shortcut:
                shortcut.write(full_photographer_alias_path)

    # Create Models
    # First name is folder, other names aliases used as links to that folder
    for model in xr_db['models']:
        full_model_name_path = os.path.join(models, model[0])
        os.makedirs(full_model_name_path, exist_ok=True)

        for alias in model[1:]:
            full_model_alias_path = os.path.join(models, alias+lnk)
            with winshell.shortcut(full_model_name_path) as shortcut:
                shortcut.write(full_model_alias_path)
