
from operations import file_names, json_load, df_to_excel
from feature_operations import replace_with_null, cast
import feature_operations as feat_ops
from column_list import del_col_set, list_cast_col
from collections import defaultdict
import pandas as pd
import numpy as np


final_path = "C:/Retrosheet/api_data/final"

### read data files
dict_final = defaultdict()
for file_nm in file_names(final_path):
    print(file_nm)
    key = file_nm.rsplit(".")[0]
    file_path = final_path + "/" + file_nm
    dict_final[key] = pd.read_pickle(file_path)

df_boxscore = dict_final["boxscore"]

### convert decimals without leading zero from object to float and replace missing values with null
replace_with_null(df_boxscore, "-.--")
replace_with_null(df_boxscore, ".---")

for col in list_cast_col:
    df_boxscore[col] = cast(df_boxscore, col, "float")

### print
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df_boxscore.dtypes)

### write pandas dataframe to excel
df_to_excel("boxscore_raw", "c:/retrosheet/api_structure", df_boxscore)