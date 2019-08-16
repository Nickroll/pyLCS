#!/usr/bin/env python

import hypothesis.strategies as st


def json_strat(depth=5):
    return st.recursive(st.floats() | st.booleans() | st.text() | st.none(),
                        lambda children: st.dictionaries(st.text(), children), max_leaves=depth)
