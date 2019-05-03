#!/usr/bin/env python

import context
import pytest
import responses
from pyLCS.matchCrawler import postMatchCrawl

MATCH_LINK_TEST = 'https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/992625?gameHash=76f99e0eb8658976'
MATCH_LINK_TEST_NO_RELM = 'https://matchhistory.euw.leagueoflegends.com/en/#match-details/TMNT02/992625?gameHash=76f99e0eb8658976'
MATCH_LINK_TEST_NO_Q = 'https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTMNT02/992625gameHash=76f99e0eb8658976'


@pytest.fixture
def make_postMatchCrawl_base():
    return postMatchCrawl(MATCH_LINK_TEST)


@pytest.fixture
def make_postMatchCrawl_base_fail_relm():
    return postMatchCrawl(MATCH_LINK_TEST_NO_RELM)


@pytest.fixture
def make_postMatchCrawl_base_fail_q():
    return postMatchCrawl(MATCH_LINK_TEST_NO_Q)


def test_post_match_handles_str(make_postMatchCrawl_base):
    assert isinstance(make_postMatchCrawl_base.match_links, list)


def test_post_match_handles_list(make_postMatchCrawl_base):
    make_postMatchCrawl_base.match_links = ['ab', 'bc']
    assert isinstance(make_postMatchCrawl_base.match_links, list)


def test_wrong_match_links_type():
    with pytest.raises(TypeError):
        postMatchCrawl(match_links=1)


TIME_JSON_LINK = 'https://acs.leagueoflegends.com/v1/stats/game/ESPORTSTMNT02/992625/timeline?gameHash=76f99e0eb8658976'
MATCH_JSON_LINK = 'https://acs.leagueoflegends.com/v1/stats/game/ESPORTSTMNT02/992625?gameHash=76f99e0eb8658976'


def test_create_json_warns(make_postMatchCrawl_base):
    with pytest.warns(UserWarning):
        make_postMatchCrawl_base.match_links = ['hasnorelativeparts']
        make_postMatchCrawl_base._create_json_links()


def test_create_json_no_relm_part(make_postMatchCrawl_base_fail_relm):
    with pytest.warns(UserWarning):
        make_postMatchCrawl_base_fail_relm._create_json_links()


def test_create_json_no_q_part(make_postMatchCrawl_base_fail_q):
    with pytest.warns(UserWarning):
        make_postMatchCrawl_base_fail_q._create_json_links()


def test_create_json_links(make_postMatchCrawl_base):
    resp = make_postMatchCrawl_base._create_json_links()

    assert resp[0] == [MATCH_JSON_LINK]
    assert resp[1] == [TIME_JSON_LINK]
    assert isinstance(resp, tuple)

# TODO: Write better tests for _create_json_links


@responses.activate
def test_json_resp(make_postMatchCrawl_base):
    responses.add(responses.GET, 'http://jsonlinks.com', status=200, json={'frames': 'frame1'})
    mh, tl = make_postMatchCrawl_base._create_json_links()
    resp = make_postMatchCrawl_base._json_retrival('http://jsonlinks.com')

    assert resp[0]['frames'] == 'frame1'


@responses.activate
def test_json_resp_type(make_postMatchCrawl_base):
    responses.add(responses.GET, 'http://jsonlinks.com', status=200, json={'frames': 'frame1'})
    mh, tl = make_postMatchCrawl_base._create_json_links()
    resp = make_postMatchCrawl_base._json_retrival('http://jsonlinks.com')

    assert isinstance(resp, list)


@responses.activate
def test_json_resp_has_none_on_fail(make_postMatchCrawl_base):
    responses.add(responses.GET, 'http://jsonlinksfail.com', status=404, json={'frames': 'frame1'})
    mh, tl = make_postMatchCrawl_base._create_json_links()
    resp = make_postMatchCrawl_base._json_retrival('http://jsonlinksfail.com')

    assert resp[0] is None


@responses.activate
def test_json_resp_handles_list(make_postMatchCrawl_base):
    responses.add(responses.GET, 'http://jsonlinks.com', status=200, json={'frames': 'frame1'})
    responses.add(responses.GET, 'http://jsonlinks2.com', status=200, json={'frames': 'frame2'})

    mh, tl = make_postMatchCrawl_base._create_json_links()
    resp = make_postMatchCrawl_base._json_retrival(['http://jsonlinks.com', 'http://jsonlinks2.com'])

    assert resp[0]['frames'] == 'frame1'
    assert resp[1]['frames'] == 'frame2'
