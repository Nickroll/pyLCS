#!/usr/bin/env python

import hypothesis.strategies as st
from pyLCS.liquidCrawler import liquidCrawler


def build_liquidCrawler():
    return st.builds(liquidCrawler, st.text(), st.integers(min_value=0), st.text(), st.booleans())


def man_build_liquidCrawler():
    return st.tuples(st.text(), st.integers(min_value=0), st.text(), st.booleans())


def build_validLiquidCrawler():
    possible_regions = ['na', 'lcs', 'lck', 'korea', 'lms', 'eu', 'europe', 'lec', 'academy']
    return st.builds(liquidCrawler, st.sampled_from(possible_regions), st.integers(min_value=0),
                     st.text(), st.booleans())


def build_invalid_regions():
    possible_regions = ['na', 'lcs', 'lck', 'korea', 'lms', 'eu', 'europe', 'lec', 'academy']

    return st.text().filter(lambda x: x not in possible_regions)
