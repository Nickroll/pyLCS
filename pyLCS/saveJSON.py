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
