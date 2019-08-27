import requests
import json
from datetime import date, datetime, timedelta
from operations import api_request, json_dump

# create list of dates, updated to use function
beg_dt = date(2018,4,1)
end_dt = date(2018,4,7)

date_list = [beg_dt + timedelta(days=x) for x in range((end_dt-beg_dt).days + 1)]

# api request to get game ids
dict_game_id = {}
for date in date_list:
    url = "http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date=" + date.strftime("%m/%d/%Y")
    data = api_request(url)
    for cnt in range(0,data["totalItems"]):
        key_game = data["dates"][0]["games"][cnt]["gamePk"]
        dict_game_id.setdefault(date.strftime("%Y-%m-%d"),[]).append(key_game)

dir_path = "C:/Retrosheet/api_data/game/game_id/game_id_"
path =  dir_path + beg_dt.strftime("%y%m%d") + "_" + end_dt.strftime("%y%m%d") + ".txt"
json_dump(dict_game_id, path)


# get game json and save to path
for key, value in dict_game_id.items():
    for key_game in sorted(value):
        ## get request to api
        url = "http://statsapi.mlb.com/api/v1.1/game/" + str(key_game) + "/feed/live"
        path = "C:/Retrosheet/api_data/game/intermediate/game_" + str(key_game) + ".txt"
        data = api_request(url)
        json_dump(data, path)
