#!/usr/bin/env python

from typing import Union

from requests_html import HTMLSession


class postMatchCrawl:
    """postMatchCrawl

    Crawls the post match links generated from liquidCrawler and gets the JSON data returned
    """

    def __init__(self, match_links: Union[list, str]=None):

        if isinstance(match_links, str):
            match_links = [match_links]

        self.match_links = match_links
