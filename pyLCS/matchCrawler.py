#!/usr/bin/env python
"""
Contains the functions necessary to create the links to the JSON data from the match history links
provided to it. The data is then downloaded in JSON form and returned as a
{match_history: info, timeline: info}
"""
from time import sleep
from typing import Union
from warnings import warn

from requests_html import HTMLSession


def _create_json_links(link: str=None) -> Union[tuple, None]:
    """_create_json_links

    Uses the match link to make the JSON links for the match history data

    Example: https://acs.leagueoflegends.com/v1/stats/game/ESPORTSTMNT02/992625?gameHash=76f99e0eb8658976
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

            timelines = f'{acs_base}/{post_link}/timeline?{hash_part}'
            match_history = f'{acs_base}/{post_link}?{hash_part}'

            return (match_history, timelines)

        else:
            warn(f'{link} is not a valid post match link')
            return (None, None)
    else:
        warn(f'{link} is not a valid post match link')
        return (None, None)


def _json_retrival(link: str=None) -> Union[dict, None]:
    """_json_retrival

    Retrieves the JSON form the link provided and returns the dicts in a list

    :param link (str): The link to get the JSON data from
    :rtype Union[dict, None]
    """

    session = HTMLSession()

    r = session.get(link)

    if r.ok:
        return r.json()

    # One retry just incase of an internet hiccup
    else:
        warn('Unable to get a response, sleeping for 5 seconds and then re-trying link'
             f'{link} after 5 seconds.')
        sleep(5)
        to_rerun = link

    if to_rerun:
        r = session.get(link)

    if r.ok:
        return r.json()
    else:
        warn(f'Unable to retrieve data for {link}. None was inserted into response')
        return None


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
        tmp_dict['MatchHistory'] = _json_retrival(match_history)
        tmp_dict['Timeline'] = _json_retrival(timelines)
        return_list.append(tmp_dict)

    return return_list
