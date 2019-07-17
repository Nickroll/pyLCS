#!/usr/bin/env python

import json
from collections import defaultdict
from typing import Union

from .parseMatchHist import _flatten_json


def _parse_tl_player_data(json_data: dict=None) -> dict:
    """_parse_tl_player_data

    Parses the JSON data and pulls out the player data and returns it as a nested dict
    Example:
        {pid: {min: {stat: stat value}}}

    :param json_data (dict): The loaded JSON data from either a file or as a dict
    :rtype dict

    RIFT INFO:
        min: {x: -120, y: -120}
        max: {x: 14870, y: 14980}
        scale:
            min: { x: 0, y: 0}
            max: { x: 14820, y: 14881}


    """

    tl_dict = defaultdict(dict)

    for idx, time in enumerate(json_data[:16]):
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


def _parse_event_data(json_data: dict=None, player_data: dict=None) -> dict:
    """_parse_event_data

    Parses the event data from the timeline and adds it to the dict returned by _parse_tl_player_data

    :param json_data (dict): The json dict containing the timeline information
    :param player_data (dict): The dict returned by _parse_tl_player_data
    :rtype dict
    """

    unwanted_types = {'SKILL_LEVEL_UP', 'ITEM_DESTROYED', 'WARD_PLACED', 'WARD_KILL', 'ITEM_SOLD',
                      'ITEM_PURCHASED', 'ITEM_UNDO'}

    for idx, i in enumerate(json_data[:16]):
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
