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

print(pd.read_json('flat.json'))
