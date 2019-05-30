#!/usr/bin/env python

import json
from typing import Union

from .parseMatchHist import _flatten_json


def _parse_tl_player_data(json_data: dict=None) -> dict:
    """_parse_tl_player_data

    Parses the JSON data and pulls out the player data and returns it as a dict
    Example:

    :param json_data (dict): The loaded JSON data from either a file or as a dict
    :rtype dict
    """

    flat_data = _flatten_json(json_data)
