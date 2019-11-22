#!/usr/bin/env python

import json
import os

from pyLCS.pyLCS import LCS, mongo_insert
from pymongo import MongoClient

try:
    usr = os.environ['MONGO_USR']
    passw = os.environ['MONGO_PASS']
    extra = os.environ['MONGO_EXTRA']
except KeyError:
    raise Exception('Please make sure to set MONGO_USR, MONGO_PASS, and MONGO_EXTRA environment variables')

lcs_data = LCS(region='na', year=2019, split='spring', playoffs=True)
lcs_data.match_history()

unwanted = {'SKILL_LEVEL_UP', 'ITEM_DESTROYED', 'ITEM_SOLD', 'WARD_PLACED', 'WARD_KILL',
            'ITEM_UNDO', 'ITEM_PURCHASED'}

output = lcs_data.parse_match_history(minute=15, unwanted_types=unwanted)

client = MongoClient(f'mongodb+srv://{usr}:{passw}@{extra}.mongodb.net/test?retryWrites=true&w=majority')
db = client['test']

for i in ['player', 'team', 'gameinfo']:
    mongo_insert(output, i, db, i, check='gameId')
