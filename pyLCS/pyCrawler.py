#!/usr/bin/env python
from typing import Union

from requests_html import HTMLResponse, HTMLSession


class pyLCS(object):
    def __init__(self, region: str=None):
        self.region = region

    @property
    def _create_connection(url: str, render: bool=False) -> Union[HTMLResponse, None]:
        """_create_connection

        Establishes a requests connection to the given page and returns the requests object

        :param url (str): The url to connect too.
        :param render (bool): If the JS should be rendered or not.
        :rtype: Union[HTMLResponse, None]
        """

        session = HTMLSession()
        r = session.get(url)

        if render:
            r.html.render()

        if r.ok:
            return r
        else:
            return None

    def _post_match_game_links(self, )
