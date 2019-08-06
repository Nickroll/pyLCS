# /usr/bin/env python

import json

from pyLCS import (liquidCrawler, matchCrawler, parseMatchHist, parseTimeline,
                   saveJSON)

lc = liquidCrawler.liquidCrawler('NA', 2019, 'Spring', False)
links = lc.match_links()
links = links[0]

json_data = matchCrawler.download_json_data(links)

with open('full_json.json', 'w') as jf:
    json.dump(json_data, jf, indent=4)
