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

xiuren_pattern = r'(\d{4})(\d{2})(\d{2})'
yyyymmdd_pattern = r'(\d{4})-(\d{2})-(\d{2})'

def get_label(set_name: str) -> str:
    if set_name.startswith("YouMiHui"):
        return "TGD_YMH"
    match = re.match(r'^([A-Z]{2,4})\.?', set_name)
    if not match:
        return ""
    label = match.group(1)
    if label == "BLV":
        return "BOL"
    return label

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

    singles_path, various_path, other_path = [xr_db['personal_folders'][k] for k in ['single', 'various_model', 'other_model']]
    various_singles, other, various, main = [xr_db['personal_collections'][k] for k in ['various_singles', 'other', 'various', 'main']]

    for various_single in various_singles:
        os.makedirs(os.path.join(various_path, various_single), exist_ok=True)

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
        model = None

        # Prep date
        match = re.search(xiuren_pattern, stamp)
        release_date_unix = None
        if not match:
            match = re.search(yyyymmdd_pattern, issue["date"])
            # print(stamp + " " + issue["date"])
        if match:
            year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
            release_date = datetime(year, month, day)
            release_date_unix = release_date.timestamp()
            # print(f"Setting time to {release_date} ({release_date_unix}).")
        else:
            print(f"ERROR: {stamp} has no date!")

        # Create XR20130905N00001 Folder
        label = issue["label"]
        tkm_path = None
        rsg_path = None
        if label == "TKM":
            tkm_path = os.path.join(root, series_paths[label])
            label = "BLS"
        if label == "RSG":
            rsg_path = os.path.join(root, series_paths[label])
            label = "MCT"
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
        if rsg_path:
            mct_at_rsg_path = os.path.join(rsg_path, stamp+LNK)
            with winshell.shortcut(issue_path) as shortcut:
                shortcut.write(mct_at_rsg_path)
            os.utime(mct_at_rsg_path, (release_date_unix, release_date_unix))
            # print(f"Create Link {mct_at_rsg_path} to {issue_path}")

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

        # Add folder to personal collection
        single = issue["single"]
        if(single):
            single_models = set(issue["models"]) & set(various_singles)
            if single_models:
                for single_model in single_models:
                    single_folder = os.path.join(various_path, single_model)
                    # print(f"Link {stamp} under {single_folder}")
                    issue_at_single_path = os.path.join(single_folder, stamp+LNK)
                    with winshell.shortcut(issue_path) as shortcut:
                        shortcut.write(issue_at_single_path)
                    os.utime(issue_at_single_path, (release_date_unix, release_date_unix))
            else:
                single_folder = singles_path
                # print(f"Link {stamp} under {single_folder}")
                issue_at_single_path = os.path.join(single_folder, stamp+LNK)
                with winshell.shortcut(issue_path) as shortcut:
                    shortcut.write(issue_at_single_path)
                os.utime(issue_at_single_path, (release_date_unix, release_date_unix))

# Special case reused BOL numbers
bol_16_stamp = "BOL.16"
bol_17_stamp = "BOL.17"

bol_16_release_date = datetime(2016, 12, 29)
bol_16_release_date_unix = bol_16_release_date.timestamp()
bol_17_release_date = datetime(2017, 1, 19)
bol_17_release_date_unix = bol_17_release_date.timestamp()

bol_16_issue_path = os.path.join(root, series_paths["BOL"], "!reused numbers", bol_16_stamp)
bol_17_issue_path = os.path.join(root, series_paths["BOL"], "!reused numbers", bol_17_stamp)

os.makedirs(bol_16_issue_path, exist_ok=True)
os.utime(bol_16_issue_path, (bol_16_release_date_unix, bol_16_release_date_unix))
os.makedirs(bol_17_issue_path, exist_ok=True)
os.utime(bol_17_issue_path, (bol_17_release_date_unix, bol_17_release_date_unix))
ctypes.windll.kernel32.SetFileAttributesW(bol_16_issue_path, HIDDEN)
ctypes.windll.kernel32.SetFileAttributesW(bol_17_issue_path, HIDDEN)

bol_16_photographer_path = os.path.join(photographers, "FES鳶YuanChen")
bol_17_photographer_path = os.path.join(photographers, "BalalaPure")
with winshell.shortcut(bol_16_issue_path) as shortcut:
    shortcut.write(os.path.join(bol_16_photographer_path, bol_16_stamp+LNK))
os.utime(os.path.join(bol_16_photographer_path, bol_16_stamp+LNK), (bol_16_release_date_unix, bol_16_release_date_unix))
with winshell.shortcut(bol_17_issue_path) as shortcut:
    shortcut.write(os.path.join(bol_17_photographer_path, bol_17_stamp+LNK))
os.utime(os.path.join(bol_17_photographer_path, bol_17_stamp+LNK), (bol_17_release_date_unix, bol_17_release_date_unix))

bol_16_model_path = os.path.join(models, "刘娅希")
bol_17_model_path = os.path.join(models, "猫九")
with winshell.shortcut(bol_16_issue_path) as shortcut:
    shortcut.write(os.path.join(bol_16_model_path, bol_16_stamp+LNK))
os.utime(os.path.join(bol_16_model_path, bol_16_stamp+LNK), (bol_16_release_date_unix, bol_16_release_date_unix))
with winshell.shortcut(bol_17_issue_path) as shortcut:
    shortcut.write(os.path.join(bol_17_model_path, bol_17_stamp+LNK))
os.utime(os.path.join(bol_17_model_path, bol_17_stamp+LNK), (bol_17_release_date_unix, bol_17_release_date_unix))

# Personal Links to models
for model in other:
    link_to_model = os.path.join(models, model)
    link_to_collection = os.path.join(other_path, model+LNK)
    # print(f"Linking {link_to_model} to {link_to_collection}")
    with winshell.shortcut(link_to_model) as shortcut:
        shortcut.write(link_to_collection)

for model in various:
    link_to_model = os.path.join(models, model)
    link_to_collection = os.path.join(various_path, model+LNK)
    # print(f"Linking {link_to_model} to {link_to_collection}")
    with winshell.shortcut(link_to_model) as shortcut:
        shortcut.write(link_to_collection)

for model in main:
    link_to_model = os.path.join(models, model)
    link_to_collection = model+LNK # this folder
    # print(f"Linking {link_to_model} to {link_to_collection}")
    with winshell.shortcut(link_to_model) as shortcut:
        shortcut.write(link_to_collection)

input("Finished.")
