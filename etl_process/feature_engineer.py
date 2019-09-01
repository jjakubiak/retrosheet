
from operations import file_names, json_load, df_to_excel
import feature_operations as feat_ops
from remove_columns import del_col_set
from collections import defaultdict
import pandas as pd
import numpy as np


final_path = "C:/Retrosheet/api_data/final"
weight_path = "C:/Retrosheet/FanGraphs"

### OBA weights dataframe
df_weight = pd.read_csv(weight_path + "/wOBA_FIP_Constants.csv")
df_weight.set_index("Season", drop=True, append=False, inplace=True, verify_integrity=False)

### read data files
dict_final = defaultdict()
for file_nm in file_names(final_path):
    print(file_nm)
    key = file_nm.rsplit(".")[0]
    file_path = final_path + "/" + file_nm
    dict_final[key] = pd.read_pickle(file_path)

### feature engineer
### gameData
df_gameData = dict_final["gameData"]

### gameData, add date columns to gameData
date_prefix = "datetime"
date_col = "originalDate"
dt = date_prefix + "." + date_col

df_gameData[dt] = pd.to_datetime(df_gameData[dt])
df_gameData[date_prefix + ".year"] = df_gameData[dt].dt.year
df_gameData[date_prefix + ".month"] = df_gameData[dt].dt.month
df_gameData[date_prefix + ".day"] = df_gameData[dt].dt.day

### boxscore
df_boxscore = dict_final["boxscore"]

### boxscore, add year
df_boxscore = df_boxscore.join(df_gameData[["datetime.year"]], how="left")
# print(df_boxscore)

### boxscore, variables for helper functions
col_away = "away.teamStats.batting.runs"
col_home = "home.teamStats.batting.runs"
label = "home.result.target"
bat_path = ".teamStats.batting"
path_pit = ".teamStats.pitching"

team_type = ["away", "home"]
list_pct = [".baseOnBalls", ".strikeOuts"]

### boxscore, apply helper function for label
df_boxscore[label] = df_boxscore.apply(feat_ops.result, axis=1, col_away=col_away, col_home=col_home)

### boxscore, batting, apply helper functions for feature engineering
for team in team_type:
    df_path = team + bat_path
    df_boxscore[df_path + ".pa"] = df_boxscore.apply(feat_ops.pa, axis=1, team=team, path=bat_path)
    df_boxscore[df_path + ".singles"] = df_boxscore.apply(feat_ops.single, axis=1, team=team, path=bat_path)

    for item in list_pct:
        pct_path = df_path + item
        df_boxscore[pct_path + "Pct"] = df_boxscore.apply(feat_ops.ratio, axis=1, team=team, path=bat_path, numer=item, denom=".pa")

    df_boxscore[df_path + ".bbkPct"] = df_boxscore.apply(feat_ops.ratio, axis=1, team=team, path=bat_path, numer=".baseOnBalls", denom=".strikeOuts")
    df_boxscore[df_path + ".babip"] = df_boxscore.apply(feat_ops.babip, axis=1, team=team, path=bat_path)
    df_boxscore[df_path + ".iso"] = df_boxscore.apply(feat_ops.iso, axis=1, team=team, path=bat_path)
    df_boxscore[df_path + ".wOBA"] = df_boxscore.apply(feat_ops.wOBA, axis=1, team=team, path=bat_path, df_weight=df_weight)
    df_boxscore[df_path + ".wRAA"] = df_boxscore.apply(feat_ops.wRAA, axis=1, team=team, path=bat_path, df_weight=df_weight)
    df_boxscore[df_path + ".wRC"] = df_boxscore.apply(feat_ops.wRC, axis=1, team=team, path=bat_path, df_weight=df_weight)

### boxscore, pitching, apply helper function for feature engineer
### boxscore, pitching, batters faced; dependent on batting pa
df_boxscore["away.teamStats.pitching.bf"], df_boxscore["home.teamStats.pitching.bf"] = df_boxscore["home.teamStats.batting.pa"], df_boxscore["away.teamStats.batting.pa"]


### boxscore, pitching, apply helper funcStions for feature engineering
for team in team_type:
    df_path_pit = team + path_pit
    ### remove team or path variable
    df_boxscore[df_path_pit + ".k9"] = df_boxscore.apply(feat_ops.ratio_9, axis=1, team=team, path=path_pit, numer=".strikeOuts", denom=".inningsPitched")
    df_boxscore[df_path_pit + ".bb9"] = df_boxscore.apply(feat_ops.ratio_9, axis=1, team=team, path=path_pit, numer=".strikeOuts", denom=".baseOnBalls")
    df_boxscore[df_path_pit + ".babip"] = df_boxscore.apply(feat_ops.babip, axis=1, team=team, path=path_pit)
    df_boxscore[df_path_pit + ".fipRaw"] = df_boxscore.apply(feat_ops.fip_raw, axis=1, team=team, path=path_pit)

### copy dataframe
df_boxscore_final = df_boxscore

### add gameID index as column in dataframe
df_boxscore_final['gameID'] = df_boxscore_final.index

### delete  columns and reformat null values, temporary until imputation has been added to etl pipeline
df_boxscore_final.drop([col for col in df_boxscore_final.columns if col in del_col_set], axis=1, inplace=True)
# df_boxscore_final.replace("-.--", np.nan, inplace=True)

### write pandas dataframe to excel
df_to_excel("boxscore_engineer", "c:/retrosheet/api_structure", df_boxscore_final)