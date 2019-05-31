# /usr/bin/env python

import json

from pyLCS import (liquidCrawler, matchCrawler, parseMatchHist, parseTimeline,
                   saveJSON)

with open('tlTest.json', 'r') as jf:
    data = json.load(jf)

print(parseTimeline._parse_tl_player_data(data)[8][10])
print(parseTimeline._parse_tl_player_data(data))
# stats = parseMatchHist.get_stats(data)
# cols = parseMatchHist.get_columns(data)
#
# saveJSON.make_sql_table('test.db', 'testtable', cols)
# saveJSON.insert_stats('test.db', 'testtable', stats)
