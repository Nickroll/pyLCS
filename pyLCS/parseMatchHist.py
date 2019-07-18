#!/usr/bin/env python
"""
Functions that parse the match history JSON. The data is returned as a dict of
{gameId: [[player1], [player2]]}. The columns returned by get_columns are in the same order as the
values returned by get_stats. The values are kept seperate as they were designed to be used with an
sqlite3 db. However, the function merge_stats_and_column will create a new dict of
{Playername1: {stat1: value, stat2: value2}, Playername2: {stat1: value, stat2: value2}}
"""

import json
from typing import List, Union


def _flatten_json(y: dict=None) -> dict:
    """flatten_json

    Flattens a JSON to a single dict, take from:
        https://stackoverflow.com/questions/51359783/python-flatten-multilevel-json

    :param y (dict): The JSON dict to be flattened
    :rtype dict
    """
    out = dict()

    def flatten(x: Union[dict, list]=None, name: str=''):
        """flatten

        The actually flattening fucntion

        :param x (Union(dict, list)): A dict or list object to be flattened
        :param name (str): The name to append to the flattened object
        """
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '_')
        elif isinstance(x, list):
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def _parse_player_json_data(json_data: dict=None) -> dict:
    """_parse_player_json_data


    Flattens the JSON file then pulls out all the players data and retuns it as a dict
    Example:
        {gameId: {TL Impact: [stats], TL Doublelift: [stats]}}

    :param json_data (dict): JSON data returned from the match history page
    :rtype dict
    """

    cols = list()
    flat_json = _flatten_json(json_data)

    ret_dict = {flat_json['gameId']: []}

    for i in range(0, 10):
        key = f'participantIdentities_{i}_player_summonerName'
        player_name = flat_json[key]
        stats_key = f'ants_{i}_'
        stats = [player_name]
        stats.append(i)

        for k, v in flat_json.items():
            if stats_key in k.lower():
                if 'antid' not in k.lower()[-5:]:
                    if 'role' in k.lower() or 'lane' in k.lower():
                        continue
                    else:
                        stats.append(v)
                        cols.append(k)

        ret_dict[flat_json['gameId']].append(stats)

    return cols, ret_dict


def _column_names_match_hist(col_data: list=None) -> list:
    """_column_names_match_hist

    Gets the names of the columns for the match history data

    :param json_data (dict): Flat JSON data returned from the match history page
    :rtype list
    """

    stats_key = f'ants_0_'
    ret_list = ['gameId', 'participantId']

    for i in col_data:
        if stats_key in i:
            names = i.split('_')

            if 'Deltas' in names[-2]:
                ret_list.append(f'{names[-2]}_{names[-1]}')
            else:
                ret_list.append(names[-1])

    ret_list.append('PlayerName')
    return ret_list


def _create_column_name_and_type(column_name: list=None, stats_data: dict=None) -> list:
    """_create_column_name_and_type

    Creates a list of [(column_name, column_type)] for all the columns to be used with SQL

    :param column_name (list): The list of columns to be used in the SQL DB returned by _column_names_match_hist
    :param stats_data (dict): The dict returned by _parse_player_json_data
    :rtype list
    """

    ret_list = list()

    # This is a terrible hack that needs to be fixed at some point
    column_name.remove('PlayerName')
    column_name.remove('gameId')
    column_name.remove('lane')
    column_name.remove('role')

    stats = list(stats_data.values())[0][0][1:]
    tup_list = list(zip(column_name, stats))

    for tup in tup_list:
        name = tup[0]
        if isinstance(tup[1], (int, float)):
            col_type = 'real'
        else:
            col_type = 'text'

        ret_list.append((name, col_type))

    ret_list.extend([('gameId', 'real'), ('PlayerName', 'text')])

    return ret_list


def get_stats(json_data: Union[str, dict]=None) -> dict:
    """get_stats

    Takes either a JSON file, as str, or JSON data loaded via the JSON module. Will return the stats as:
        {gameId: [[Player 1 Stats], [Player 2 Stats]]}

    :param json_file (Union[str, dict]): The path to the JSON file containing the stats or the JSON dict
    :rtype dict
    """

    if isinstance(json_data, str):
        with open(json_data, 'r') as jf:
            data = json.load(jf)

    elif isinstance(json_data, dict):
        data = json_data

    else:
        raise TypeError(f'{type(json_data)} is wrong type, must be of type str or dict')

    _, stats = _parse_player_json_data(data)

    return stats


def get_columns(json_data: Union[str, dict]=None) -> List[tuple]:
    """get_columns

    Takes a JSON file or JSON data loaded via the JSON module and retuns the column names for use in the
    SQL table. Only needs to be run when creating the table the first time, or to check on the columns
    being created

    :param json_data (Union[str, dict]): The path to the JSON file or the JSON dict
    :rtype List[tuple]
    """

    if isinstance(json_data, str):
        with open(json_data, 'r') as jf:
            data = json.load(jf)

    elif isinstance(json_data, dict):
        data = json_data

    else:
        raise TypeError(f'{type(json_data)} is wrong type, must be of type str or dict')

    cols, stats = _parse_player_json_data(data)
    cols = _column_names_match_hist(cols)
    cols = _create_column_name_and_type(cols, stats)

    return cols


def merge_stats_and_column(stats: dict=None, cols: List[tuple]=None) -> dict:
    """merge_stats_and_column

    Merges the players column and stats into one dictonary:

    {Playername1: {stat1: value, stat2: value2}, Playername2: {stat1: value, stat2: value2}}

    :param stats (dict): The stats rturned by get_stats
    :param cols (List[tuple]): The column returned by get_column
    :rtype dict
    """

    keys = [i[0] for i in cols]
    ret_dict = dict()

    for k, v in stats.items():
        for i in v:
            values = i[1:]
            values.extend([k, i[0]])

            ret_dict[values[-1]] = dict(zip(keys, values))
            ret_dict[values[-1]].pop('PlayerName')

    return ret_dict
