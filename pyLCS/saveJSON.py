#!/usr/bin/env python

import sqlite3
from typing import Union

import pandas


def flatten_json(y: dict=None) -> dict:
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


def _make_database(path: str=None) -> Union[sqlite3.Connection, None]:
    """_make_database

    Creates the sqlite3 database and returns the connection to it

    :param path (str): The path to the database to create
    :rtype Union(sqite3.Connection, None)
    """

    try:
        conn = sqlite3.connect(path)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None


def _create_table(conn: sqlite3.Connection=None, table_name: str=None) -> None:
    """_create_table

    Creates a table at the given sqlite connection passed to it

    :param conn (sqlite3.Connection): A database to create a table at
    :param table_name (str): The name of the table to create at the database
    :rtype None
    """

    SQL = f'CREATE TABLE IF NOT EXISTS {table_name}'

    try:
        c = conn.cursor()
        c.execute(SQL)
    except sqlite3.Error as e:
        print(e)


def _parse_player_json_data(json_data: dict=None) -> dict:
    """_parse_player_json_data

    Flattens the JSON file then pulls out all the players data and retuns it as a dict
    Example:
        {gameId: {TL Impact: [stats], TL Doublelift: [stats]}}

    :param json_data (dict): JSON data returned from the match history page
    :rtype dict
    """

    flat_json = flatten_json(json_data)
    ret_dict = {flat_json['gameId']: None}

    for i in range(0, 10):
        key = f'participantIdentities_{i}_player_summonerName'
        player_name = flat_json[key]
        stats_key = f'ants_{i}_'
        stats = list()

        for k, v in flat_json.items():
            if stats_key in k.lower():
                stats.append(v)

        ret_dict[player_name] = stats

    return ret_dict


def _column_names_match_hist(json_data: dict=None) -> list:
    """_column_names_match_hist

    Gets the names of the columns for the match history data

    :param json_data (dict): JSON data returned from the match history page
    :rtype list
    """

    flat_json = flatten_json(json_data)
    stats_key = f'ants_0_'
    ret_list = ['gameId']

    for k, _ in flat_json.items():
        if stats_key in k.lower():
            names = k.split('_')

            if 'Deltas' in names[-2]:
                ret_list.append(f'{names[-2]}_{names[-1]}')
            else:
                ret_list.append(names[-1])

    return ret_list
