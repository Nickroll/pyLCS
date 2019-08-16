#!/usr/bin/env python


import context
import pytest
import responses
from hypothesis import given
from pyLCS.liquidCrawler import liquidCrawler
from pyLCS.strategies import liquid_strats


@given(liquid_strats.build_liquidCrawler())
def test_liquidCrawler_builds(b):
    pass


@given(liquid_strats.man_build_liquidCrawler())
def test_man_liquidCrawler_builds(t):
    lc = liquidCrawler(t[0], t[1], t[2], t[3])

    assert isinstance(lc.year, str)


@pytest.fixture
def create_liquidCrawler_base():
    lc = liquidCrawler('na', 2019, 'spring', False)

    return lc


@responses.activate
def test_create_connection_valid(create_liquidCrawler_base):
    responses.add(responses.GET, 'https://validlink.com', status=200)
    resp = create_liquidCrawler_base._create_connection('https://validlink.com', render=False)

    assert resp is not None


@responses.activate
def test_create_connection_invalid(create_liquidCrawler_base):
    responses.add(responses.GET, 'https://invalidlink.com', status=404)
    resp = create_liquidCrawler_base._create_connection('https://invalidlink.com', render=False)

    assert resp is None
