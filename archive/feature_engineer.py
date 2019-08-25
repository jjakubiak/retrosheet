
# from operations import file_names, json_load
# from collections import defaultdict
# import pandas as pd
# from pandas.api.types import is_numeric_dtype
# import numpy as np

# game_path = "C:/Retrosheet/api_data/final"
# weight_path = "C:/Retrosheet/FanGraphs"

# ### OBA weights dataframe
# df_weight = pd.read_csv(weight_path + "/wOBA_FIP_Constants.csv")
# df_weight.set_index("Season", drop=True, append=False, inplace=True, verify_integrity=False)


# dict_final = defaultdict()
# for index, file_nm in enumerate(file_names(game_path)):
#     print(file_nm)
#     key = file_nm.rsplit(".")[0]
#     file_path = game_path + "/" + file_nm
#     dict_final[key] = pd.read_csv(file_path)


# # ### gameData
# df_gameData = dict_final["gameData"]
# del_col = list(df_gameData)[0]
# del df_gameData[del_col]

# dt_prfx = "datetime"
# date_col = "originalDate"
# dt = dt_prfx + "." + date_col


# df_gameData[dt] = pd.to_datetime(df_gameData[dt])

# df_gameData[dt_prfx + ".year"] = df_gameData[dt].dt.year
# df_gameData[dt_prfx + ".month"] = df_gameData[dt].dt.month
# df_gameData[dt_prfx + ".day"] = df_gameData[dt].dt.day


# ### boxscore
# df_boxscore = dict_final["boxscore"]
# del_col = list(df_boxscore)[0]
# del df_boxscore[del_col]

# col_away = "away.teamStats.batting.runs"
# col_home = "home.teamStats.batting.runs"
# label = "home.result.target"

# ### helper functions for calculated fields
# ### label data
# def result(row):
#     if row[col_away] > row[col_home]:
#         val = False
#     elif row[col_away] < row[col_home]:
#         val = True
#     return val


# def pa(row, team, path, val=0):
#     df_path = team + path
#     list_attrb = [".atBats", ".baseOnBalls", ".hitByPitch", ".sacBunts", ".sacFlies", ".catchersInterference"]
#     for attrb in list_attrb:
#         val += row[df_path + attrb]
#     return val



# def single(row, team, path, val=0):
#     df_path = team + path
#     val = row[df_path + ".hits"]
#     list_attrb = [".doubles", ".triples", ".homeRuns"]
#     for attrb in list_attrb:
#         val -= row[df_path + attrb]
#     return val


# def ratio(row, team, path, numer, denom):
#     df_path = team + path
#     try:
#         return round(row[df_path + numer] / row[df_path + denom], 3)
#     except ZeroDivisionError:
#         return None


# def ratio_9(row, team, path, numer, denom):
#     df_path = team + path
#     try:
#         return round((row[df_path + numer] * 9) / row[df_path + denom], 3)
#     except ZeroDivisionError:
#         return None


# def babip(row, team, path, val=0):
#     df_path = team + path
#     numer = row[df_path + ".hits"] - row[df_path + ".homeRuns"]
#     denom = row[df_path + ".atBats"] - row[df_path + ".strikeOuts"] - row[df_path + ".homeRuns"] + row[df_path + ".sacFlies"]
#     try:
#         return round(numer / denom, 3)
#     except ZeroDivisionError:
#         return None


# def iso(row, team, path, val=0):
#     df_path = team + path
#     return row[df_path + ".slg"] - row[df_path + ".avg"]


# def wOBA(row, team, path, val=0):
#     """ calculate standard wOBA, dependent on singles """
#     w, s = [], []
#     df_path = team + path
#     year = row["datetime.year"]
#     col_nm = ["wBB", "wHBP", "w1B", "w2B", "w3B", "wHR"]
#     stat_nm = [".baseOnBalls", ".hitByPitch", ".singles", ".doubles", ".triples", ".homeRuns"]
#     for col in col_nm:
#         w.append(df_weight.loc[year, col])
#     for stat in stat_nm:
#         s.append(row[df_path + stat])
#     prod = sum([a*b for a,b in zip(s,w)])
#     denom = row[df_path + ".atBats"] + row[df_path + ".baseOnBalls"] - row[df_path + ".intentionalWalks"] + row[df_path + ".sacFlies"] + row[df_path + ".hitByPitch"]
#     try:
#         return round(prod / denom, 3)
#     except ZeroDivisionError:
#         return None


# def wRAA(row, team, path, val=0):
#     """ calculate standard wRAA, dependent on standard wOBA """
#     df_path = team + path
#     year = row["datetime.year"]
#     try: 
#         raa = round(((row[df_path + ".wOBA"] - df_weight.loc[year, "wOBA"]) / df_weight.loc[year, "wOBAScale"]) * row[df_path + ".pa"], 3)
#         return raa
#     except ZeroDivisionError:
#         return None


# def wRC(row, team, path, val=0):
#     df_path = team + path
#     year = row["datetime.year"]
#     try: 
#         rc = round((((row[df_path + ".wOBA"] - df_weight.loc[year, "wOBA"]) / df_weight.loc[year, "wOBAScale"]) + (df_weight.loc[year, "R/PA"])) * row[df_path + ".pa"], 3)
#         return rc
#     except ZeroDivisionError:
#         return None


# def fip_raw(row, team, path, val=0):
#     df_path = team + path
#     year = row["datetime.year"]
#     try: 
#         fip = ((row[df_path + ".homeRuns"] * 13) + ((row[df_path + ".baseOnBalls"] + row[df_path + ".hitBatsmen"]) * 3) - (row[df_path + ".strikeOuts"] * 2)) / row[df_path + ".inningsPitched"]
#         return fip
#     except ZeroDivisionError:
#         return None


# ### add calculated columns to dataframe
# df_boxscore[label] = df_boxscore.apply(result, axis=1)

# ### update path to bat path
# team_type = ["away", "home"]
# list_pct = [".baseOnBalls", ".strikeOuts"]
# path = ".teamStats.batting"

# print(df_boxscore.columns)

# ### add year to boxscore
# df_boxscore = pd.merge(df_boxscore, df_gameData[["gameID", "datetime.year"]], on="gameID", how="left")

# for team in team_type:
#     df_path = team + path
#     df_boxscore[df_path + ".pa"] = df_boxscore.apply(pa, axis=1, team=team, path=path)
#     df_boxscore[df_path + ".singles"] = df_boxscore.apply(single, axis=1, team=team, path=path)

#     for item in list_pct:
#         pct_path = df_path + item
#         df_boxscore[pct_path + "Pct"] = df_boxscore.apply(ratio, axis=1, team=team, path=path, numer=item, denom=".pa")

#     df_boxscore[df_path + ".bbkPct"] = df_boxscore.apply(ratio, axis=1, team=team, path=path, numer=".baseOnBalls", denom=".strikeOuts")
#     df_boxscore[df_path + ".babip"] = df_boxscore.apply(babip, axis=1, team=team, path=path)
#     df_boxscore[df_path + ".iso"] = df_boxscore.apply(iso, axis=1, team=team, path=path)
#     df_boxscore[df_path + ".wOBA"] = df_boxscore.apply(wOBA, axis=1, team=team, path=path)
#     df_boxscore[df_path + ".wRAA"] = df_boxscore.apply(wRAA, axis=1, team=team, path=path)
#     df_boxscore[df_path + ".wRC"] = df_boxscore.apply(wRC, axis=1, team=team, path=path)

# ### pitch stats
# ### batters faced, dependent on batting pa
# ### move up into loop for dependecies
# df_boxscore["away.teamStats.pitching.bf"], df_boxscore["home.teamStats.pitching.bf"] = df_boxscore["home.teamStats.batting.pa"], df_boxscore["away.teamStats.batting.pa"]

# # ### remove loop
# path_pit = ".teamStats.pitching"
# for team in team_type:
#     df_path_pit = team + path_pit
#     ### remove team or path variable
#     df_boxscore[df_path_pit + ".k9"] = df_boxscore.apply(ratio_9, axis=1, team=team, path=path_pit, numer=".strikeOuts", denom=".inningsPitched")
#     df_boxscore[df_path_pit + ".bb9"] = df_boxscore.apply(ratio_9, axis=1, team=team, path=path_pit, numer=".strikeOuts", denom=".baseOnBalls")
#     df_boxscore[df_path_pit + ".babip"] = df_boxscore.apply(babip, axis=1, team=team, path=path_pit)
#     df_boxscore[df_path_pit + ".fipRaw"] = df_boxscore.apply(fip_raw, axis=1, team=team, path=path_pit)


# ### finalize
# ### ad dteam loop
# df_final = df_boxscore

# del_col = ("away.note"
# , "away.team.allStarStatus"
# , "away.team.id"
# , "away.team.link"
# , "away.team.name"
# , "away.team.springLeague.abbreviation"
# , "away.team.springLeague.id"
# , "away.team.springLeague.link"
# , "away.team.springLeague.name"

# , "home.note"
# , "home.team.allStarStatus"
# , "home.team.id"
# , "home.team.link"
# , "home.team.name"
# , "home.team.springLeague.abbreviation"
# , "home.team.springLeague.id"
# , "home.team.springLeague.link"
# , "home.team.springLeague.name"

# , "datetime.year"

# , "away.teamStats.pitching.runs"
# , "home.teamStats.pitching.runs"
# , "away.teamStats.batting.runs"
# , "home.teamStats.batting.runs"
# , "away.teamStats.batting.rbi"
# , "home.teamStats.batting.rbi"
# , "away.teamStats.batting.totalBases"
# , "home.teamStats.batting.totalBases"
# , "away.teamStats.pitching.runsScoredPer9"
# , "home.teamStats.pitching.runsScoredPer9"
# , "away.teamStats.pitching.earnedRuns"
# , "home.teamStats.pitching.earnedRuns"

# , "away.teamStats.pitching.stolenBasePercentage"
# , "home.teamStats.pitching.stolenBasePercentage"
# , "away.teamStats.fielding.stolenBasePercentage"
# , "home.teamStats.fielding.stolenBasePercentage"
# , "away.teamStats.batting.stolenBasePercentage"
# , "home.teamStats.batting.stolenBasePercentage"

# , "away.teamStats.pitching.bb9"
# , "home.teamStats.pitching.bb9")

# df_final.drop([col for col in df_final.columns if col in del_col], axis=1, inplace=True)
# df_final.replace(".---", np.nan, inplace=True)
# df_final.sort_index(axis=1, inplace=True)
# cols = list(df_final)
# cols.insert(0, cols.pop(cols.index("home.result.target")))
# cols.insert(0, cols.pop(cols.index("gameID")))
# df_final = df_final.loc[:, cols]

# ### write pandas dataframe to excel
# file_nm = "final"
# save_to = "c:/retrosheet/api_structure_" + file_nm + ".xlsx"
# writer = pd.ExcelWriter(save_to)
# df_final.to_excel(writer,'Sheet1')
# writer.save()

# # file_nm = "gameData"
# # save_to = "c:/retrosheet/api_structure_" + file_nm + ".xlsx"
# # writer = pd.ExcelWriter(save_to)
# # df_gameData.to_excel(writer,'Sheet1')
# # writer.save()


