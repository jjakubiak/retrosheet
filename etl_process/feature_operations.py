
import pandas as pd
import numpy as np

### helper functions for calculated fields


def result(row, col_away, col_home):
    """ label data based on home team win """
    if row[col_away] > row[col_home]:
        val = False
    elif row[col_away] < row[col_home]:
        val = True
    return val


def pa(row, team, path, val=0):
    df_path = team + path
    list_attrb = [".atBats", ".baseOnBalls", ".hitByPitch", ".sacBunts", ".sacFlies", ".catchersInterference"]
    for attrb in list_attrb:
        val += row[df_path + attrb]
    return val


def single(row, team, path, val=0):
    df_path = team + path
    val = row[df_path + ".hits"]
    list_attrb = [".doubles", ".triples", ".homeRuns"]
    for attrb in list_attrb:
        val -= row[df_path + attrb]
    return val


def ratio(row, team, path, numer, denom):
    df_path = team + path
    try:
        return round(row[df_path + numer] / row[df_path + denom], 3)
    except ZeroDivisionError:
        return None


def ratio_9(row, team, path, numer, denom):
    df_path = team + path
    try:
        return round((row[df_path + numer] * 9) / row[df_path + denom], 3)
    except ZeroDivisionError:
        return None


def babip(row, team, path, val=0):
    df_path = team + path
    numer = row[df_path + ".hits"] - row[df_path + ".homeRuns"]
    denom = row[df_path + ".atBats"] - row[df_path + ".strikeOuts"] - row[df_path + ".homeRuns"] + row[df_path + ".sacFlies"]
    try:
        return round(numer / denom, 3)
    except ZeroDivisionError:
        return None


def iso(row, team, path, val=0):
    df_path = team + path
    return row[df_path + ".slg"] - row[df_path + ".avg"]


def wOBA(row, team, path, df_weight, val=0):
    """ calculate standard wOBA, dependent on singles """
    w, s = [], []
    df_path = team + path
    year = row["datetime.year"]
    col_nm = ["wBB", "wHBP", "w1B", "w2B", "w3B", "wHR"]
    stat_nm = [".baseOnBalls", ".hitByPitch", ".singles", ".doubles", ".triples", ".homeRuns"]
    for col in col_nm:
        w.append(df_weight.loc[year, col])
    for stat in stat_nm:
        s.append(row[df_path + stat])
    prod = sum([a*b for a,b in zip(s,w)])
    denom = row[df_path + ".atBats"] + row[df_path + ".baseOnBalls"] - row[df_path + ".intentionalWalks"] + row[df_path + ".sacFlies"] + row[df_path + ".hitByPitch"]
    try:
        return round(prod / denom, 3)
    except ZeroDivisionError:
        return None


def wRAA(row, team, path, df_weight, val=0):
    """ calculate standard wRAA, dependent on standard wOBA """
    df_path = team + path
    year = row["datetime.year"]
    try: 
        raa = round(((row[df_path + ".wOBA"] - df_weight.loc[year, "wOBA"]) / df_weight.loc[year, "wOBAScale"]) * row[df_path + ".pa"], 3)
        return raa
    except ZeroDivisionError:
        return None


def wRC(row, team, path, df_weight, val=0):
    df_path = team + path
    year = row["datetime.year"]
    try: 
        rc = round((((row[df_path + ".wOBA"] - df_weight.loc[year, "wOBA"]) / df_weight.loc[year, "wOBAScale"]) + (df_weight.loc[year, "R/PA"])) * row[df_path + ".pa"], 3)
        return rc
    except ZeroDivisionError:
        return None


def fip_raw(row, team, path, val=0):
    df_path = team + path
    try: 
        fip = round(((row[df_path + ".homeRuns"] * 13) + ((row[df_path + ".baseOnBalls"] + row[df_path + ".hitBatsmen"]) * 3) - (row[df_path + ".strikeOuts"] * 2)) / row[df_path + ".inningsPitched"], 3)
        return fip
    except ZeroDivisionError:
        return None


### general operations
def cast(df, cast_col, data_type):
    return df[cast_col].astype(data_type)


def replace_with_null(df, null_str):
    return df.replace(null_str, np.nan, inplace=True)