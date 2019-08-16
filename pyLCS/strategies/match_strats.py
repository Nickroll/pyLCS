#!/usr/bin/env python

import hypothesis.strategies as st


def valid_match_history_links():
    return st.from_regex(r'[^\s]*(ESPORTSTMNT)[^\s]*(\?)[^\s]*', fullmatch=True)


def invalid_match_historoy_links_sports():
    return st.from_regex(r'[^\sE]*(?!ESPORTSTMNT)[^\sE]*(\?)[^\sE]*', fullmatch=True)


def invalid_match_historoy_links_q():
    return st.from_regex(r'[^\s\?]*(ESPORTSTMNT)[^\s\?]*', fullmatch=True)


def valid_http_links():
    return st.from_regex(r'(http[s]?:\/\/)[a-z]+(\.com\/)\w*', fullmatch=True)
