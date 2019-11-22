#!/usr/bin/env python

import json

from pyLCS.pyLCS import LCS, mongo_insert
from pymongo import MongoClient

lcs_data = LCS(region='na', year=2019, split='spring', playoffs=True)
lcs_data.match_history()

unwanted = {'SKILL_LEVEL_UP', 'ITEM_DESTROYED', 'ITEM_SOLD', 'WARD_PLACED', 'WARD_KILL',
            'ITEM_UNDO', 'ITEM_PURCHASED'}

output = lcs_data.parse_match_history(minute=15, unwanted_types=unwanted)


client = MongoClient("")
db = client['test']

for i in ['player', 'team', 'gameinfo']:
    mongo_insert(output, i, db, i, check='gameId')
