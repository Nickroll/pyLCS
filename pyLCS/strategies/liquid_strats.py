#!/usr/bin/env python

import hypothesis.strategies as st
from pyLCS.liquidCrawler import liquidCrawler


def build_liquidCrawler():
    return st.builds(liquidCrawler, st.text(), st.integers(min_value=0), st.text(), st.booleans())


def man_build_liquidCrawler():
    return st.tuples(st.text(), st.integers(min_value=0), st.text(), st.booleans())
