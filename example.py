#!/usr/bin/env python

import json

from pyLCS.pyLCS import LCS

lcs_data = LCS(region='all', year=2019, split='spring', playoffs=True)
lcs_data.match_history()

unwanted = {'SKILL_LEVEL_UP', 'ITEM_DESTROYED', 'ITEM_SOLD', 'WARD_PLACED', 'WARD_KILL',
            'ITEM_UNDO', 'ITEM_PURCHASED'}

output = lcs_data.parse_match_history(minute=15, unwanted_types=unwanted)

with open('json_dump.json', 'w') as jf:
    json.dump(output, jf, indent=4)
