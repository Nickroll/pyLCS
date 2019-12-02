#!/usr/bin/env python

"""
Retrieves all the necessary game data from the liquidpedia game site. Finds the links to the match
history pages and returns them for use later.
"""

from typing import Union

from .connection import create_connection
from .exceptions import pyLCSExceptions


class matchHistory(object):
    """matchHistory

    Basic class for creating and retriving the post match history links from liquidpedia
    """

    def __init__(self, region: str=None, year: Union[str, int]=None, split: str=None, playoffs: bool=False):
        self.region = region

        if str(year).isnumeric():
            self.year = str(year)
        else:
            raise(TypeError('Year must be of an int or a numeric string'))

        self.split = split

        if isinstance(playoffs, bool):
            self.playoffs = playoffs
        else:
            raise(TypeError('Playoffs must be of type bool'))

    # TODO: Consider making this a self object instead of return
    def _ext_link_creation(self) -> Union[str, list]:
        """_post_match_game_links

        Uses liquidpedia to retrieve the links to the post match game links for the given region

        :rtype Union[str, list]
        """

        base_link = 'https://liquipedia.net/leagueoflegends/'

        # Add ermerging region support
        if self.region.lower() in ['na', 'lcs']:
            ext = [f'{base_link}LCS/{self.year}/{self.split.capitalize()}/Group_Stage']
        elif self.region.lower() in ['lck', 'korea']:
            ext = [f'{base_link}LCK/{self.year}/{self.split.capitalize()}/Group_Stage']
        elif self.region.lower() == 'lms':
            ext = [f'{base_link}LMS/{self.year}/{self.split.capitalize()}/Group_Stage']
        elif self.region.lower() in ['eu', 'europe', 'lec']:
            ext = [f'{base_link}LEC/{self.year}/{self.split.capitalize()}/Group_Stage']
        elif self.region.lower() == 'academy':
            ext = [f'{base_link}LCS/Academy_League/{self.year}/{self.split.capitalize()}/Group_Stage']
        elif self.region.lower() == 'lcl':
            ext = [f'{base_link}LCL/{self.year}/{self.split.capitalize()}/Group_Stage']
        elif self.region.lower() == 'ljl':
            ext = [f'{base_link}LJL/{self.year}/{self.split.capitalize()}/Group_Stage']
        elif self.region.lower() == 'lla':
            ext = [f'{base_link}LLA/{self.year}/{self.split.capitalize()}/Group_Stage']
        elif self.region.lower() == 'vcs':
            ext = [f'{base_link}VCS/{self.year}/{self.split.capitalize()}/Group_Stage']
        elif self.region.lower() == 'opl':
            ext = [f'{base_link}OPL/{self.year}/{self.split.capitalize()}/Group_Stage']
        elif self.region.lower() == 'tcl':
            ext = [f'{base_link}TCL/{self.year}/{self.split.capitalize()}/Group_Stage']
        elif self.region.lower() == 'all':
            ext = []
            spring_sum_regions = ['LCS', 'LCK', 'LEC', 'LJL', 'LCL', 'VCS', 'LMS']
            for r in spring_sum_regions:
                tmp_list = [f'{base_link}{r}/{self.year}/Spring/Group_Stage',
                            f'{base_link}{r}/{self.year}/Summer/Group_Stage']
                ext.extend(tmp_list)

            wint_sum_regions = ['TCL', 'CBLOL', 'BRCC']
            for r in wint_sum_regions:
                tmp_list = [f'{base_link}{r}/{self.year}/Winter/Group_Stage',
                            f'{base_link}{r}/{self.year}/Summer/Group_Stage']
                ext.extend(tmp_list)

            ext.extend([f'{base_link}LLA/{self.year}/Closing/Group_Stage', f'{base_link}LLA/{self.year}/Opening/Group_Stage',
                        f'{base_link}OPL/{self.year}/Split_1/Group_Stage', f'{base_link}OPL/{self.year}/Split_2/Group_Stage',
                        f'{base_link}LCS/Academy_League/{self.year}/Summer/Group_Stage', f'{base_link}LCS/Academy_League/{self.year}/Spring/Group_Stage'])

        else:
            raise pyLCSExceptions.RegionError(f'{self.region} is not one of LCS, LCK, LMS, '
                                              'LEC, LCL, LJL, LLA, VCS, OPL, academy, '
                                              'TCL, or all')

        if self.playoffs:
            p_ext = list()
            for e in ext:
                p_ext.append(f'{e[:-11]}Playoffs')

            ext.extend(p_ext)
            return ext

        else:
            return ext

    def _retrieve_post_match_site_links(self, ext_link: list, render: bool) -> list:
        """_retrieve_post_match_site_links

        Uses xpath to find the href links to the match history pages

        :param ext_link (str): The links returned by _ext_link_creation
        :param render (bool): If the page should be rendered for JS
        :rtype list
        """

        ret_links = []

        for el in ext_link:
            r = create_connection(link=el, render=render)

            if not r:
                continue

            if not r.text:
                continue

            links = r.html.xpath('//a[starts-with(@title, "Match History")]/@href')

            # Check for empty links and remove them
            for l in links:
                if l in ['', ' ']:
                    continue
                else:
                    ret_links.append(l)

            if len(ret_links) == 0:
                raise(pyLCSExceptions.LinkLenError('Length of links retrieved was 0. '
                                                   'Either extensions were not properly created or '
                                                   'All hrefs were empty (xpath may be broken)'))

        return ret_links

    def match_links(self, render: bool=True) -> list:
        """match_links

        Retrieves the links to the match history pages from the liquidpedia website.

        :param render (bool): If JavaScript should be rendered on the page
        :rtype list
        """

        exts = self._ext_link_creation()
        links = self._retrieve_post_match_site_links(ext_link=exts, render=render)

        return links
