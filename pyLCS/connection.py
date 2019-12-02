#!/usr/bin/env python


from typing import Union

from requests_html import HTMLResponse, HTMLSession


def create_connection(link: str=None, render: bool=False, json: bool=False) -> Union[None, HTMLResponse]:
    """create_connection

    Creates a connection to a site and can render the JS if needed.

    :param link (str): The website to fetch
    :param render (bool): To render JS or not
    :param json(bool): To return the JSON or not
    :rtype Union[None, HTMLResponse]
    """

    session = HTMLSession()

    r = session.get(link)

    if r.ok:
        if render:
            r.render()

        if json:
            return r.json()
        else:
            return r

    else:
        return None
