#!/usr/bin/env python
from typing import Union

from requests_html import HTMLResponse, HTMLSession

from .exceptions import pyLCSExceptioins


class pyCrawler(object):
    def __init__(self, region: str=None, year: Union[str, int]=None, split: str=None,
                 playoffs: bool=False):
        self.region = region
        self.year = str(year)
        self.split = split
        self.playoffs = playoffs

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

    def _ext_link_creation(self) -> Union[tuple, str, list]:
        """_post_match_game_links

        Uses liquidpedia to retrieve the links to the post match game links for the given region
        
        :rtype: Union[tuple, str]
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
            raise pyLCSExceptioins.RegionError(f'{self.region} is not one of LCS, LCK, LMS, '
                                               'LPL, LEC, or academy')

        if self.playoffs:
            p_ext = f'{ext[:-11]}Playoffs'

            return (ext, p_ext)
        else:
            return ext
