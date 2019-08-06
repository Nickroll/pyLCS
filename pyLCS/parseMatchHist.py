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

    Formats the match history to {{player1: [{stat1: value1}]}}

    :param json_data (dict): A dict in JSON-like style. Returned by matchCrawler.download_json_data
    :rtype dict
    """

    flat_mh = _flatten_json(json_data['MatchHistory'])
    return_dict = dict()

    for i in range(0, 10):
        key = f'participantIdentities_{i}_player_summonerName'
        player_name = flat_mh[key]
        stats_key = f'ants_{i}_'
        return_dict[player_name] = {}

        for k, v in flat_mh.items():
            if stats_key in k.lower():
                if 'antid' not in k.lower()[-5:]:

                    # Role and lane are not listed correctly so they are useless
                    if 'role' in k.lower() or 'lane' in k.lower():
                        continue

                    # Deltas need to have more than just the last part of the key to make sense
                    s_key = k.split('_')
                    if 'Deltas' in s_key[-2]:
                        return_dict[player_name].update({f'{s_key[-2]}_{s_key[-1]}': v})
                    else:
                        return_dict[player_name].update({s_key[-1]: v})

    return return_dict


def _format_timeLine_players(json_data: dict=None, minute: int=15) -> dict:
    """_format_timeLine_players

    Formats the timeline information to {player1: {time0: [{stat1: value1}]}}

    :param json_data (dict): A json-like dict returned by matchCrawler.download_json_data
    :param minute (int): The last minute in time to gather data for
    :rtype dict
    """
    # TODO: Handle timelimits > game time

    tl_data = json_data['Timeline']['frames']
    tl_return = defaultdict(dict)  # Easy dict nesting with for loop

    pid_to_names = _make_pid_name_dict(json_data)

    for idx, time in enumerate(tl_data[:minute + 1]):
        for i in time['participantFrames']:
            tl_return[time['participantFrames'][i]['participantId'] - 1][idx] = time['participantFrames'][i]

            # Fix for pid as it differes from match history in the number here RITO PLS
            tl_return[time['participantFrames'][i]['participantId'] - 1][idx]['participantId'] = pid_to_names[tl_return[time['participantFrames'][i]['participantId'] - 1][idx]['participantId'] - 1]

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


def _parse_event_data_players(json_data: dict=None, timeline_data: dict=None, minute: int=15, unwanted_types: Union[set, list]={}) -> dict:
    """_parse_event_data_players

    Specifically parses the event data part of the timeline JSON information

    :param json_data (dict): The JSON-like dict rturned by matchCrawler.download_json_data
    :param timeline_data (dict): The dict returned from _format_timeLine_players
    :param minute (int): The last minute to collect data from
    :param unwanted_type (Union[set, list]): The unwanted event stats
    :rtype dict
    """

    frames = json_data['Timeline']['frames']
    ids_to_name = _make_pid_name_dict(json_data)

    for idx, i in enumerate(frames[:minute + 1]):
        for e in i['events']:
            if e['type'] not in unwanted_types:
                to_insert = {'event': e}

                # Ids need to be fixed again
                for k, v in e.items():
                    if k in ['killerId', 'creatorId', 'participantId']:
                        key_id = int(v) - 1
                        key_id = ids_to_name[key_id]

                    if 'Id' in k and k != 'itemId':
                        if isinstance(v, int):
                            to_insert['event'][k] = ids_to_name[v - 1]
                        elif isinstance(v, list):
                            updated_ids = [ids_to_name[pids - 1] for pids in v]
                            to_insert['event'][k] = updated_ids

                timeline_data[key_id][idx] = dict(timeline_data[key_id][idx], **to_insert)

            else:
                continue

    return timeline_data


def _game_information(json_data: dict=None) -> dict:
    """_game_information

    Retrieves basic game information like gameId, gameDuration, gameVersion and platformId

    :param json_data (dict): The full JSON dict returned my matchCrawler.download_json_data
    :rtype dict
    """

    data = json_data['MatchHistory']
    ret_dict = dict()
    for k, v in data.items():
        # The data here is just in k:v pair not nested in any way
        if isinstance(v, (dict, list)):
            continue
        else:
            ret_dict[k] = v

    return ret_dict


def _format_team_information(json_data: dict=None) -> dict:
    """_format_team_information

    Gets the basic team information form the JSON object

    :param json_data (dict): A JSON-like dict returned by matchCrawler.download_json_data
    :rtype dict
    """
    ret_data = dict()
    data = json_data['MatchHistory']['teams']

    team_0 = json_data['MatchHistory']['participantIdentities'][0]['player']['summonerName'].split(' ')[0]
    team_1 = json_data['MatchHistory']['participantIdentities'][9]['player']['summonerName'].split(' ')[0]

    ret_data[team_0] = data[0]
    ret_data[team_1] = data[1]

    return ret_data


def _merge_formats_together(match_history: dict, timeline: dict, team: dict, game_info: dict) -> dict:
    """_merge_formats_together

    Merges the previous JSON-like dicts together to create one master dict

    :param match_history (dict): The dict returned by _format_matchHistory_players
    :param timeline (dict): The dict returned by _format_timeLine_players
    :param team (dict): The dict returned by _format_team_information
    :param game_info (dict): The dict returned by _game_information
    :rtype dict
    """

    game_info['Players'] = match_history
    game_info['Team'] = team

    for p in game_info['Players']:
        game_info['Players'][p]['Minute'] = {}

    for k, v in timeline.items():
        game_info['Players'][k]['Minute'].update(v)

    return game_info


def parse_match_history(json_data: dict=None, minute: int=15, unwanted_types: Union[set, list]=None) -> dict:
    """parse_match_history

    Parse the match history datat that is returned by matchCrawler.download_json_data. The data is
    returned as a dict in a easier to read format and for insertion into a mongoDB. The format is
    JSON-like and can also be stored as a JSON object

    :param json_data (dict): The json-like dict from matchCrawler.download_json_data
    :param minute (int): The number of minutes you want timeline data for
    :param unwanted_types (Union[set, list]):
    :rtype dict
    """
