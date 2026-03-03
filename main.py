import json
import os

# Meta Paths
meta_paths = {}

with open('.data.json') as data_json:
    xr_db = json.load(data_json)

    # Create Meta folders
    for meta_folder_name, meta_folder_path in xr_db['meta_folders'].items():
        os.makedirs(meta_folder_path, exist_ok=True)
        meta_paths[meta_folder_name] = os.path.abspath(meta_folder_path)

    root = meta_paths["all"]
    models = meta_paths["models"]
    unknown_models = meta_paths["unknown_models"]
    photographers = meta_paths["photographers"]
    unknown_photographers = meta_paths["unknown_photographers"]
    specials = meta_paths["specials"]
    collections = meta_paths["collections"]
    crossovers = meta_paths["crossovers"]
    featuring = meta_paths["featuring"]
    free = meta_paths["free"]

    # Create Personal folders
    for personal_folder_name, personal_folder_path in xr_db['personal_folders'].items():
        os.makedirs(personal_folder_path, exist_ok=True)

    # Create Labels and Series
    for series_folder_name, series_folder_path in xr_db['series_folders'].items():
        full_series_folder_path = os.path.join(root, series_folder_path)
        os.makedirs(full_series_folder_path, exist_ok=True)
