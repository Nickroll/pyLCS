#!/usr/bin/env python

from collections import defaultdict

from .parseMatchHist import _flatten_json


def _parse_tl_player_data(json_data: dict=None, minute: int=15) -> dict:
    """_parse_tl_player_data

    Parses the JSON data and pulls out the player data and returns it as a nested dict up to the minute specified

    :param json_data (dict): The loaded JSON data from either a file or as a dict
    :param minute (int): The last minute in time you want to gather stats for
    :rtype dict

    RIFT INFO:
        min: {x: -120, y: -120}
        max: {x: 14870, y: 14980}
        scale:
            min: { x: 0, y: 0}
            max: { x: 14820, y: 14881}


    """

    tl_dict = defaultdict(dict)

    for idx, time in enumerate(json_data[:minute + 1]):
        for i in time['participantFrames']:
            tl_dict[time['participantFrames'][i]['participantId'] - 1][idx] = time['participantFrames'][i]

            # Fix for participant ID as it differes in match history and timeline info
            tl_dict[time['participantFrames'][i]['participantId'] - 1][idx]['participantId'] -= 1

    for k, v in tl_dict.items():
        for key, val in v.items():
            tl_dict[k][key] = _flatten_json(val)

    return dict(tl_dict)


def _fix_pid_with_names(time_line_dict: dict=None, match_history_stats: dict=None) -> dict:
    """_fix_pid_with_names

    Uses the stats returned by parseMatchHist.get_stats() to replace the pid key with the players name

    :param time_line_dict (dict): The dict returned from _parse_tl_player_data
    :param match_history_stats (dict): The dict returned from parseMatchHist.get_stats
    :rtype dict
    """

    fixed_dict = dict()

    v = list(match_history_stats.values())
    for i, l in enumerate(v[0]):
        fixed_dict[l[0]] = time_line_dict[i]

    return fixed_dict


def _parse_event_data(json_data: dict=None, player_data: dict=None, minute: int=15) -> dict:
    """_parse_event_data

    Parses the event data from the timeline and adds it to the dict returned by _parse_tl_player_data

    :param json_data (dict): The json dict containing the timeline information
    :param player_data (dict): The dict returned by _parse_tl_player_data
    :param minute (int): The maximum time you want to gather stats for in minutes
    :rtype dict
    """

    unwanted_types = {'SKILL_LEVEL_UP', 'ITEM_DESTROYED', 'WARD_PLACED', 'WARD_KILL', 'ITEM_SOLD',
                      'ITEM_PURCHASED', 'ITEM_UNDO'}

    for idx, i in enumerate(json_data[:minute + 1]):
        for e in i['events']:
            if e['type'] not in unwanted_types:
                pid = int(e['killerId']) - 1

                # Fixing the issue where pid's don't match
                to_insert = e
                for k, v in to_insert.items():
                    if 'Id' in k:
                        if isinstance(v, int):
                            to_insert[k] -= 1
                        elif isinstance(v, list):
                            updated_ids = [pids - 1 for pids in v]
                            to_insert[k] = updated_ids

                player_data[pid][idx] = [player_data[pid][idx], to_insert]
            else:
                continue

    return player_data


def timeline_stats(timeline_data: str=None, match_history_stats: dict=None, minute: int=15) -> dict:
    """timeline_stats

    Parses the timeline stats returned by matchCrawler.download_json_data() and returns a json like
    object that contains data timeline data up to the minute specified

    :param timeline_data (str): The second data object returned by matchCrawler.download_json_data()
    :param match_history_stats (dict): The data returned by parseMatchHist.get_stats()
    :param minute (int): The maximum minute for which you want timeline data returned
    :rtype dict
    """

    if not isinstance(minute, int):
        minute = int(minute)

    parse_data = _parse_tl_player_data(timeline_data, minute)
    event_data = _parse_event_data(timeline_data, parse_data, minute)
    fixed = _fix_pid_with_names(event_data, match_history_stats)

    return fixed
