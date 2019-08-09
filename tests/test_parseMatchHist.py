#!/usr/bin/env python

import json

import context
import pytest
from pyLCS import parseMatchHist
from pyLCS.exceptions import pyLCSExceptions

with open('tests/testParseMatchHist_input.json', 'r') as jf:
    FULL_JSON_TEST = json.load(jf)


FAIL_JSON_TEST = {'MatchHistory': {'participantIdentities':
                                   [{'participantId': 1},
                                    {'participantId': 2}]}}


def test_format_matchHistory_players_returns_error():
    with pytest.raises(pyLCSExceptions.InvalidPlayerAmount):
        parseMatchHist._format_matchHistory_players(FAIL_JSON_TEST)


def test_format_matchHistory_players_returns_valid():
    ret_dict = parseMatchHist._format_matchHistory_players(FULL_JSON_TEST)

    assert ret_dict != {}


def test_format_matchHistory_players_returns_dict():
    ret_dict = parseMatchHist._format_matchHistory_players(FULL_JSON_TEST)

    assert isinstance(ret_dict, dict)


def test_format_matchHistory_players_adds_correct_role():
    ret_dict = parseMatchHist._format_matchHistory_players(FULL_JSON_TEST)

    assert ret_dict['TL Impact']['role'] == 'Top'
    assert ret_dict['C9 Licorice']['role'] == 'Top'
