#!/usr/bin/env python

"""

"""
import context
import pytest
import responses
from pyLCS.exceptions import pyLCSExceptions
from pyLCS.liquidCrawler import liquidCrawler


@pytest.fixture
def make_liquidCrawler_base():
    return liquidCrawler(region='na', year='2019', split='spring', playoffs=False)


@responses.activate
def test_create_connection_returns(make_liquidCrawler_base):
    responses.add(responses.GET, 'http://test.com', status=200)
    resp = make_liquidCrawler_base._create_connection(url='http://test.com', render=False)

    assert resp is not None


@responses.activate
def test_create_connection_bad_return(make_liquidCrawler_base):
    responses.add(responses.GET, 'http://testfail.com', status=404)
    resp = make_liquidCrawler_base._create_connection(url='http://testfail.com', render=False)

    assert resp is None


def test_ext_link_creation_returns_str(make_liquidCrawler_base):
    ext = make_liquidCrawler_base._ext_link_creation()

    assert isinstance(ext, str)


def test_ext_link_creation_returns_list(make_liquidCrawler_base):
    make_liquidCrawler_base.region = 'lpl'
    ext = make_liquidCrawler_base._ext_link_creation()

    assert isinstance(ext, list)


def test_ext_link_creation_returns_tuple(make_liquidCrawler_base):
    make_liquidCrawler_base.playoffs = True
    ext = make_liquidCrawler_base._ext_link_creation()

    assert isinstance(ext, tuple)


def test_ext_link_creation_strings_correct(make_liquidCrawler_base):
    ret_links = []
    check_list = ['https://liquipedia.net/leagueoflegends/LCS/2019/Spring/Group_Stage',
                  'https://liquipedia.net/leagueoflegends/LCS/Academy_League/2019/Spring/Group_Stage',
                  'https://liquipedia.net/leagueoflegends/LCK/2019/Spring/Group_Stage',
                  'https://liquipedia.net/leagueoflegends/LMS/2019/Spring/Group_Stage']

    for i in ['na', 'lck', 'lms', 'eu', 'academy']:
        make_liquidCrawler_base.region = i
        ret_links.append(make_liquidCrawler_base._ext_link_creation())

    assert ret_links.sort() == check_list.sort()


def test_ext_link_creation_for_lpl(make_liquidCrawler_base):
    check_list = ['https://liquipedia.net/leagueoflegends/LPL/2019/Spring/Group_Stage/Week_1-5',
                  'https://liquipedia.net/leagueoflegends/LPL/2019/Spring/Group_Stage/Week_6-10']
    make_liquidCrawler_base.region = 'lpl'
    ret_links = make_liquidCrawler_base._ext_link_creation()

    assert check_list.sort() == ret_links.sort()


def test_ext_link_creation_raises_region_error(make_liquidCrawler_base):
    with pytest.raises(pyLCSExceptions.RegionError):
        make_liquidCrawler_base.region = 'fails'
        make_liquidCrawler_base._ext_link_creation()


def test_ext_link_creation_playoffs(make_liquidCrawler_base):
    check_list = ['https://liquipedia.net/leagueoflegends/LCS/2019/Spring/Playoffs']

    make_liquidCrawler_base.playoffs = True
    ext, p_ext = make_liquidCrawler_base._ext_link_creation()

    assert check_list[0] == p_ext


HTML_BODY = '<html><body><a href="https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/992625?gameHash=76f99e0eb8658976&amp;tab=overview" title="Match History" target="_blank" rel="nofollow noreferrer noopener"><img alt="Match History" src="/commons/images/c/ce/Match_Info_Stats.png" width="32" height="32"></a></body></html>'
HTML_RETURN = ['https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/992625?gameHash=76f99e0eb8658976&tab=overview',
               'https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/992641?gameHash=19f754ef4c0360d7',
               'https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/992659?gameHash=4c30fc1e819c44c5&tab=overview']
FAIL_BODY = '<html><body><a title="Match History"</a></body></html>'
FAIL_WITH_HREF = '<html><body><a href="" title="Match History"</a></body></html>'


@responses.activate
def test_retrieve_post_returns_list(make_liquidCrawler_base):
    responses.add(responses.GET, 'http://test.com', status=200, body=HTML_BODY)
    links = make_liquidCrawler_base._retrieve_post_match_site_links('http://test.com', False)

    assert isinstance(links, list)


@responses.activate
def test_retrieve_post_returns_correct(make_liquidCrawler_base):
    responses.add(responses.GET, 'http://test.com', status=200, body=HTML_BODY)
    links = make_liquidCrawler_base._retrieve_post_match_site_links('http://test.com', False)

    assert all(l in HTML_RETURN for l in links)


@responses.activate
def test_retrieve_post_returns_linkLenError(make_liquidCrawler_base):
    responses.add(responses.GET, 'http://test.com', status=200, body=FAIL_BODY)
    with pytest.raises(pyLCSExceptions.LinkLenError):
        make_liquidCrawler_base._retrieve_post_match_site_links('http://test.com', False)


@responses.activate
def test_retrieve_post_returns_linkLenError_href(make_liquidCrawler_base):
    responses.add(responses.GET, 'http://test.com', status=200, body=FAIL_WITH_HREF)
    with pytest.raises(pyLCSExceptions.LinkLenError):
        make_liquidCrawler_base._retrieve_post_match_site_links('http://test.com', False)


BAD_EXT_YEAR_LINK = 'https://liquipedia.net/leagueoflegends/LCS/100/Spring/Group_Stage'
BAD_EXT_SPLIT_LINK = 'https://liquipedia.net/leagueoflegends/LCS/2019/Thisfailsduh/Group_Stage'


@responses.activate
def test_match_links_bad_year(make_liquidCrawler_base):
    responses.add(responses.GET, BAD_EXT_YEAR_LINK, status=200,)
    make_liquidCrawler_base.year = '100'

    with pytest.raises(pyLCSExceptions.PageEmptyError):
        make_liquidCrawler_base.match_links(render=False)


@responses.activate
def test_match_links_bad_split(make_liquidCrawler_base):
    responses.add(responses.GET, BAD_EXT_SPLIT_LINK, status=200,)
    make_liquidCrawler_base.split = 'Thisfailsduh'

    with pytest.raises(pyLCSExceptions.PageEmptyError):
        make_liquidCrawler_base.match_links(render=False)


@responses.activate
def test_match_links_bad_region(make_liquidCrawler_base):
    make_liquidCrawler_base.region = 'notaregion'

    with pytest.raises(pyLCSExceptions.RegionError):
        make_liquidCrawler_base.match_links(render=False)


TO_MOCK = 'https://liquipedia.net/leagueoflegends/LCS/2019/Spring/Group_Stage'
@responses.activate
def test_match_links_returns_list(make_liquidCrawler_base):
    responses.add(responses.GET, TO_MOCK, status=202, body=HTML_BODY)
    links = make_liquidCrawler_base.match_links(render=False)

    assert all(l in HTML_RETURN for l in links)
