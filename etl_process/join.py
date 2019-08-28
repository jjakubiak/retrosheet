
from collections import defaultdict
import pandas as pd
from operations import file_names

final_path = "C:/Retrosheet/api_data/final"

### read data files
dict_final = defaultdict()
for file_nm in file_names(final_path):
    print(file_nm)
    key = file_nm.rsplit(".")[0]
    file_path = final_path + "/" + file_nm
    dict_final[key] = pd.read_csv(file_path, index_col=[0])

### boxscore
df_boxscore = dict_final["boxscore"]
df_boxscore = dict_final["boxscore"]

print(df_boxscore)