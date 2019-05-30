# /usr/bin/env python

import json

from pyLCS import liquidCrawler, matchCrawler, parseMatchHist, saveJSON

with open('test.json', 'r') as jf:
    data = json.load(jf)



stats = parseMatchHist.get_stats(data)
cols = parseMatchHist.get_columns(data)

saveJSON.make_sql_table('test.db', 'testtable', cols)
saveJSON.insert_stats('test.db', 'testtable', stats)
