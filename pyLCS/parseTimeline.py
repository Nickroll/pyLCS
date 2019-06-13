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

# TODO: Link name and PID for a given game
