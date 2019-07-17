# /usr/bin/env python

import json

from pyLCS import (liquidCrawler, matchCrawler, parseMatchHist, parseTimeline,
                   saveJSON)

with open('tlTest.json', 'r') as jf:
    tldata = json.load(jf)


with open('test.json', 'r') as f:
    data = json.load(f)

stats = parseMatchHist.get_stats(data)
fixed = parseTimeline.timeline_stats(tldata, stats, 15)

with open('fixed.json', 'w') as jf:
    json.dump(fixed, jf, indent=4)

# cols = parseMatchHist.get_columns(data)
# saveJSON.make_sql_table('test.db', 'testtable', cols)
# saveJSON.insert_stats('test.db', 'testtable', stats)
