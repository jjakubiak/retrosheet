### etl proccess, rename folder
from operations import json_load, file_names, map_keys, check_int, get_item, df_output, save_dataframe_csv
import pandas as pd
from collections import defaultdict
from pandas.io.json import json_normalize
import pandas as pd
import shutil

path_nm = "C:/Retrosheet/api_data/game/intermediate/"
to_path = "C:/Retrosheet/api_data/game/complete/"
save_path = "C:/Retrosheet/api_data/parsed/intermediate/"

game_id_key = ["gameData", "game", "pk"]


for index, file_nm in enumerate(file_names(path_nm)):
    print(file_nm)

    distinct_series_pevnt = set()
    distinct_series_runnr = set()
    distinct_series_crdt = set()
    distinct_series_pindx = set()
    distinct_series_rindx = set()
    distinct_series_main = set()

    dict_pevnt = defaultdict(list)
    dict_runnr = defaultdict(list)
    dict_crdt = defaultdict(list)
    dict_pindx = defaultdict(list)
    dict_rindx = defaultdict(list)
    dict_main = defaultdict(list)
    dict_final = defaultdict(dict)

    dir_path = path_nm + file_nm
    json_raw = json_load(dir_path)

    ### filter json on specific path
    json_data = json_raw["liveData"]["plays"]["allPlays"]

    ### map all parent child relationships
    ### create list of all json object paths
    json_map = map_keys(json_data)
    list_map = list(json_map)
    game_id = get_item(json_raw, game_id_key)

    ### split list_map by serperator
    split_path = [item.split(".") for item in list_map]

    ### replace string integers with integer values
    for i, item in enumerate(split_path):
        for v, val in enumerate(item):
            if check_int(val):
                split_path[i][v] = int(val)

    ### dict of all key value pairs where keys are json object path
    dict_series = {}
    for item in split_path:
        dict_series[tuple(item)] = get_item(json_data, item)


    #### player data
    pl = "players"
    gm = "gameData"
    json_data_pl = json_raw[gm][pl]

    ### loop through players data
    list_pl = []
    for k , v in json_data_pl.items():
        df_data_pl = json_normalize(data=v)
        index = str(game_id) + "-" + k
        df_data_pl.insert(0,"index", index, True)
        df_data_pl.set_index("index", inplace=True, drop=True)

        list_pl.append(df_data_pl)

    df_all_pl = pd.concat(list_pl, sort=True)
    

    ### game data
    gmID = "gameID"
    json_data_gm = json_raw[gm]
    df_data_gm = json_normalize(data=json_data_gm)

    ### game data remove all players data
    df_data_gm.drop(list(df_data_gm.filter(regex = pl)), axis = 1, inplace = True)

    df_data_gm.insert(0,gmID, game_id, True)
    df_data_gm.set_index(gmID, inplace=True, drop=True)


    ### boxscorce
    livedata = "liveData"
    bxscr = "boxscore"
    tms = "teams"
    bx_rmv = ["players", "batters", "pitchers", "bench", "bullpen", "battingOrder", "info", "notes"]
    json_data_bx = json_raw[livedata][bxscr][tms]
    df_data_bx = json_normalize(data=json_data_bx)

    ### boxscore remove all list data
    for i in bx_rmv:
        df_data_bx.drop(list(df_data_bx.filter(regex = i)), axis = 1, inplace = True)

    df_data_bx.insert(0, gmID, game_id, True)
    df_data_bx.set_index(gmID, inplace=True, drop=True)


    for k, v in dict_series.items():

        ### playEvents
        pevnt = "playEvents"
        if k[1] in set([pevnt]):
            key_pevnt = '.'.join(map(str, k[3:]))
            index_pevnt = str(game_id) + "-" + str(k[0]) + "-" + str(k[2])

            if key_pevnt not in distinct_series_pevnt:
                distinct_series_pevnt.add(key_pevnt)
                dict_pevnt[key_pevnt] = pd.Series(v, index=[index_pevnt], name=key_pevnt)
            else:
                s_pevnt = pd.Series(v, index=[index_pevnt], name=key_pevnt)
                dict_pevnt[key_pevnt] = dict_pevnt[key_pevnt].append(s_pevnt)

        ### runners
        runnr_01, runnr_02, runnr_03 = "runners", "movement", "details"
        if k[1] in set([runnr_01]) and k[3] in set([runnr_02, runnr_03]):
            key_runnr = '.'.join(map(str, k[3:]))
            index_runnr = str(game_id) + "-" + str(k[0]) + "-" + str(k[2])

            if key_runnr not in distinct_series_runnr:
                distinct_series_runnr.add(key_runnr)
                dict_runnr[key_runnr] = pd.Series(v, index=[index_runnr], name=key_runnr)
            else:
                s_runnr = pd.Series(v, index=[index_runnr], name=key_runnr)
                dict_runnr[key_runnr] = dict_runnr[key_runnr].append(s_runnr)


        ### runners credits
        crdt = "credits"
        if k[1] in set([runnr_01]) and k[3] in set([crdt]):
            key_crdt = '.'.join(map(str, k[5:]))
            index_crdt = str(game_id) + "-" + str(k[0]) + "-" + str(k[2]) + "-" + str(k[4])

            if key_crdt not in distinct_series_crdt:
                distinct_series_crdt.add(key_crdt)
                dict_crdt[key_crdt] = pd.Series(v, index=[index_crdt], name=key_crdt)
            else:
                s_crdt = pd.Series(v, index=[index_crdt], name=key_crdt)
                dict_crdt[key_crdt] = dict_crdt[key_crdt].append(s_crdt)


        ### pitchIndex
        pindx = "pitchIndex"
        if k[1] in set([pindx]):
            index_pindx = str(game_id) + "-" + str(k[0]) + "-" + str(k[2])

            if pindx not in distinct_series_pindx:
                distinct_series_pindx.add(pindx)
                dict_pindx[pindx] = pd.Series(v, index=[index_pindx], name=pindx)
            else:
                s_pindx = pd.Series(v, index=[index_pindx], name=pindx)
                dict_pindx[pindx] = dict_pindx[pindx].append(s_pindx)


        ### runnerIndex
        rindx = "runnerIndex"
        if k[1] in set([rindx]):
            index_rindx = str(game_id) + "-" + str(k[0]) + "-" + str(k[2])

            if rindx not in distinct_series_rindx:
                distinct_series_rindx.add(rindx)
                dict_rindx[rindx] = pd.Series(v, index=[index_rindx], name=rindx)
            else:
                s_rindx = pd.Series(v, index=[index_rindx], name=rindx)
                dict_rindx[rindx] = dict_rindx[rindx].append(s_rindx)


        ### main
        main = "main"
        main_01, main_02, main_03, main_04 = "result", "about", "count", "matchup"
        main_05, main_06, main_07, main_08 = "batterHotColdZones", "pitcherHotColdZones",  "batterHotColdZoneStats", "pitcherHotColdZoneStats"
        if k[1] in set([main_01, main_02, main_03, main_04]) and k[2] not in set([main_05, main_06, main_07, main_08]):
            key_main = '.'.join(map(str, k[1:]))
            indx = str(game_id) + "-" + str(k[0])
            if key_main not in distinct_series_main:
                distinct_series_main.add(key_main)
                dict_main[key_main] = pd.Series(v, index=[indx], name=key_main)
            else:
                s_main = pd.Series(v, index=[indx], name=key_main)
                dict_main[key_main] = dict_main[key_main].append(s_main)

    ### write dataframes to disk
    df_output(dict_pevnt, pevnt, game_id, save_path)
    df_output(dict_runnr, runnr_01, game_id, save_path)
    df_output(dict_crdt, crdt, game_id, save_path)
    df_output(dict_pindx, pindx, game_id, save_path)
    df_output(dict_rindx, rindx, game_id, save_path)
    df_output(dict_main, main, game_id, save_path)

    save_dataframe_csv(df_data_gm, save_path + "gameData/", "gameData_" + str(game_id))
    save_dataframe_csv(df_all_pl, save_path + "players/", "players_" + str(game_id))
    save_dataframe_csv(df_data_bx, save_path + "boxScore/", "boxScore_" + str(game_id))

    ### move files from staging to complete directory
    from_path = path_nm + "game_" + str(game_id) + ".txt"
    to_path = "C:/Retrosheet/api_data/game/complete/" + "game_" + str(game_id) + ".txt"
    shutil.move(from_path, to_path)