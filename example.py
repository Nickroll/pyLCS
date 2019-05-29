# /usr/bin/env python

import json

from pyLCS import liquidCrawler, matchCrawler, saveJSON

with open('test.json', 'r') as jf:
    data = json.load(jf)

col_list = saveJSON.get_columns(data)
stats = saveJSON.get_stats(data)

saveJSON.make_sql_table('test.db', 'testtable', col_list)
saveJSON.insert_stats('test.db', 'testtable', stats)
