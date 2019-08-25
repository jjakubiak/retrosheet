
from json_operations import file_paths, save_dataframe_csv
from collections import defaultdict
import pandas as pd
import os.path
import shutil


to_path = "C:/Retrosheet/api_data/parsed/complete/"
all_files = file_paths("C:/Retrosheet/api_data/parsed/intermediate/")

key_set = set()
dict_test = defaultdict(list)

### read indivudual files and add to a dictionary of lists of dataframes
if bool(all_files):
    for k, v in all_files.items():
        for file_nm in v:
            # print(file_nm)
            key = k.rsplit("/")[-1]
            key_set.add(key)


            from_path = k + "/" + file_nm
            df = pd.read_csv(from_path)

            if key not in key_set:
                key_set.add(key)
                dict_test[key] = df
            else:
                dict_test[key].append(df)

            ### move files from staging to complete directory
            shutil.move(from_path, to_path + key + "/" + file_nm)

    ### append to final data files
    save_path = "C:/Retrosheet/api_data/final/"

    for k,v in dict_test.items():
        df_combined = pd.concat(v, axis=0, sort=False, copy=False)
        file_path = save_path + k + ".txt"
        if os.path.exists(file_path):
            df_combined.to_csv(file_path, mode="a", header=False)
        else:
            save_dataframe_csv(df_combined, save_path, k)

else:
    print("Warning: Files do not exist")

game_path = "C:/Retrosheet/api_data/game/"
source_dir = "intermediate/"
final_dir = "complete/"


# update to use functions from json_operations
game_files = os.listdir(game_path + source_dir)
if bool(game_files):
    for f in game_files:
            shutil.move(game_path + source_dir + f, game_path + final_dir + f)
else:
    print("Warning: Files do not exist")







