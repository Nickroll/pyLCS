#!/usr/bin/env python
"""

"""

import json
from collections import defaultdict
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


def _format_matchHistory_players(json_data: dict=None) -> dict:
    """_format_matchHistory_players

    Formats the match history to {_id: gameID, {player1: [{stat1: value1}]}}

    :param json_data (dict): A dict in JSON-like style. Returned by matchCrawler.download_json_data
    :rtype dict
    """

    return_dict = {'_id': f"{json_data['MatchHistory']['gameId']}mh"}
    flat_mh = _flatten_json(json_data['MatchHistory'])

    for i in range(0, 10):
        key = f'participantIdentities_{i}_player_summonerName'
        player_name = flat_mh[key]
        stats_key = f'ants_{i}_'
        return_dict[player_name] = []

        for k, v in flat_mh.items():
            if stats_key in k.lower():
                if 'antid' not in k.lower()[-5:]:

                    # Role and lane are not listed correctly so they are useless
                    if 'role' in k.lower() or 'lane' in k.lower():
                        continue

                    # Deltas need to have more than just the last part of the key to make sense
                    s_key = k.split('_')
                    if 'Deltas' in s_key[-2]:
                        return_dict[player_name].append({f'{s_key[-2]}_{s_key[-1]}': v})
                    else:
                        return_dict[player_name].append({s_key[-1]: v})

    return return_dict


def _format_timeLine_players(json_data: dict=None, minute: int=15) -> dict:
    """_format_timeLine_players

    Formats the timeline information to {_id: gameID, {player1: {time0: [{stat1: value1}]}}

    :param json_data (dict): A json-like dict returned by matchCrawler.download_json_data
    :param minute (int): The last minute in time to gather data for
    :rtype dict
    """

    tl_data = json_data['Timeline']['frames']
    tl_return = defaultdict(dict)  # Easy dict nesting with for loop

    tl_return['_id'] = f"{json_data['MatchHistory']['gameId']}tl"

    for idx, time in enumerate(tl_data[:minute + 1]):
        for i in time['participantFrames']:
            tl_return[time['participantFrames'][i]['participantId'] - 1][idx] = time['participantFrames'][i]

            # Fix for pid as it differes from match history in the number here RITO PLS
            tl_return[time['participantFrames'][i]['participantId'] - 1][idx]['participantId'] -= 1

    pid_to_names = _make_pid_name_dict(json_data)

    for k, v in pid_to_names.items():
        tl_return[v] = tl_return.pop(k)

    return tl_return


def _make_pid_name_dict(json_data: dict=None) -> dict:
    """_make_pid_name_dict

    Creates a dictonary of {pid: playername} for easy conversion later

    :param json_data (dict): The JSON like dict returned from matchCrawler.download_json_data
    :rtype dict
    """

    return_dict = dict.fromkeys(range(0, 10))

    for k, _ in return_dict.items():
        return_dict[k] = json_data['MatchHistory']['participantIdentities'][k]['player']['summonerName']

    return return_dict
