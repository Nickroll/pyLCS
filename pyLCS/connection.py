#!/usr/bin/env python

import os
from typing import Union

from backoff import expo, on_exception
from ratelimit import RateLimitException, limits
from requests_html import HTMLResponse, HTMLSession


@on_exception(expo, RateLimitException, max_tries=8)
@limits(calls=15, period=900)
def create_connection(link: str=None, render: bool=False, json: bool=False) -> Union[None, HTMLResponse]:
    """create_connection

    Creates a connection to a site and can render the JS if needed.

    :param link (str): The website to fetch
    :param render (bool): To render JS or not
    :param json(bool): To return the JSON or not
    :rtype Union[None, HTMLResponse]
    """

    ID_TOKEN = os.environ['ID_TOKEN']

    session = HTMLSession()

    cookies = {'id_token': ID_TOKEN}
    r = session.get(link, cookies=cookies)

    if r.ok:
        print(f'Links: {link}\nStatus: {r.status_code}\n---------------------')

        if render:
            r.html.render()

        if json:
            return r.json()

        else:
            return r

    else:
        print(f'Links: {link}\nStatus: {r.status_code}\n{r.headers}\nID Token: {ID_TOKEN}\n'
              'If status is 429 than the ID token needs to be regenerated from the login page.\n'
              '-------------------------')
        return None
