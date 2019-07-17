# /usr/bin/env python

import json

from pyLCS import (liquidCrawler, matchCrawler, parseMatchHist, parseTimeline,
                   saveJSON)

with open('tlTest.json', 'r') as jf:
    tldata = json.load(jf)

parse_data = parseTimeline._parse_tl_player_data(tldata)

with open('test.json', 'r') as f:
    data = json.load(f)

stats = parseMatchHist.get_stats(data)
events = parseTimeline._parse_event_data(tldata, parse_data)
fixed = parseTimeline._fix_pid_with_names(events, stats)

with open('fixed.json', 'w') as jf:
    json.dump(fixed, jf, indent=4)


# cols = parseMatchHist.get_columns(data)
# saveJSON.make_sql_table('test.db', 'testtable', cols)
# saveJSON.insert_stats('test.db', 'testtable', stats)
