#!/usr/bin/env python
"""
Function for insertion of JSON-like data into a mongo database using JSON-like data returned by
parseMatchHist.parse_match_history().
"""

from typing import List, Union


def insert_into_mongoDB(merged_data: Union[str, List[dict]], collection_set: str, database: str, collection: str, check: str) -> None:
    """insert_into_mongoDB

    Insertes data returned by parseMatchHist.parse_match_history into a mongoDB collection

    :param merged_data (Union[str, List[dict]): The data from parseMatchHist.parse_match_history
    :param collection_set (str): One of players, team, or gameinfo
    :param database (stre: The database  to insert into
    :param collection (str): The collection for insertion
    :rtype None
    """

    if not isinstance(merged_data, list):
        merged_data = [merged_data]

    for i in merged_data:
        insert_dict = dict()

        value = i['GameInfo']['gameId']
        if collection_set.lower() in ['player', 'players']:
            for k, v in i['Player'].items():
                insert_dict = {'playerName': k, 'gameId': i['GameInfo']['gameId']}

                for ikey, ivalue in v.items():
                    insert_dict[ikey] = ivalue

                if check:
                    if database[collection].count_documents({'gameId': value, 'playerName': k}) == 0:
                        database[collection].insert_one(insert_dict)
                    else:
                        print('Document already exists in collection and skipped.')
                        continue
                else:
                    database[collection].insert_one(insert_dict)

        elif collection_set.lower() in ['team', 'teams']:
            for k, v in i['Team'].items():
                insert_dict = {'teamName': k, 'gameId': i['GameInfo']['gameId']}
                for ikey, ivalue in v.items():
                    insert_dict[ikey] = ivalue

                if check:
                    if database[collection].count_documents({'gameId': value, 'teamName': k}) == 0:
                        database[collection].insert_one(insert_dict)
                    else:
                        print('Document already exists in collection and skipped.')
                        continue
                else:
                    database[collection].insert_one(insert_dict)

        elif collection_set.lower() == 'gameinfo':
            for k, v in i['GameInfo'].items():
                insert_dict[k] = v

            if check:
                if database[collection].count_documents({'gameId': value}) == 0:
                    database[collection].insert_one(insert_dict)
                else:
                    continue
            else:
                database[collection].insert_one(insert_dict)
        else:
            raise(KeyError(f'Collection set {collection_set} was not found in merged_data'))

    return None
