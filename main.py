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
