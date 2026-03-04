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
    specials = meta_paths["special"]
    collections = meta_paths["collection"]
    crossovers = meta_paths["crossover"]
    featuring = meta_paths["featuring"]
    free = meta_paths["free"]

    # Create Personal folders
    for personal_folder_name, personal_folder_path in xr_db['personal_folders'].items():
        os.makedirs(personal_folder_path, exist_ok=True)

    # Create Labels and Series
    for series_folder_name, series_folder_path in xr_db['series_folders'].items():
        full_series_folder_path = os.path.join(root, series_folder_path)
        os.makedirs(full_series_folder_path, exist_ok=True)
        series_paths[series_folder_name] = os.path.abspath(full_series_folder_path)

    BOL = series_paths["BOL"]
    KIM = series_paths["KIM"]
    TG = series_paths["TG"]
    TG_DK = series_paths["TG_DK"]
    TG_MCT = series_paths["TG_MCT"]
    TG_YMH = series_paths["TG_YMH"]
    UG = series_paths["UG"]
    UGS = series_paths["UGS"]
    XR = series_paths["XR"]
    BLS = series_paths["BLS"]
    CD = series_paths["CD"]
    DK = series_paths["DK"]
    FL = series_paths["FL"]
    HY = series_paths["HY"]
    HYG = series_paths["HYG"]
    IMS = series_paths["IMS"]
    LY = series_paths["LY"]
    MF = series_paths["MF"]
    MCT = series_paths["MCT"]
    MT = series_paths["MT"]
    MY = series_paths["MY"]
    MS = series_paths["MS"]
    MM = series_paths["MM"]
    MYG = series_paths["MYG"]
    RSG = series_paths["RSG"]
    ST = series_paths["ST"]
    TKM = series_paths["TKM"]
    UX = series_paths["UX"]
    WS = series_paths["WS"]
    YU = series_paths["YU"]
    XYS = series_paths["XYS"]
    YMH = series_paths["YMH"]
    YOU = series_paths["YOU"]

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
