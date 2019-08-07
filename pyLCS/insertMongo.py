#!/usr/bin/env python


def insert_into_mongoDB(merged_data: dict=None, collection_set: str=None, database: str=None, collection: str=None) -> None:
    """insert_into_mongoDB

    Insertes data returned by parseMatchHist.parse_match_history into a mongoDB collection

    :param merged_data (dict): The data from parseMatchHist.parse_match_history
    :param collection_set (str): One of players, team, or gameinfo
    :param database (str): The database  to insert into
    :param collection (str): The collection for insertion
    :rtype None
    """

    insert_dict = dict()

    if collection_set.lower() in ['player', 'players']:

        for k, v in merged_data['Player'].items():
            insert_dict = {'PlayerName': k, 'GameId': merged_data['GameInfo']['gameId']}
            for ikey, ivalue in v.items():
                insert_dict[ikey] = ivalue

            database[collection].insert_one(insert_dict)

    elif collection_set.lower() in ['team', 'teams']:
        for k, v in merged_data['Team'].items():
            insert_dict = {'TeamName': k, 'GameId': merged_data['GameInfo']['gameId']}
            for ikey, ivalue in v.items():
                insert_dict[ikey] = ivalue

            database[collection].insert_one(insert_dict)

    elif collection_set.lower() == 'gameinfo':
        for k, v in merged_data['GameInfo'].items():
            insert_dict[k] = v

        database[collection].insert_one(insert_dict)

    return None
