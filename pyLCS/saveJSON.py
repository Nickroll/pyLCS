#!/usr/bin/env python

import sqlite3
from typing import Union
from warnings import warn

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


def _create_table(conn: sqlite3.Connection=None, table_name: str=None,
                  column_list: list=None)-> None:
    """_create_table

    Creates a table at the given sqlite connection passed to it

    :param conn (sqlite3.Connection): A database to create a table at
    :param table_name (str): The name of the table to create at the database
    :param column_list (list): A list of tuples containing (column name, type)
    :rtype None
    """

    SQL = f""" CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT)"""

    try:
        c = conn.cursor()
        c.execute(SQL)
    except sqlite3.Error as e:
        print(e)

    for tup in column_list:
        SQL = f"""ALTER TABLE {table_name} ADD COLUMN '{tup[0]}' {tup[1]}"""
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
    cols = list()
    flat_json = flatten_json(json_data)
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
                    stats.append(v)
                    cols.append(k)

        ret_dict[flat_json['gameId']].append(stats)

    return cols, ret_dict


def _column_names_match_hist(col_data: list=None) -> list:
    """_column_names_match_hist

    Gets the names of the columns for the match history data

    :param json_data (dict): JSON data returned from the match history page
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

    stats = list(stats_data.values())[0][0][1:]
    tup_list = list(zip(column_name, stats))

    for tup in tup_list:
        name = tup[0]
        if isinstance(tup[1], int):
            col_type = 'real'
        else:
            col_type = 'text'

        ret_list.append((name, col_type))

    ret_list.extend([('gameId', 'real'), ('PlayerName', 'text')])

    return ret_list


def _fix_for_sql_instertion(stats_data: dict=None) -> list:
    """_fix_for_sql_instertion

    Fixes the order of the list for insertion into the SQLite DB

    :param stats_data (dict): The stats dict that is returned by _parse_player_json_data
    :rtype list
    """

    fixed_insert = list()

    for k, v in stats_data.items():
        for i in v:
            tmp_fix = i[1:]
            tmp_fix.extend([k, i[0]])

            fixed_insert.append(tuple(tmp_fix))

    return fixed_insert


def make_sql_table(database: str=None, table_name: str=None, column_names: list=None) -> None:
    """make_sql_database

    Creates columns for a given table

    :param database (str): The database to connect to
    :param table_name (str): The table to create the column names for
    :param column_names (list): The list of tuples returned by _create_column_name_and_type
    :rtype None
    """

    conn = _make_database(database)
    _create_table(conn, table_name, column_names)
    conn.close()


def insert_stats(database: str=None, table_name: str=None, stats_data: dict=None) -> None:
    """insert_stats

    Well insert the stats into the SQL DB connection and table provided

    :param database (str): The name of the SQLite3 Database
    :param table_name (str): The table name to insert the data into
    :param stats_data (dict): The stats returned by _parse_player_json_data
    :rtype None
    """

    correct_insert = _fix_for_sql_instertion(stats_data)
    conn = _make_database(database)

    SQL = f"""INSERT INTO {table_name} VALUES (null, {'?,'*len(correct_insert[0])}"""
    SQL = f"""{SQL[:-1]})"""

    c = conn.cursor()
    c.executemany(SQL, correct_insert)

    conn.commit()
    conn.close()
