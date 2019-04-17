#!/usr/bin/env python
import context
import pytest
import responses
from pyLCS.exceptions import pyLCSExceptions
from pyLCS.pyCrawler import pyCrawler


@pytest.fixture
def make_pyCrawler_base():
    return pyCrawler(region='na', year='2019', split='spring', playoffs=False)


@responses.activate
def test_create_connection_returns(make_pyCrawler_base):
    responses.add(responses.GET, 'http://test.com', status=200)
    resp = make_pyCrawler_base._create_connection(url='http://test.com')

    assert resp is not None


@responses.activate
def test_create_connection_bad_return(make_pyCrawler_base):
    responses.add(responses.GET, 'http://testfail.com', status=404)
    resp = make_pyCrawler_base._create_connection(url='http://testfail.com')

    assert resp is None


def test_ext_link_creation_return_type_tuple(make_pyCrawler_base):
    make_pyCrawler_base.playoffs = True
    extension = make_pyCrawler_base._ext_link_creation()

    assert isinstance(extension, tuple)


def test_ext_link_creation_return_type_str(make_pyCrawler_base):
    extension = make_pyCrawler_base._ext_link_creation()

    assert isinstance(extension, str)


def test_ext_link_creation_return_type_list(make_pyCrawler_base):
    make_pyCrawler_base.region = 'lpl'
    extension = make_pyCrawler_base._ext_link_creation()

    assert isinstance(extension, list)


def test_ext_link_creation_string(make_pyCrawler_base):
    return_links = []
    check_list = ['https://liquipedia.net/leagueoflegends/LCS/2019/Spring/Group_Stage',
                  'https://liquipedia.net/leagueoflegends/LCS/Academy_League/2019/Spring/Group_Stage',
                  'https://liquipedia.net/leagueoflegends/LCK/2019/Spring/Group_Stage',
                  'https://liquipedia.net/leagueoflegends/LMS/2019/Spring/Group_Stage']

    for i in ['na', 'lck', 'lms', 'eu', 'academy']:
        make_pyCrawler_base.region = i
        return_links.append(make_pyCrawler_base._ext_link_creation())

    assert return_links.sort() == check_list.sort()


def test_ext_link_creation_raises_error(make_pyCrawler_base):
    with pytest.raises(pyLCSExceptions.RegionError):
        make_pyCrawler_base.region = 'fails'
        make_pyCrawler_base._ext_link_creation()


def test_ext_link_creation_lpl(make_pyCrawler_base):
    check_list = ['https://liquipedia.net/leagueoflegends/LPL/2019/Spring/Group_Stage/Week_1-5',
                  'https://liquipedia.net/leagueoflegends/LPL/2019/Spring/Group_Stage/Week_6-10']

    make_pyCrawler_base.region = 'lpl'
    return_links = make_pyCrawler_base._ext_link_creation()

    assert check_list.sort() == return_links.sort()


def test_ext_link_creation_playoffs(make_pyCrawler_base):
    check_list = ['https://liquipedia.net/leagueoflegends/LCS/2019/Spring/Playoffs']

    make_pyCrawler_base.playoffs = True
    ext, p_ext = make_pyCrawler_base._ext_link_creation()

    assert check_list[0] == p_ext


HTML_BODY = '<html><body><a href="https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/992625?gameHash=76f99e0eb8658976&amp;tab=overview" title="Match History" target="_blank" rel="nofollow noreferrer noopener"><img alt="Match History" src="/commons/images/c/ce/Match_Info_Stats.png" width="32" height="32"></a></body></html>'
HTML_RETURN = ['https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/992625?gameHash=76f99e0eb8658976&tab=overview',
               'https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/992641?gameHash=19f754ef4c0360d7',
               'https://matchhistory.euw.leagueoflegends.com/en/#match-details/ESPORTSTMNT02/992659?gameHash=4c30fc1e819c44c5&tab=overview']


@responses.activate
def test_retrieve_post_returns_list(make_pyCrawler_base):
    responses.add(responses.GET, 'http://test.com', status=200, body=HTML_BODY)
    links = make_pyCrawler_base._retrieve_post_match_site_links('http://test.com', False)

    assert isinstance(links, list)


@responses.activate
def test_retrieve_post_returns_correct(make_pyCrawler_base):
    responses.add(responses.GET, 'http://test.com', status=200, body=HTML_BODY)
    links = make_pyCrawler_base._retrieve_post_match_site_links('http://test.com', False)

    assert links[0] == HTML_RETURN[0]
