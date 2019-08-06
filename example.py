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

# pprint(parseMatchHist._format_matchHistory_players(full_json))
pprint(parseMatchHist._format_timeLine_players(full_json))
