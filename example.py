#!/usr/bin/env python

import json

from pyLCS import liquidCrawler, matchCrawler, parseMatchHist

lc = liquidCrawler.liquidCrawler('na', 2019, 'Spring', False)
links = lc.match_links()
links = links[:3]


json_data = matchCrawler.download_json_data(links)


# with open('full_json.json', 'r') as jf:
#     full_json = json.load(jf)
#
unwanted = {'SKILL_LEVEL_UP', 'ITEM_DESTROYED', 'ITEM_SOLD', 'WARD_PLACED', 'WARD_KILL',
            'ITEM_UNDO', 'ITEM_PURCHASED'}
#
merge = parseMatchHist.parse_match_history(json_data, 100, unwanted)

with open('merge.json', 'w') as jf:
    json.dump(merge, jf, indent=4)
