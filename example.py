# /usr/bin/env python

import json
from pprint import pprint

from pyLCS import (liquidCrawler, matchCrawler, parseMatchHist, parseTimeline,
                   saveJSON)

# lc = liquidCrawler.liquidCrawler('NA', 2019, 'Spring', False)
# links = lc.match_links()
# links = links[0]

# json_data = matchCrawler.download_json_data(links)

with open('full_json.json', 'r') as jf:
    full_json = json.load(jf)

mh_data = parseMatchHist._format_matchHistory_players(full_json)
timeline_data = parseMatchHist._format_timeLine_players(full_json)
unwanted = {'SKILL_LEVEL_UP', 'ITEM_DESTROYED', 'ITEM_SOLD', 'WARD_PLACED', 'WARD_KILL',
            'ITEM_UNDO', 'ITEM_PURCHASED'}

tl_data = parseMatchHist._parse_event_data_players(full_json, timeline_data, 15, unwanted)
game_info = parseMatchHist._game_information(full_json)
team_data = parseMatchHist._format_team_information(full_json)

merge = parseMatchHist._merge_formats_together(mh_data, timeline_data, team_data, game_info)

with open('merge.json', 'w') as jf:
    json.dump(merge, jf, indent=4)
