#!/usr/bin/env python

import requests_html


def _create_connection(url: str, render: bool=False):
    """_create_connection

    Establishes a requests connection to the given page and returns the requests object

    :param url (str): The url to connect too.
    :param render (bool): If the JS should be rendered or not.
    """

