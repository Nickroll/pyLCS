#!/usr/bin/env python


import context
import pytest
import responses
from hypothesis import given
from pyLCS.exceptions import pyLCSExceptions
from pyLCS.liquidCrawler import liquidCrawler
from pyLCS.strategies import liquid_strats


@pytest.fixture
def create_liquidCrawler_base():
    lc = liquidCrawler('na', 2019, 'spring', False)

    return lc


@given(liquid_strats.build_liquidCrawler())
def test_liquidCrawler_builds(b):
    pass


@given(liquid_strats.man_build_liquidCrawler())
def test_man_liquidCrawler_builds(t):
    lc = liquidCrawler(t[0], t[1], t[2], t[3])

    assert isinstance(lc.year, str)


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


@given(liquid_strats.build_validLiquidCrawler())
def test_ext_creation_valid(lc):
    resp = lc._ext_link_creation()

    if lc.playoffs:
        assert isinstance(resp, list)
        assert 'Playoffs' in resp[1]
    else:
        assert isinstance(resp, str)
        assert lc.year in resp
        assert lc.split.capitalize() in resp


@given(liquid_strats.build_invalid_regions())
def test_ext_creation_invalid_region(create_liquidCrawler_base, r):
    create_liquidCrawler_base.region = r

    with pytest.raises(pyLCSExceptions.RegionError):
        create_liquidCrawler_base._ext_link_creation()
