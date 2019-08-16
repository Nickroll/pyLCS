#!/usr/bin/env python


import context
import pytest
import responses
from hypothesis import given, settings
from hypothesis import strategies as st
from pyLCS.matchCrawler import (_create_json_links, _json_retrival,
                                download_json_data)
from pyLCS.strategies import match_strats


@settings(max_examples=200)
@given(match_strats.valid_match_history_links())
def test_create_json_links(l):
    res = _create_json_links(l)

    assert res != (None, None)
    assert 'timeline?' in res[1]
    assert '?' in res[0]
    assert isinstance(res, tuple)


@settings(max_examples=200)
@given(match_strats.invalid_match_historoy_links_sports())
def test_create_json_links_warns_sports(l):
    with pytest.warns(UserWarning):
        res = _create_json_links(l)

    assert res == (None, None)


@settings(max_examples=200)
@given(match_strats.invalid_match_historoy_links_q())
def test_create_json_links_warns_q(l):
    with pytest.warns(UserWarning):
        res = _create_json_links(l)

    assert res == (None, None)


# ISSUE: for some reason takes forever, maybe responses issue?
@responses.activate
# @given(match_strats.valid_http_links())
# @settings(max_examples=20, deadline=None)
def test_json_retrival_returns_valid():
    responses.add(responses.GET, 'https://validjson.com', status=200, json={'playerstats': 10}, match_querystring=True)
    res = _json_retrival('https://validjson.com')

    assert isinstance(res, dict)
    assert res['playerstats'] == 10


# ISSUE: for some reason takes forever, maybe responses issue?
@responses.activate
# @given(match_strats.valid_http_links())
# @settings(max_examples=20, deadline=None)
def test_json_retrival_warns_invalid():
    responses.add(responses.GET, 'https://invalidjson.com', status=404, json={'playerstats': 19}, match_querystring=True)
    with pytest.warns(UserWarning):
        resp = _json_retrival('https://invalidjson.com')

    assert resp is None


MH_JSON_LINK = 'https://acs.leagueoflegends.com/v1/stats/game/ESPORTSTMNT02/992625?gameHash=76f99e0eb8658976'
TL_JSON_LINK = 'https://acs.leagueoflegends.com/v1/stats/game/ESPORTSTMNT02/992625/timeline?gameHash=76f99e0eb8658976'
MATCH_LINK_TEST = 'https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/992625?gameHash=76f99e0eb8658976'


@responses.activate
def test_download_works_with_list():
    responses.add(responses.GET, MH_JSON_LINK, status=200, json={'mhstats': 1})
    responses.add(responses.GET, TL_JSON_LINK, status=200, json={'tlstats': 1})
    resp = download_json_data([MATCH_LINK_TEST])

    assert isinstance(resp, list)
    assert resp[0] == {'MatchHistory': {'mhstats': 1},
                       'Timeline': {'tlstats': 1}}


@responses.activate
def test_download_works_without_list():
    responses.add(responses.GET, MH_JSON_LINK, status=200, json={'mhstats': 1})
    responses.add(responses.GET, TL_JSON_LINK, status=200, json={'tlstats': 1})
    resp = download_json_data(MATCH_LINK_TEST)

    assert isinstance(resp, list)
    assert resp[0] == {'MatchHistory': {'mhstats': 1},
                       'Timeline': {'tlstats': 1}}
