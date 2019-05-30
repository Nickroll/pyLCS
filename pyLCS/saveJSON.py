#!/usr/bin/env python

import sqlite3
from typing import Union


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


def make_sql_table(database: str=None, table_name: str=None, column_names: list=None) -> None:
    """make_sql_database

    Creates columns for a given table

    :param database (str): The database to connect to
    :param table_name (str): The table to create the column names for
    :param column_names (list): The list of tuples returned by get_columns
    :rtype None
    """

    conn = _make_database(database)
    _create_table(conn, table_name, column_names)

    conn.commit()
    conn.close()


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


def insert_stats(database: str=None, table_name: str=None, stats_data: dict=None) -> None:
    """insert_stats

    Well insert the stats into the SQL DB connection and table provided in the same order as the columns
    made in make_sql_table.

    :param database (str): The name of the SQLite3 Database
    :param table_name (str): The table name to insert the data into
    :param stats_data (dict): The stats returned by get_stats
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
