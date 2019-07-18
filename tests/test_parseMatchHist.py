#!/usr/bin/env python

import context
import pytest
import responses
import json
from pyLCS.parseMatchHist import _column_names_match_hist, _flatten_json

JSON_FILE = 'test.json'

with open(JSON_FILE, 'r') as jf:
    JSON_DATA = json.load(jf)

FLAT_JSON = _flatten_json(JSON_DATA)


def test_column_names_match_hist_returns_list():
    col_names = _column_names_match_hist(FLAT_JSON)
    assert isinstance(col_names, list)


def test_column_names_match_hist_flat_vs_reg():
    flat_cols = _column_names_match_hist(FLAT_JSON)
    col_names = _column_names_match_hist(JSON_DATA)
    assert col_names != flat_cols


def test_column_names_match_hist_reg_no_splits():
    col_names = _column_names_match_hist(JSON_DATA)
    assert len(col_names) == 3


def test_column_names_match_hist_only_has_specific_cols():
    col_names = _column_names_match_hist(JSON_DATA)
    assert col_names == ['gameId', 'participantId', 'PlayerName']


@pytest.mark.xfail
def test_column_names_match_hist_lacks_subset():
    col_list = ['longestTimeSpentLiving', 'statPerk2', 'lane', 'teamId', 'gameId', 'championId']
    col_names = _column_names_match_hist(JSON_DATA)
    assert set(col_list).issubset(col_names)


def test_column_names_match_hist_flat_with_splits():
    col_names = _column_names_match_hist(FLAT_JSON)
    assert len(col_names) > 3


def test_column_names_match_hist_flat_has_specific_cols():
    col_list = ['longestTimeSpentLiving', 'statPerk2', 'lane', 'teamId', 'gameId', 'championId']
    col_names = _column_names_match_hist(FLAT_JSON)
    assert set(col_list).issubset(set(col_names))


