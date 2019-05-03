#!/usr/bin/env python

from typing import Union
from warnings import warn

from requests_html import HTMLSession


class postMatchCrawl:
    """postMatchCrawl

    Crawls the post match links generated from liquidCrawler and gets the JSON data returned
    """

    def __init__(self, match_links: Union[list, str]=None):

        if isinstance(match_links, str):
            match_links = [match_links]

        if not isinstance(match_links, list):
            raise TypeError('Match links is not of type list or string')

        self.match_links = match_links

    def _create_json_links(self) -> tuple:
        """_create_json_links

        Uses the match links to make the JSON links for the match history data

        Example: https://acs.leagueoflegends.com/v1/stats/game/ESPORTSTMNT02/992625?gameHash=76f99e0eb8658976
        https://acs.leagueoflegends.com/v1/stats/game/ESPORTSTMNT02/992625/timeline?gameHash=76f99e0eb86589
        :rtype tuple: (match_history, timelines)
        """

        acs_base = 'https://acs.leagueoflegends.com/v1/stats/game'
        timelines = list()
        match_history = list()

        for l in self.match_links:
            relm_part = l.find('ESPORTSTMNT')
            if relm_part != -1:
                q_loc = l.find('?')

                if q_loc != -1:
                    post_link = l[relm_part:q_loc]
                    hash_part = l[q_loc + 1:]

                    timelines.append(f'{acs_base}/{post_link}/timeline?{hash_part}')
                    match_history.append(f'{acs_base}/{post_link}?{hash_part}')

                else:
                    warn(f'{l} is not a valid post match link')
                    continue

            else:
                warn(f'{l} is not a valid post match link')
                continue

        return (match_history, timelines)

    def _json_retrival(self, link: Union[list, str]=None) -> list:
        """_json_retrival

        Retrieves the JSON form the link provided and returns the dicts in a list

        :param link (Union[list, str]): The link or a list of links to serach
        :rtype list
        """
        if isinstance(link, str):
            link = [link]

        session = HTMLSession()
        json_resp = list()

        for l in link:
            r = session.get(l)

            if r.ok:
                json_resp.append(r.json())
            else:
                json_resp.append(None)

        return json_resp
