#!/usr/bin/env python

import os
from typing import Union

from requests_html import HTMLResponse, HTMLSession

ID_TOKEN = os.environ['ID_TOKEN']


def create_connection(link: str=None, render: bool=False, json: bool=False) -> Union[None, HTMLResponse]:
    """create_connection

    Creates a connection to a site and can render the JS if needed.

    :param link (str): The website to fetch
    :param render (bool): To render JS or not
    :param json(bool): To return the JSON or not
    :rtype Union[None, HTMLResponse]
    """

    session = HTMLSession()

    cookies = {'id_token': ID_TOKEN}
    r = session.get(link, cookies=cookies)

    if r.ok:
        print(f'links: {link}')
        print(f'Status: {r.status_code}')
        print(r.headers)
        print('---------------------- \n')

        if render:
            r.html.render()

        if json:
            return r.json()

        else:
            return r

    else:
        print(f'links: {link}')
        print(f'Status: {r.status_code}')
        print(r.headers)
        print(r.cookies)
        print(r.text)
        print('If status is 429 than the ID token needs to be regenerated from the login page.')
        print('---------------------- \n')

        return None
