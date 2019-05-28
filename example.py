# /usr/bin/env python

import json

from pyLCS import liquidCrawler, matchCrawler, saveJSON

with open('flat.json', 'r') as jf:
    data = json.load(jf)

stats = saveJSON._parse_player_json_data(data)
cols = saveJSON._column_names_match_hist(data)
col_list = saveJSON._create_column_name_and_type(cols, stats)

saveJSON.make_sql_database('test.db', 'testname', [('gameid', 'real')])
