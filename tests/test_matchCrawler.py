#!/usr/bin/env python

import context
import pytest
import responses
from pyLCS.matchCrawler import postMatchCrawl

MATCH_LINK_TEST = 'https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/992625?gameHash=76f99e0eb8658976'


@pytest.fixture
def make_postMatchCrawl_base():
    return postMatchCrawl(MATCH_LINK_TEST)


TIME_JSON_LINK = 'https://acs.leagueoflegends.com/v1/stats/game/ESPORTSTMNT02/992625/timeline?gameHash=76f99e0eb8658976'
MATCH_JSON_LINK = 'https://acs.leagueoflegends.com/v1/stats/game/ESPORTSTMNT02/992625?gameHash=76f99e0eb8658976'


def test_create_json_links(make_postMatchCrawl_base):
    resp = make_postMatchCrawl_base._create_json_links()

    assert resp[0] == [MATCH_JSON_LINK]
    assert resp[1] == [TIME_JSON_LINK]
    assert isinstance(resp, tuple)
