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
    with pytest.warns(UserWarning):
        resp = create_liquidCrawler_base._create_connection('https://invalidlink.com', render=False)

    assert resp is None


@given(liquid_strats.build_validLiquidCrawler())
def test_ext_creation_valid(lc):
    resp = lc._ext_link_creation()

    if lc.playoffs:
        assert len(resp) == 2
        assert 'Playoffs' in resp[1]
    else:
        assert len(resp) == 1
        assert lc.year in resp[0]
        assert lc.split.capitalize() in resp[0]


@given(liquid_strats.build_invalid_regions())
def test_ext_creation_invalid_region(create_liquidCrawler_base, r):
    create_liquidCrawler_base.region = r

    with pytest.raises(pyLCSExceptions.RegionError):
        create_liquidCrawler_base._ext_link_creation()


HTML_BODY = '<html><body><a href="https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/992625?gameHash=76f99e0eb8658976&amp;tab=overview" title="Match History" target="_blank" rel="nofollow noreferrer noopener"><img alt="Match History" src="/commons/images/c/ce/Match_Info_Stats.png" width="32" height="32"></a></body></html>'
HTML_RETURN = ['https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/992625?gameHash=76f99e0eb8658976&tab=overview',
               'https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/992641?gameHash=19f754ef4c0360d7',
               'https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/992659?gameHash=4c30fc1e819c44c5&tab=overview']
FAIL_BODY = '<html><body><a title="Match History"</a></body></html>'
FAIL_WITH_HREF = '<html><body><a href="" title="Match History"</a></body></html>'


@responses.activate
def test_retrieve_post_returns_list(create_liquidCrawler_base):
    responses.add(responses.GET, 'http://test.com', status=200, body=HTML_BODY)
    links = create_liquidCrawler_base._retrieve_post_match_site_links(['http://test.com'], False)

    assert isinstance(links, list)


@responses.activate
def test_retrieve_post_returns_correct(create_liquidCrawler_base):
    responses.add(responses.GET, 'http://test.com', status=200, body=HTML_BODY)
    links = create_liquidCrawler_base._retrieve_post_match_site_links(['http://test.com'], False)

    assert all(l in HTML_RETURN for l in links)


@responses.activate
def test_retrieve_post_returns_linkLenError(create_liquidCrawler_base):
    responses.add(responses.GET, 'http://test.com', status=200, body=FAIL_BODY)
    with pytest.raises(pyLCSExceptions.LinkLenError):
        create_liquidCrawler_base._retrieve_post_match_site_links(['http://test.com'], False)


@responses.activate
def test_retrieve_post_returns_linkLenError_href(create_liquidCrawler_base):
    responses.add(responses.GET, 'http://test.com', status=200, body=FAIL_WITH_HREF)
    with pytest.raises(pyLCSExceptions.LinkLenError):
        create_liquidCrawler_base._retrieve_post_match_site_links(['http://test.com'], False)


# BAD_EXT_YEAR_LINK = 'https://liquipedia.net/leagueoflegends/LCS/100/Spring/Group_Stage'
# BAD_EXT_SPLIT_LINK = 'https://liquipedia.net/leagueoflegends/LCS/2019/Thisfailsduh/Group_Stage'
#
#
# @responses.activate
# def test_match_links_bad_year(create_liquidCrawler_base):
#     responses.add(responses.GET, BAD_EXT_YEAR_LINK, status=200,)
#     create_liquidCrawler_base.year = '100'
#
#     with pytest.raises(pyLCSExceptions.PageEmptyError):
#         create_liquidCrawler_base.match_links(render=False)
#
#
# @responses.activate
# def test_match_links_bad_split(create_liquidCrawler_base):
#     responses.add(responses.GET, BAD_EXT_SPLIT_LINK, status=200,)
#     create_liquidCrawler_base.split = 'Thisfailsduh'
#
#     with pytest.raises(pyLCSExceptions.PageEmptyError):
#         create_liquidCrawler_base.match_links(render=False)
#

@responses.activate
def test_match_links_bad_region(create_liquidCrawler_base):
    create_liquidCrawler_base.region = 'notaregion'

    with pytest.raises(pyLCSExceptions.RegionError):
        create_liquidCrawler_base.match_links(render=False)


TO_MOCK = 'https://liquipedia.net/leagueoflegends/LCS/2019/Spring/Group_Stage'
@responses.activate
def test_match_links_returns_list(create_liquidCrawler_base):
    responses.add(responses.GET, TO_MOCK, status=202, body=HTML_BODY)
    links = create_liquidCrawler_base.match_links(render=False)

    assert all(l in HTML_RETURN for l in links)
