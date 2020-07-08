#!/usr/bin/env python
"""
Contains the functions necessary to create the links to the JSON data from the match history links
provided to it. The data is then downloaded in JSON form
"""

from typing import Union
from warnings import warn

from .connection import create_connection


def _create_json_links(link: str=None) -> Union[tuple, None]:
    """_create_json_links

    Uses the match link to make the JSON links for the match history data

    Example:

        Input:
            https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/992625?gameHash=76f99e0eb8658976
        Output:
            https://acs.leagueoflegends.com/v1/stats/game/ESPORTSTMNT02/992625?gameHash=76f99e0eb8658976
            https://acs.leagueoflegends.com/v1/stats/game/ESPORTSTMNT02/992625/timeline?gameHash=76f99e0eb86589

    :param link (str): The link to convert to match history and timeline links
    :rtype Union[tuple, None]: (match_history, timelines)
    """

    acs_base = 'https://acs.leagueoflegends.com/v1/stats/game'

    relm_part = link.find('ESPORTSTMNT')

    # Finds the location of the ? and slices the string
    if relm_part != -1:
        q_loc = link.find('?')

        if q_loc != -1:
            post_link = link[relm_part:q_loc]
            hash_part = link[q_loc + 1:]

            match_history = f'{acs_base}/{post_link}?{hash_part}'
            timelines = f'{acs_base}/{post_link}/timeline?{hash_part}'

            return (match_history, timelines)

        else:
            warn(f'{link} is not a valid post match link')
            return (None, None)
    else:
        warn(f'{link} is not a valid post match link')
        return (None, None)


def download_json_data(match_links: Union[list, str]=None) -> list:
    """download_json_data

    Downloads the JSON data from the match links provided

    :param match_link (Union[list, str]): The links to the match history page
    :rtype list
    """

    return_list = list()

    if not isinstance(match_links, list):
        match_links = [match_links]

    for l in match_links:

        tmp_dict = dict()
        match_history, timelines = _create_json_links(l)
        tmp_dict['MatchHistory'] = create_connection(match_history, json=True)
        tmp_dict['Timeline'] = create_connection(timelines, json=True)
        return_list.append(tmp_dict)

    return return_list

