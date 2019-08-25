
from operations import file_paths, save_dataframe_csv
from collections import defaultdict
import pandas as pd
import shutil

### complete directory
to_path = "C:/Retrosheet/api_data/parsed/complete/"

key_set = set()
dict_group = defaultdict(list)

### read indivudual files and add to a dictionary of lists of dataframes
### create function to read files to dict

### staging directory
all_files = file_paths("C:/Retrosheet/api_data/parsed/intermediate/")
if bool(all_files):
    for k, v in all_files.items():
        print("extract:", k)
        for file_nm in v:
            # print(file_nm)
            key = k.rsplit("/")[-1]
            key_set.add(key)

            from_path = k + "/" + file_nm
            df_indv = pd.read_csv(from_path, index_col=[0])

            if key not in key_set:
                key_set.add(key)
                dict_group[key] = df_indv
            else:
                dict_group[key].append(df_indv)

            ### move files from staging to complete directory
            shutil.move(from_path, to_path + key + "/" + file_nm)

dict_df = defaultdict(list)

### combine dataframes
for k, v in dict_group.items():
    for index, df_row in enumerate(v):
        if index == 0:
            dict_df[k] = df_row
        else:
            df = dict_df[k]
            dict_df[k] = pd.concat([df, df_row], sort=False)
# print(dict_df["boxscore"])


### read existing dataframes from directory
final_set = set()
dict_final = defaultdict(list)

save_path = "C:/Retrosheet/api_data/final/"
final_files = file_paths(save_path)
if bool(final_files):
    for k, v in final_files.items():
        for file_nm in v:
            # print(file_nm)
            key = file_nm.rsplit(".")[0]
            final_set.add(key)

            from_path = k + "/" + file_nm
            df_final = pd.read_csv(from_path, index_col=[0])

            if key not in final_set:
                final_set.add(key)
                dict_final[key] = df_final
            else:
                dict_final[key].append(df_final)

### rename  variable
key_list = set([k for k in dict_df] + [k for k in dict_final])

for item in key_list:
    file_path = save_path + item + ".txt"
    if not bool(dict_final):
        df_combined = dict_df[item]
    else:
        df_combined = pd.concat([dict_final[item][0], dict_df[item]], sort=False)
    df_combined.to_csv(file_path, mode="w", header=True)


### write pandas dataframe to excel
# file_nm = "box"
# save_to = "c:/retrosheet/api_structure_" + file_nm + ".xlsx"
# writer = pd.ExcelWriter(save_to)
# dict_final.to_excel(writer,'Sheet1')
# writer.save()

