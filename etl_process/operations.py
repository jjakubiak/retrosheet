

from datetime import date, timedelta
import requests
import json
import os
from os import walk
from os.path import join
import pandas as pd
from pandas import ExcelWriter
from collections import defaultdict
import shutil


def api_request(url_path):
    """ get request from api, returns raw json """
    response = requests.get(url_path)
    return json.loads(response.content)


def json_dump(data, file_path):
    """ dump raw json file to drive"""
    with open(file_path, 'w') as outfile:  
        json.dump(data, outfile)


def json_load(file_path):
    """ return raw json file from drive"""
    with open(file_path) as json_file:  
        return json.load(json_file)


def date_rng(beg_dt, end_dt):
    """ date input format: YYYY-MM-DD """
    beg_dt = beg_dt.split("-")
    beg_dt = date(int(beg_dt[0]), int(beg_dt[1]), int(beg_dt[2]))

    end_dt = end_dt.split("-")
    end_dt = date(int(end_dt[0]), int(end_dt[1]), int(end_dt[2]))

    date_list = [beg_dt + timedelta(days=x) for x in range((end_dt-beg_dt).days + 1)]
    return date_list


def file_names(path, dirpath="", dirnames=""):
    """ return list of file names from directory """
    lst_file = []
    for (dirpath, dirnames, filenames) in walk(path):
        lst_file.extend(filenames)
        return lst_file


def file_paths(path):
    """ return dict of lists, kays as file paths and values as files names"""
    allfiles = {path: files for path, dirs, files in walk(path) for f in files}
    return(allfiles)



def map_keys(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from map_keys(v, path + "." + k if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            s = str(i)
            yield from map_keys(v, path + "." + s if path else s)
    else:
        yield path


def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


def get_item(response, path):
    for item in path:
            response = response[item]
    return response


def save_dataframe_csv(dataframe, path, file_name):
    # dataframe.to_csv(path + file_name + ".txt", index=False)
    dataframe.to_csv(path + file_name + ".txt")


def save_dataframe_pkl(dataframe, path, file_name):
    """ writing to pickle preserves the indicies and data types """
    dataframe.to_pickle(path + file_name + ".pkl")


def df_output(dict_obj, var_nm, game_id, save_path):
    col_nm = [v.name for k, v in dict_obj.items()]
    series_lst = [v for k, v in dict_obj.items()]
    df = pd.concat(series_lst, axis=1, keys=col_nm, sort=False, copy=False)

    save_dataframe_csv(df, save_path + var_nm + "/", var_nm + "_" + str(game_id))


def df_output_pkl(dict_obj, var_nm, game_id, save_path):
    col_nm = [v.name for k, v in dict_obj.items()]
    series_lst = [v for k, v in dict_obj.items()]
    df = pd.concat(series_lst, axis=1, keys=col_nm, sort=False, copy=False)

    save_dataframe_pkl(df, save_path + var_nm + "/", var_nm + "_" + str(game_id))

# def read_pickle(data, path, file_name):
#     return pd.read_pickle(path + file_name + ".pkl")

### write pandas dataframe to excel
def df_to_excel(file_nm, path, dataframe):
    save_to = path + "_" + file_nm + ".xlsx"
    writer = ExcelWriter(save_to)
    dataframe.to_excel(writer, file_nm)
    writer.save()


def rev_slash(string):
    return string.replace(os.sep, '/')


def remove_files(path):
    for parent, dirnames, filenames in os.walk(path):
        for fn in filenames:
            if fn.lower().endswith('.txt') or fn.lower().endswith('.pkl'):
                os.remove(os.path.join(parent, fn))
            
