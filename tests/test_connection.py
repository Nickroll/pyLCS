#!/usr/bin/env python
import context
import pytest
import responses
from pyLCS.exceptions import pyLCSExceptioins
from pyLCS.pyCrawler import pyCrawler


@responses.activate
def test_create_connection_returns():
    responses.add(responses.GET, 'http://test.com', status=200)
    resp = pyCrawler._create_connection('http://test.com')

    assert resp is not None


@responses.activate
def test_create_connection_bad_return():
    responses.add(responses.GET, 'http://testfail.com', status=404)
    resp = pyCrawler._create_connection('http://testfail.com')

    assert resp is None


def test_ext_link_creation_return_type_tuple():
    pyc = pyCrawler(region='na', year='2019', split='spring', playoffs=True)
    extension = pyc._ext_link_creation()

    assert isinstance(extension, tuple)


def test_ext_link_creation_return_type_str():
    pyc = pyCrawler(region='na', year='2019', split='spring', playoffs=False)
    extension = pyc._ext_link_creation()

    assert isinstance(extension, str)


def test_ext_link_creation_return_type_list():
    pyc = pyCrawler(region='lpl', year='2019', split='spring', playoffs=False)
    extension = pyc._ext_link_creation()

    assert isinstance(extension, list)


def test_ext_link_creation_string():
    return_links = []
    check_list = ['https://liquipedia.net/leagueoflegends/LCS/2019/Spring/Group_Stage',
                  'https://liquipedia.net/leagueoflegends/LCS/Academy_League/2019/Spring/Group_Stage',
                  'https://liquipedia.net/leagueoflegends/LCK/2019/Spring/Group_Stage',
                  'https://liquipedia.net/leagueoflegends/LMS/2019/Spring/Group_Stage']

    for i in ['na', 'lck', 'lms', 'eu', 'academy']:
        pyc = pyCrawler(region=i, year='2019', split='spring', playoffs=False)
        return_links.append(pyc._ext_link_creation())

    assert return_links.sort() == check_list.sort()


def test_ext_link_creation_raises_error():
    with pytest.raises(pyLCSExceptioins.RegionError):
        pyc = pyCrawler(region='fails', year='2019', split='spring', playoffs=False)
        pyc._ext_link_creation()


def test_ext_link_creation_lpl():
    check_list = ['https://liquipedia.net/leagueoflegends/LPL/2019/Spring/Group_Stage/Week_1-5',
                  'https://liquipedia.net/leagueoflegends/LPL/2019/Spring/Group_Stage/Week_6-10']

    pyc = pyCrawler(region='lpl', year='2019', split='spring', playoffs=False)
    return_links = pyc._ext_link_creation()

    assert check_list.sort() == return_links.sort()
