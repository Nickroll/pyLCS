# /usr/bin/env python

import json

from pyLCS import (liquidCrawler, matchCrawler, parseMatchHist, parseTimeline,
                   saveJSON)

with open('tlTest.json', 'r') as jf:
    tldata = json.load(jf)

tldata = parseTimeline._parse_tl_player_data(tldata)

with open('test.json', 'r') as f:
    data = json.load(f)

stats = parseMatchHist.get_stats(data)
fixed = parseTimeline._fix_pid_with_name(tldata, stats)


# cols = parseMatchHist.get_columns(data)
# saveJSON.make_sql_table('test.db', 'testtable', cols)
# saveJSON.insert_stats('test.db', 'testtable', stats)
