#!/usr/bin/env python

import json

import context
import pytest
from pyLCS import parseMatchHist
from pyLCS.exceptions import pyLCSExceptions


@pytest.fixture
def global_json():
    with open('tests/testParseMatchHist_input.json', 'r') as jf:
        FULL_JSON_TEST = json.load(jf)

    return FULL_JSON_TEST

FAIL_JSON_TEST = {'MatchHistory': {'participantIdentities':
                                   [{'participantId': 1},
                                    {'participantId': 2}]}}


def test_format_matchHistory_players_returns_error():
    with pytest.raises(pyLCSExceptions.InvalidPlayerAmount):
        parseMatchHist._format_matchHistory_players(FAIL_JSON_TEST)


def test_format_matchHistory_players_returns_valid(global_json):
    ret_dict = parseMatchHist._format_matchHistory_players(global_json)

    assert ret_dict != {}


def test_format_matchHistory_players_returns_dict(global_json):
    ret_dict = parseMatchHist._format_matchHistory_players(global_json)

    assert isinstance(ret_dict, dict)


def test_format_matchHistory_players_adds_correct_role(global_json):
    ret_dict = parseMatchHist._format_matchHistory_players(global_json)

    assert ret_dict['TL Impact']['role'] == 'Top'
    assert ret_dict['C9 Licorice']['role'] == 'Top'


MIN_TEST = {'MatchHistory': {'participantIdentities':
                                    [{'participantId': 0, 'player': {'summonerName': 'TL 0'}},
                                     {'participantId': 1, 'player': {'summonerName': 'TL 1'}},
                                     {'participantId': 2, 'player': {'summonerName': 'TL 2'}},
                                     {'participantId': 3, 'player': {'summonerName': 'TL 3'}},
                                     {'participantId': 4, 'player': {'summonerName': 'TL 4'}},
                                     {'participantId': 5, 'player': {'summonerName': 'TL 5'}},
                                     {'participantId': 6, 'player': {'summonerName': 'TL 6'}},
                                     {'participantId': 7, 'player': {'summonerName': 'TL 7'}},
                                     {'participantId': 8, 'player': {'summonerName': 'TL 8'}},
                                     {'participantId': 9, 'player': {'summonerName': 'TL 9'}}
                                    ],
                             'participants':
                                    [{'stats': {'win': True, 'level': 10},
                                      'timeline': {'xpPerMinDeltas': {'0-10': 0}}},
                                     {'stats': {'win': True, 'level': 11},
                                      'timeline': {'xpPerMinDeltas': {'0-10': 1}}},
                                     {'stats': {'win': True, 'level': 12},
                                      'timeline': {'xpPerMinDeltas': {'0-10': 2}}},
                                     {'stats': {'win': True, 'level': 13},
                                      'timeline': {'xpPerMinDeltas': {'0-10': 3}}},
                                     {'stats': {'win': True, 'level': 14},
                                      'timeline': {'xpPerMinDeltas': {'0-10': 4}}},
                                     {'stats': {'win': True, 'level': 15},
                                      'timeline': {'xpPerMinDeltas': {'0-10': 5}}},
                                     {'stats': {'win': True, 'level': 16},
                                      'timeline': {'xpPerMinDeltas': {'0-10': 6}}},
                                     {'stats': {'win': True, 'level': 17},
                                      'timeline': {'xpPerMinDeltas': {'0-10': 7}}},
                                     {'stats': {'win': True, 'level': 18},
                                      'timeline': {'xpPerMinDeltas': {'0-10': 8}},
                                      'teamId': 'TL'},
                                     {'stats': {'win': True, 'level': 19},
                                      'timeline': {'xpPerMinDeltas': {'0-10': 9}}}
                                    ]}}


def test_format_matchHistory_players_ret_dict_player_names():
    ret_dict = parseMatchHist._format_matchHistory_players(MIN_TEST)

    assert ret_dict['TL 0']['win'] is True
    assert ret_dict['TL 1']['level'] == 11
    assert ret_dict['TL 2']['xpPerMinDeltas_0-10'] == 2
    assert ret_dict['TL 8']['teamId'] == 'TL'


def test_format_timeLine_players_returns_dict(global_json):
    ret_dict = parseMatchHist._format_timeLine_players(global_json, 15)

    assert isinstance(ret_dict, dict)


def test_format_timeLine_players_returns_correct(global_json):
    ret_dict = parseMatchHist._format_timeLine_players(global_json, 15)

    assert ret_dict['C9 Licorice'][3]['currentGold'] == 423


def test_format_timeLine_players_returns_names(global_json):
    ret_dict = parseMatchHist._format_timeLine_players(global_json, 15)

    keys = list(ret_dict.keys())
    assert keys == ['TL Impact', 'TL Xmithie', 'TL Jensen', 'TL Doublelift', 'TL CoreJJ', 'C9 Licorice', 'C9 Svenskeren', 'C9 Nisqy', 'C9 Sneaky', 'C9 Zeyzal']
