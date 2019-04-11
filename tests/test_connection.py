#!/usr/bin/env python
import context
import responses
from pyLCS import pyCrawler


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
