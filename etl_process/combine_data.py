
from operations import file_paths, save_dataframe_csv
from collections import defaultdict
import pandas as pd
import shutil

### complete directory
to_path = "C:/Retrosheet/api_data/parsed/complete/"

key_set = set()
dict_group = defaultdict(list)

### read individual files and add to a dictionary containing a list of dataframes for each key, key is the file prefix
### staging directory
all_files = file_paths("C:/Retrosheet/api_data/parsed/intermediate/")
if bool(all_files):
    for k, v in all_files.items():
        print("extract:", k)
        for file_nm in v:
            key = k.rsplit("/")[-1]
            key_set.add(key)

            from_path = k + "/" + file_nm
            # df_indv = pd.read_csv(from_path, index_col=[0])
            df_indv = pd.read_pickle(from_path)

            if key not in key_set:
                key_set.add(key)
                dict_group[key] = df_indv
            else:
                dict_group[key].append(df_indv)

            ### move files from staging to complete directory
            # shutil.move(from_path, to_path + key + "/" + file_nm)

dict_df = defaultdict(list)
dict_dup = defaultdict(list)

### combine list of data frames created above into single dataframe; outer join, adds single new row and any new columns
### checks if the index is unique
for k, v in dict_group.items():
    for index, df_row in enumerate(v):
        df_row_index = df_row.index.values[0]
        if index == 0:
            dict_df[k] = df_row
        else:
            df = dict_df[k]
            ### add new row to combined dataframe if the index is unique
            try:
                dict_df[k] = pd.concat([df, df_row], sort=False, verify_integrity=True)
            except ValueError:
                ### 1) store all duplicate index rows 2) delete old row from existing dataframe and 3) add new row to existing dataframe
                df_obj = dict_df[k]
                dict_dup[k].append(df_obj.loc[df_row_index])
                dict_df[k].drop([df_row_index], inplace=True)
                dict_df[k] = pd.concat([df, df_row], sort=False, verify_integrity=True)


### read existing final dataframes from directory into dictionary of dataframes
final_set = set()
dict_final = defaultdict(list)

save_path = "C:/Retrosheet/api_data/final/"
final_files = file_paths(save_path)
if bool(final_files):
    for k, v in final_files.items():
        for file_nm in v:
            key = file_nm.rsplit(".")[0]
            final_set.add(key)

            from_path = k + "/" + file_nm
            df_final = pd.read_pickle(from_path)

            if key not in final_set:
                final_set.add(key)
                dict_final[key] = df_final
            else:
                dict_final[key].append(df_final)


### verify integrity manually
dict_df_index = {key: val.index.values for key, val in dict_df.items()}
dict_final_index = {key: val[0].index.values for key, val in dict_final.items()}

### create list of distinct key from previous dictionary and new dictionary
list_key = set([k for k in dict_df_index] + [k for k in dict_final_index])

### find duplicate keys and remove from previous dataframes
dup_dict = defaultdict(list)

if bool(dict_final_index):
    for key in list_key:
        dup_index = list(set(dict_df_index[key]).intersection(dict_final_index[key]))
        df_obj = dict_final[key][0]
        dup_dict[key].append(df_obj.loc[dup_index])
        dict_final[key][0].drop(dup_index, inplace=True)

for key in list_key:
    file_path = save_path + key + ".pkl"
    if not bool(dict_final):
        df_combined = dict_df[key]
    else:
        df_combined = pd.concat([dict_final[key][0], dict_df[key]], sort=False, verify_integrity=True)
    df_combined.to_pickle(file_path)
    df_combined.to_csv("C:/Retrosheet/api_data/final_txt/"+ key + ".txt")


### write pandas dataframe to excel
# file_nm = "box"
# save_to = "c:/retrosheet/api_structure_" + file_nm + ".xlsx"
# writer = pd.ExcelWriter(save_to)
# dict_final.to_excel(writer,'Sheet1')
# writer.save()
