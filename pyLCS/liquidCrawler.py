#!/usr/bin/env python

"""
Retrieves all the necessary game data from the liquidpedia game site. Finds the links to the match
history pages and returns them for use later.
"""

from typing import Union

from requests_html import HTMLResponse, HTMLSession

from .exceptions import pyLCSExceptions


class liquidCrawler(object):
    """liquidCrawler

    Basic class for creating and retriving the post match history links from liquidpedia
    """

    def __init__(self, region: str=None, year: Union[str, int]=None, split: str=None, playoffs: bool=False):
        self.region = region
        self.year = str(year)
        self.split = split
        self.playoffs = playoffs

    def _create_connection(self, url: str=None, render: bool=None) -> Union[HTMLResponse, None]:
        """_create_connection

        Establishes a requests connection to the given page and returns the requests object

        :param url (str): The url to connect too.
        :param render (bool): If the JS should be rendered or not.
        :rtype Union[HTMLResponse, None]
        """

        session = HTMLSession()
        r = session.get(url)

        if render:
            r.html.render()

        if r.ok:
            return r
        else:
            return None

    def _ext_link_creation(self) -> Union[tuple, str, list]:
        """_post_match_game_links

        Uses liquidpedia to retrieve the links to the post match game links for the given region

        :rtype Union[tuple, str]
        """

        base_link = 'https://liquipedia.net/leagueoflegends/'

        if self.region.lower() in ['na', 'lcs']:
            ext = f'{base_link}LCS/{self.year}/{self.split.capitalize()}/Group_Stage'
        elif self.region.lower() in ['lck', 'korea']:
            ext = f'{base_link}LCK/{self.year}/{self.split.capitalize()}/Group_Stage'
        elif self.region.lower() == 'lms':
            ext = f'{base_link}LMS/{self.year}/{self.split.capitalize()}/Group_Stage'
        elif self.region.lower() in ['lpl', 'china']:
            ext = []
            ext.append(f'{base_link}LPL/{self.year}/{self.split.capitalize()}/Group_Stage/Week_1-5')
            ext.append(f'{base_link}LPL/{self.year}/{self.split.capitalize()}/Group_Stage/Week_6-10')
        elif self.region.lower() in ['eu', 'europe', 'lec']:
            ext = f'{base_link}LEC/{self.year}/{self.split.capitalize()}/Group_Stage'
        elif self.region.lower() == 'academy':
            ext = f'{base_link}LCS/Academy_League/{self.year}/{self.split.capitalize()}/Group_Stage'
        else:
            raise pyLCSExceptions.RegionError(f'{self.region} is not one of LCS, LCK, LMS, '
                                              'LPL, LEC, or academy')

        if self.playoffs:
            p_ext = f'{ext[:-11]}Playoffs'

            return (ext, p_ext)
        else:
            return ext

    def _retrieve_post_match_site_links(self, ext_link: str=None, render: bool=None):
        """_retrieve_post_match_stats

        Uses the links created by _ext_link_creation to get the links to the post match games
        """

        r = self._create_connection(url=ext_link, render=render)
        links = r.html.xpath('//a[@title="Match History"]/@href')

        if len(links) == 0:
            raise(pyLCSExceptions.LinkLenError('Length of links retrieved was 0.'))

        return links

    def match_links(self, render: bool=True) -> list:
        """match_links

        Retrieves the links to the match history pages from the liquidpedia website.

        :param render (bool): If JavaScript should be rendered on the page
        :rtype list
        """

        exts = self._ext_link_creation()
        links = self._retrieve_post_match_site_links(ext_link=exts, render=render)

        return links
