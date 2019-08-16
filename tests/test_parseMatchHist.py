#!/usr/bin/env python

import context
import pytest
from hypothesis import assume, given
from pyLCS import parseMatchHist
from pyLCS.exceptions import pyLCSExceptions
from pyLCS.strategies import parse_strats


@given(parse_strats.json_strat())
def test_flatten_flattens(j):
    assume(j is not None)
    flat = parseMatchHist._flatten_json(j)

    assert all(not isinstance(l, (dict, list, tuple)) for l in flat.values())
