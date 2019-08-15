#!/usr/bin/env python


import context
import pytest
import responses
from hypothesis import given
from hypothesis import strategies as st
from pyLCS.matchCrawler import (_create_json_links, _json_retrival,
                                download_json_data)
from strategies import match_strats


@given(match_strats.valid_match_history_links())
def test_create_json_links(l):
    res = _create_json_links(l)

    assert res is not None


@given(match_strats.invalid_match_historoy_links_sports())
def test_create_json_links_warns_sports(l):
    with pytest.warns(UserWarning):
        _create_json_links(l)


@given(match_strats.invalid_match_historoy_links_q())
def test_create_json_links_warns_q(l):
    with pytest.warns(UserWarning):
        _create_json_links(l)
