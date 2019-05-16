#!/usr/bin/env python

import context
import pytest
import responses
from pyLCS.matchCrawler import (_create_json_links, _json_retrival,
                                download_json_data)

MATCH_LINK_TEST = 'https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/992625?gameHash=76f99e0eb8658976'
MATCH_LINK_TEST_NO_RELM = 'https://matchhistory.euw.leagueoflegends.com/en/#match-details/TMNT02/992625?gameHash=76f99e0eb8658976'
MATCH_LINK_TEST_NO_Q = 'https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTMNT02/992625gameHash=76f99e0eb8658976'

MH_JSON_LINK = 'https://acs.leagueoflegends.com/v1/stats/game/ESPORTSTMNT02/992625?gameHash=76f99e0eb8658976'
TL_JSON_LINK = 'https://acs.leagueoflegends.com/v1/stats/game/ESPORTSTMNT02/992625/timeline?gameHash=76f99e0eb8658976'


def test_create_json_links_pass():
    mh, tl = _create_json_links(MATCH_LINK_TEST)
    assert mh == MH_JSON_LINK
    assert tl == TL_JSON_LINK


def test_create_json_links_warn_relm():
    with pytest.warns(UserWarning):
        mh, tl = _create_json_links(MATCH_LINK_TEST_NO_RELM)
        assert mh is None
        assert tl is None


def test_create_json_link_warn_q():
    with pytest.warns(UserWarning):
        mh, tl = _create_json_links(MATCH_LINK_TEST_NO_Q)
        assert mh is None
        assert tl is None


@responses.activate
def test_json_retrival_returns_valid():
    responses.add(responses.GET, 'http://www.validjsonlink.com', status=200,
                  json={'playerstats': 10})
    resp = _json_retrival('http://www.validjsonlink.com')

    assert isinstance(resp, dict)
    assert resp['playerstats'] == 10


@responses.activate
def test_json_retrival_warns_invalid():
    responses.add(responses.GET, 'http://www.invalidjsonlink.com', status=404,
                  json={'playerstats': 10})

    with pytest.warns(UserWarning):
        resp = _json_retrival('http://www.invalidjsonlink.com')

    assert resp is None


@responses.activate
def test_download_json_data_valid():
    responses.add(responses.GET, MH_JSON_LINK, status=200, json={'pstats': 10, 'tstats': 100})
    responses.add(responses.GET, TL_JSON_LINK, status=200, json={'tlstats1': 10, 'tlstats2': 100})

    resp = download_json_data(MATCH_LINK_TEST)

    assert isinstance(resp, dict)
    assert resp['MatchHistory']['pstats'] == 10
    assert resp['MatchHistory']['tstats'] == 100
    assert resp['Timeline']['tlstats1'] == 10
    assert resp['Timeline']['tlstats2'] == 100
