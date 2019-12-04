#!/usr/bin/env python
"""
Contains a LCS class which groups together all the funtions in insert, matchHistory,
downloadJson, and parse for ease of use. Also contains a funciton which calls
insert.insert_into_mongoDB to insert the data into a mongoDB
"""

import json
from typing import List, Union

from . import downloadJson, insert, matchHistory, mhParse


class LCS(object):

    def __init__(self, region: str=None, year: Union[str, int]=None, split: str=None, playoffs: bool=False):
        self._lc = matchHistory.matchHistory(region, year, split, playoffs)
        self._region_type = type(region)

    def _match_link_gen(self):
        """_match_link_gen

        Generates the match links using liquidCrawler.match_links
        """

        self._match_links = self._lc.match_links()

    def get_match_links(self) -> list:
        """match_links

        Returns the match links created by _match_link_gen
        rtype list
        """

        return self._match_links

    def _download_json(self):
        """_download_json

        Downloads the JSON data using downloadJson.download_json_data
        """

        self._json_data = downloadJson.download_json_data(self._match_links)

    def get_json_data(self) -> dict:
        """get_json_data

        If the JSON data is wanted as a return for self parsing
        :rtype dict
        """
        return self._json_data

    def match_history(self) -> None:
        """match_history

        Generates the match link data and downloads JSOn data using _match_link_gen and _download_json
        rtype None
        """

        self._match_link_gen()
        self._download_json()

        return None

    def parse_match_history(self, minute: Union[int, str]='max', unwanted_types: Union[set, list, tuple]=None) -> dict:
        """parse_match_history

        Parse the match history datat that is returned by downloadJson.download_json_data. The data is
        returned as a list of dicts in a easier to read format and for insertion into a mongoDB. The
        dict contiains headings Player, Team, Game. The player info is 1 json-like object per player,
        team is the same per team, and game is just the game info.

        :param minute (Union[int, str]): The number of minutes to parse for timeline data, or max for all
        :param unwanted_types (Union[set, list, tuple]): The unwatned event types, none returns all
        :rtype dict
        """

        output_data = mhParse.parse_MH(self._json_data, minute, unwanted_types)

        return output_data


def _format_for_mongo_data(merged_data: Union[str, List[dict]]=None) -> dict:
    """_format_for_mongo_data

    :param merged_data (Union[str, List[dict]]): The data from mhParse.parse_match_history
    :rtype dict
    """

    merged_data = json.dumps(merged_data)
    formatted = json.loads(merged_data)

    return formatted


def mongo_insert(merged_data: Union[str, List[dict]]=None, collection_set: str=None, database: str=None, collection: str=None, check: str=None) -> None:
    """mongo_insert

    Insertes data returned by pyLCS.parse_match_history into a mongoDB collection, to be run with
    known new data

    :param merged_data (Union[str, List[dict]): The data from mhParse.parse_match_history
    :param collection_set (str): One of players, team, or gameinfo
    :param database (str): The database  to insert into
    :param collection (str): The collection for insertion
    :param check (str): A string to use a check to ensure the document is not already in the collection
    :rtype None
    """

    print('Inserting Documents')
    formatted = _format_for_mongo_data(merged_data)
    insert.insert_into_mongoDB(formatted, collection_set, database, collection, check)

    return None
