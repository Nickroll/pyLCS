#!/usr/bin/env python

"""
Retrieves all the necessary game data from the liquidpedia game site. Finds the links to the match
history pages and returns them for use later.
"""

import configparser
from .connection import create_connection
from .exceptions import pyLCSExceptions


# TODO: Make this read from a config file of some sort
def _ext_link_creation(config_path: str) -> list:
    """_post_match_game_links

    Creates the links to liquipedia pages

    :param config_path (str): The path to the config.ini file
    :rtype Union[list]
    """

    link_list = list()

    config = configparser.ConfigParser()
    config.read(config_path)
    parse_dict = {sec: dict(config.items(sec)) for sec in config.sections()}

    base = parse_dict['Links']['base']
    group = parse_dict['Links']['group']
    year = parse_dict['Links']['year']
    if parse_dict['Links']['playoffs'].lower() == 'true':
        playoffs = True

    for k, v in parse_dict['Regions'].items():
        if v.lower() == 'true':
            reg = k.upper()
            sp = parse_dict['Splits'][k].split(' ')

            if len(sp) == 2:
                tmp = [f'{base}{reg}/{year}/{sp[0]}/{group}', f'{base}{reg}/{year}/{sp[1]}/{group}']
                link_list.extend(tmp)
            else:
                tmp = [f'{base}{reg}/{year}/{sp}/{group}']
                link_list.extend(tmp)

            if playoffs:
                link_list.extend([f'{i}/Playoffs' for i in tmp])

    return link_list


def _retrieve_post_match_site_links(ext_link: list, render: bool) -> list:
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


def match_links(config_path: str, render: bool=True) -> list:
    """match_links

    Retrieves the links to the match history pages from the liquidpedia website.

    :param config_path (str): The path to the config.ini file
    :param render (bool): If JavaScript should be rendered on the page
    :rtype list
    """

    exts = _ext_link_creation(config_path)
    links = _retrieve_post_match_site_links(ext_link=exts, render=render)

    return links
