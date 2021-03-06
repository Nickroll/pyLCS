#!/usr/bin/env python
"""
Contains the funcitons necessary to parse the match history data returned by the matchCrawler set of
functions. Data is returned in a JSON-like form.
"""
import operator
from collections import defaultdict
from functools import reduce
from typing import List, Union
from warnings import warn

from .exceptions import pyLCSExceptions


def _test_for_key(data_dict: dict, key_list: list) -> Union[dict, None]:
    """_test_for_key

    Tests to see if the key is in the dict. If not it returns None

    :param data_dict (dict): The dict to test for a given key
    :param key_list (list): A list of keys to test
    :rtype Union[dict, None]
    """

    try:
        data = reduce(operator.getitem, key_list, data_dict)
        return data
    except Exception:
        return None


def _flatten_json(y: dict=None) -> dict:
    """flatten_json

    Flattens a JSON to a single dict, take from:
        https://stackoverflow.com/questions/51359783/python-flatten-multilevel-json

    :param y (dict): The JSON dict to be flattened
    :rtype dict
    """
    if y is None:
        return None

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


def _add_roles(return_dict: dict, player_name: str, i: int) -> dict:
    """_add_roles

    Since roles are broken on the match history this adds them manually

    :param return_dict (dict): The dict to be retruned at the end of _format_matchHistory_players
    :param player_name (str): The player name to get the role
    :param i (int): The int corresponding to the players position
    :rtype dict
    """

    role_dict = {0: 'Top', 1: 'Jungle', 2: 'Middle', 3: 'ADC', 4: 'Support'}

    if i < 5:
        return_dict[player_name] = {'role': role_dict[i]}
    else:
        return_dict[player_name] = {'role': role_dict[i - 5]}

    return return_dict


def _format_matchHistory_players(json_data: dict) -> Union[dict, None]:
    """_format_matchHistory_players

    Formats the match history to {{player1: [{stat1: value1}]}}

    :param json_data (dict): A dict in JSON-like style. Returned by matchCrawler.download_json_data
    :rtype Union[dict, None]
    """

    return_dict = dict()

    flat_mh = _flatten_json(_test_for_key(json_data, ['MatchHistory']))

    if flat_mh is None:
        warn('JSON data lacked a MatchHistory key meaning it was not returned by'
             'matchCralwer.download_json_data, None returned')
        return None

    # There should always be 10 players in a game, extra check
    if len(json_data['MatchHistory']['participantIdentities']) != 10:
        raise pyLCSExceptions.InvalidPlayerAmount('The number of players in the game is not 10'
                                                  f"it is {len(json_data['MatchHistory']['participantIdentities'])}")

    for i in range(0, 10):
        key = f'participantIdentities_{i}_player_summonerName'
        try:
            player_name = flat_mh[key]
            stats_key = f'ants_{i}_'

            # Since roles are broken we will add them manually
            return_dict = _add_roles(return_dict, player_name, i)

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

                        # Team ID is unhelpfully 100 or 200 so we just replace
                        elif 'teamId' in s_key[-1]:
                            team = player_name.split(' ')[0]
                            return_dict[player_name].update({s_key[-1]: team})
                        else:
                            return_dict[player_name].update({s_key[-1]: v})
        except KeyError:
            warn('The JSON data returned did not have the necessary information, None returned')
            return None

    return return_dict


def _format_timeLine_players(json_data: dict, minute: Union[int, str]) -> Union[dict, None]:
    """_format_timeLine_players

    Formats the timeline information to {player1: {time0: [{stat1: value1}]}}

    :param json_data (dict): A json-like dict returned by matchCrawler.download_json_data
    :param minute (Union[int, str]): The last minute in time to gather data for or max for all data
    :rtype Union[dict, None]
    """

    tl_data = _test_for_key(json_data, ['Timeline', 'frames'])

    if tl_data is None:
        warn('JSON data did not contain Timeline or frames. Was the data from'
             'matchCrawler.download_json_data. None returned')
        return None

    tl_return = defaultdict(dict)  # Easy dict nesting with for loop
    pid_to_names = _make_pid_name_dict(json_data)

    for idx, time in enumerate(tl_data[:minute]):
        for i in time['participantFrames']:
            tl_return[time['participantFrames'][i]['participantId'] - 1][idx] = time['participantFrames'][i]

            # Fix for pid as it differes from match history in the number here RITO PLS
            tl_return[time['participantFrames'][i]['participantId'] - 1][idx]['participantId'] = pid_to_names[tl_return[time['participantFrames'][i]['participantId'] - 1][idx]['participantId'] - 1]

    # Repalce ids with name
    for k, v in pid_to_names.items():
        tl_return[v] = tl_return.pop(k)

    return tl_return


def _make_pid_name_dict(json_data: dict) -> dict:
    """_make_pid_name_dict

    Creates a dictonary of {pid: playername} for easy conversion later

    :param json_data (dict): The JSON like dict returned from matchCrawler.download_json_data
    :rtype dict
    """

    return_dict = dict.fromkeys(range(0, 10))

    for k, _ in return_dict.items():
        return_dict[k] = json_data['MatchHistory']['participantIdentities'][k]['player']['summonerName']

    return return_dict


def _parse_event_data_players(json_data: dict, timeline_data: dict, minute: Union[int, str], unwanted_types: Union[set, list]) -> Union[dict, None]:
    """_parse_event_data_players

    Specifically parses the event data part of the timeline JSON information

    :param json_data (dict): The JSON-like dict rturned by matchCrawler.download_json_data
    :param timeline_data (dict): The dict returned from _format_timeLine_players
    :param minute (Union[int, str]): The last minute to collect data from or max for all
    :param unwanted_type (Union[set, list]): The unwanted event stats
    :rtype Union[dict, None]
    """

    frames = _test_for_key(json_data, ['Timeline', 'frames'])

    if frames is None:
        warn('JSON data did not contain Timeline or frames. Was the data from'
             'matchCrawler.download_json_data. None returned')
        return None

    ids_to_name = _make_pid_name_dict(json_data)

    for idx, i in enumerate(frames[:minute]):
        for e in i['events']:
            if e['type'] not in unwanted_types:
                to_insert = {'event': e}

                # Ids need to be fixed again
                for k, v in e.items():
                    key_id = None

                    # For the creator or the killer (aka who the stat goes under)
                    if k in ['killerId', 'creatorId', 'participantId']:

                        # Checks to make sure minions are not the spawner as there id is 0
                        if int(v) == 0:
                            continue
                        else:
                            key_id = int(v) - 1

                        key_id = ids_to_name[key_id]
                        team = key_id.split(' ')[0]

                    if k == 'teamId':
                        to_insert['event'][k] = team

                    if 'Id' in k and k not in ['itemId', 'teamId']:
                        if isinstance(v, int):
                            to_insert['event'][k] = ids_to_name[v - 1]
                        elif isinstance(v, list):
                            updated_ids = [ids_to_name[pids - 1] for pids in v]
                            to_insert['event'][k] = updated_ids

                    if key_id:

                        # Fixing the time as it is in milisecondsa
                        to_insert['event']['timestamp'] /= 1000
                        minutes = to_insert['event']['timestamp'] / 60
                        seconds = int(round(minutes % 1 * 60, 0))
                        to_insert['event']['timestamp'] = float(f'{int(minutes)}.{seconds}')

                        timeline_data[key_id][idx] = dict(timeline_data[key_id][idx], **to_insert)

            else:
                continue

    return timeline_data


def _game_information(json_data: dict) -> Union[dict, None]:
    """_game_information

    Retrieves basic game information like gameId, gameDuration, gameVersion and platformId

    :param json_data (dict): The full JSON dict returned my matchCrawler.download_json_data
    :rtype Union[dict, None]
    """

    data = _test_for_key(json_data, ['MatchHistory'])

    if data is None:
        warn('JSON data did not have a MatchHistory key. Was it created by'
             'matchCrawler.download_json_data? None returned')
        return None

    ret_dict = dict()
    for k, v in data.items():

        # The data here is just in k:v pair not nested in any way
        if isinstance(v, (dict, list)):
            continue
        else:
            ret_dict[k] = v

    # Fixing game duration
    minutes = ret_dict['gameDuration'] / 60
    seconds = int(round(minutes % 1 * 60, 0))
    ret_dict['gameDuration'] = float(f'{int(minutes)}.{seconds}')

    return ret_dict


def _format_team_information(json_data: dict) -> Union[dict, None]:
    """_format_team_information

    Gets the basic team information form the JSON object

    :param json_data (dict): A JSON-like dict returned by matchCrawler.download_json_data
    :rtype Union[dict, None]
    """
    ret_data = dict()

    data = _test_for_key(json_data, ['MatchHistory', 'teams'])

    if data is None:
        warn('JSON data did not have MatchHistory team information. Was the data created by'
             'matchCrawler.download_json_data? None returned')
        return None

    team_0 = json_data['MatchHistory']['participantIdentities'][0]['player']['summonerName'].split(' ')[0]
    team_1 = json_data['MatchHistory']['participantIdentities'][9]['player']['summonerName'].split(' ')[0]

    ret_data[team_0] = data[0]
    ret_data[team_1] = data[1]

    ret_data[team_0]['teamId'] = team_0
    ret_data[team_1]['teamId'] = team_1

    return ret_data


def _merge_formats_together(match_history: dict, event_data: dict, team: dict) -> dict:
    """_merge_formats_together

    Merges the previous JSON-like dicts together to create one master dict

    :param match_history (dict): The dict returned by _format_matchHistory_players
    :param event_data (dict): The dict returned by _parse_event_data_players
    :param team (dict): The dict returned by _format_team_information
    :rtype dict
    """

    if all(l is None for l in [match_history, event_data, team]):
        raise(pyLCSExceptions.AllNoneError('All of match_history, event_data, and team_data are'
                                           'None. Make sure the data passed to parse_match_history'
                                           'Was generated by matchCrawler.download_json_data.'))

    game_info = dict()
    game_info['Players'] = match_history
    game_info['Team'] = team

    for p in game_info['Players']:
        game_info['Players'][p]['Minute'] = {}

    for k, v in event_data.items():
        game_info['Players'][k]['Minute'].update(v)

    return game_info


def _find_max_length(game_data: dict, minute: Union[int, str]) -> int:
    """_find_max_length

    Finds the max length of the game and returns it as an int

    :param game_data (dict): The individual game data returned by matchCrawler.download_json_data
    :param minute (Union[int, str]): The number of minutes to get data for
    :rtype int
    """

    max_length = int(game_data['MatchHistory']['gameDuration'] / 60)

    if isinstance(minute, str):
        if minute.isnumeric():
            minute = int(minute)
        elif minute.lower() == 'max':
            minute = max_length
        else:
            raise TypeError('Minute must be of type int or the string max')

    if minute > max_length:
        minute = max_length
        warn('Minute provided was greater than the game length. Minute was set to the max game length')
    elif minute < max_length:
        minute += 1

    return minute


def parse_MH(json_data: List[dict], minute: Union[int, str], unwanted_types: Union[set, list]) -> dict:
    """parse_MH

    Parse the match history datat that is returned by matchCrawler.download_json_data. The data is
    returned as a list of dicts in a easier to read format and for insertion into a mongoDB. The
    dict contiains headings Player, Team, Game. The player info is 1 json-like object per player,
    team is the same per team, and game is just the game info.

    :param json_data (List[dict]): The json-like dict from matchCrawler.download_json_data
    :param minute (Union[int, str]): The number of minutes you want timeline data for or max for all
    :param unwanted_types (Union[set, list]): Unwanted event types, can be None
    :rtype dict
    """

    if not isinstance(json_data, list):
        raise(TypeError(f'JSON_data must be of type list not {type(json_data)}'))

    ret_list = list()

    for i in json_data:
        minute = _find_max_length(i, minute)

        mh_data = _format_matchHistory_players(i)
        timeline_data = _format_timeLine_players(i, minute)
        event_data = _parse_event_data_players(i, timeline_data, minute, unwanted_types)
        team_data = _format_team_information(i)
        game_info = _game_information(i)

        merge = _merge_formats_together(mh_data, event_data, team_data)

        parse_dict = {'Player': {}, 'Team': {}, 'GameInfo': game_info}

        for k, v in merge['Players'].items():
            parse_dict['Player'][k] = v

        for k, v in merge['Team'].items():
            parse_dict['Team'][k] = v

        ret_list.append(parse_dict)

    return ret_list
