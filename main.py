import ctypes # Hiding
from datetime import datetime
import json
import os
import re
import winshell

# Folder/File visibility
HIDDEN = 0x02
NORMAL = 0x80

# Dict Paths
meta_paths = {}
series_paths = {}

LNK = ".lnk"
XE = ".xr_error"

UNKNOWN = "!"

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
            full_photographer_alias_path = os.path.join(photographers, alias+LNK)
            with winshell.shortcut(full_photographer_name_path) as shortcut:
                shortcut.write(full_photographer_alias_path)

    # Create Models
    # First name is folder, other names aliases used as links to that folder
    for model in xr_db['models']:
        full_model_name_path = os.path.join(models, model[0])
        os.makedirs(full_model_name_path, exist_ok=True)

        for alias in model[1:]:
            full_model_alias_path = os.path.join(models, alias+LNK)
            with winshell.shortcut(full_model_name_path) as shortcut:
                shortcut.write(full_model_alias_path)

    # Create Issues
    for issue in xr_db['issues']:

        stamp = issue["id"]

        # Prep date
        match = re.search(r'(\d{4})(\d{2})(\d{2})', stamp)
        release_date_unix = None
        if not match:
            match = re.search(r'(\d{4})(\d{2})(\d{2})', issue["date"])
        if match:
            year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
            release_date = datetime(year, month, day)
            release_date_unix = release_date.timestamp()
            # print(f"Setting time to {release_date} ({release_date_unix}).")

        # Create XR20130905N00001 Folder
        label = issue["label"]
        tkm_path = None
        if label == "TKM":
            tkm_path = os.path.join(root, series_paths[label])
            label = "BLS"
        issue_path = os.path.join(root, series_paths[label], stamp)
        # print(f"Create Folder: {issue_path}")
        os.makedirs(issue_path, exist_ok=True)
        os.utime(issue_path, (release_date_unix, release_date_unix))
        if tkm_path:
            bls_at_tkm_path = os.path.join(tkm_path, stamp+LNK)
            with winshell.shortcut(issue_path) as shortcut:
                shortcut.write(bls_at_tkm_path)
            os.utime(bls_at_tkm_path, (release_date_unix, release_date_unix))
            # print(f"Create Link {bls_at_tkm_path} to {issue_path}")

        # Link Folder at respective Photographer
        photographer = issue["photographer"]
        photographer_path = None
        if photographer == UNKNOWN:
            photographer_path = unknown_photographers
        else:
            photographer_path = os.path.join(photographers, photographer)
        if not os.path.exists(photographer_path):
            print(f"Photographer {photographer} not found. New?")
        else:
            issue_at_photographer_path = os.path.join(photographer_path, stamp+LNK)
            # print(f"Create Link {issue_at_photographer_path} to {issue_path}")
            with winshell.shortcut(issue_path) as shortcut:
                    shortcut.write(issue_at_photographer_path)
            os.utime(issue_at_photographer_path, (release_date_unix, release_date_unix))

        #Link Folder at respective Models (can be more than one)
        model_path = None
        for model in issue["models"]:
            if model == UNKNOWN:
                model_path = unknown_models
            else:
                model_path = os.path.join(models, model)
            if not os.path.exists(model_path):
                print(f"Model {model} not found. New Girl?")
                continue
            issue_at_model_path = os.path.join(model_path, stamp+LNK)
            # print(f"Create Link {issue_at_model_path} to {issue_path}")
            with winshell.shortcut(issue_path) as shortcut:
                shortcut.write(issue_at_model_path)
            os.utime(issue_at_model_path, (release_date_unix, release_date_unix))

        # Create and hide xr_error files, if applicable
        for error in issue["errors"]:
            error_file = os.path.join(issue_path, error+XE)
            # print(f"Create File {error_file}")
            open(error_file, 'a').close()
            os.utime(error_file, None)
            ctypes.windll.kernel32.SetFileAttributesW(error_file, HIDDEN)

        # Hide folder, if not in possession
        owned = issue["owned"]
        if(not owned):
            # print(f"Mark {stamp} as hidden")
            ctypes.windll.kernel32.SetFileAttributesW(issue_path, HIDDEN)
        else:
            ctypes.windll.kernel32.SetFileAttributesW(issue_path, NORMAL)

        # Link Folder, if special issue (more than one category can be applicable)
        for special in issue["specials"]:
            special_path = os.path.join(meta_paths[special])
            # print("Create Link " + os.path.join(special_path, stamp+LNK) + " to " + issue_path)
            with winshell.shortcut(issue_path) as shortcut:
                shortcut.write(os.path.join(special_path, stamp+LNK))
            os.utime(os.path.join(special_path, stamp+LNK), (release_date_unix, release_date_unix))

input("Finished.")
