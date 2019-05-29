# /usr/bin/env python

import json

from pyLCS import liquidCrawler, matchCrawler, saveJSON

with open('flat.json', 'r') as jf:
    data = json.load(jf)

cols, stats = saveJSON._parse_player_json_data(data)
cols = saveJSON._column_names_match_hist(cols)

s = saveJSON._fix_for_sql_instertion(stats)
col_list = saveJSON._create_column_name_and_type(cols, stats)

# LANE AND ROLE ARE USELESS DROP THEM
saveJSON.make_sql_table('test.db', 'testtable', col_list)
saveJSON.insert_stats('test.db', 'testtable', stats)
