# /usr/bin/env python

import json

import pandas as pd
from pyLCS import liquidCrawler, matchCrawler, saveJSON

# lc = liquidCrawler.liquidCrawler(region='na', year=2019, split='spring', playoffs=False)
# mls = lc.match_links(render=True)
#
# mc = matchCrawler.download_json_data(mls[0])
#
# NOTES: SQLite DBS: Player end match stats, player timeline stats, team match, team timeline
# NOTES: gameId and player name is key for sqlite server
# NOTES: Link timeline and match history
# NOTES: Link player and team

#with open('test.json', 'w') as f:
#    json.dump(mc['MatchHistory'], f, indent=4)

# with open('flat.json', 'w') as f:
#     to_dump = saveJSON.flatten_json(mc['MatchHistory'])
#     json.dump(to_dump, f)

with open('flat.json', 'r') as jf:
    data = json.load(jf)

#p_list = list()
#for i in range(0, 10):
#    key = f'participantIdentities_{i}_player_summonerName'
#    name = data[key]
#    stats_key = f'ants_{i}_'
#
#    for k, v in data.items():
#        if stats_key in k.lower():
#            test = [name, i, k, v]
#
#print(test)

stats = saveJSON._parse_player_json_data(data)
cols = saveJSON._column_names_match_hist(data)
col_list = saveJSON._create_column_name_and_type(cols, stats)
print(len(col_list))
# TODO: FIX THE ORDER OF THE COLUMNS
x = list(zip(cols, stats['TL Impact']))
print(x)
