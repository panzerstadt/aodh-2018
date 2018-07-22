#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from utils.baseutils import get_filepath

db_file = "./db/db.json"

def load_db(database_path=db_file, debug=False):
    database_path = get_filepath(database_path)
    with open(database_path, encoding='utf-8') as json_db:
        return json.loads(json_db.read())


def update_db(dict_in, database_path=db_file, debug=False):
    with open(database_path, 'r') as json_db:
        state_str = json_db.read()
        state = json.loads(state_str)
        if debug:
            print('current state')
            print(json.dumps(state, indent=4, ensure_ascii=False))
            print('replacing state (this is not redux yet)')

        for k, v in dict_in.items():
            state[k] = dict_in[k]

    with open(database_path, 'w', encoding='utf-8') as json_db:
        if debug:
            print('saving state')
        json.dump(state, json_db, indent=4, ensure_ascii=False)


def make_db(dict_in, database_path, skip_if_exists=True, debug=False):
    try:
        with open(database_path): pass
        if skip_if_exists: return
        response = input('database already exists. overwrite with empty database? (y/N)')

        if response and response == 'y':
            with open(database_path, 'w', encoding='utf-8') as json_db:
                json.dump(dict_in, json_db, indent=4, ensure_ascii=False)
        else:
            return
    except:
        with open(database_path, 'w', encoding='utf-8') as json_db:
            json.dump(dict_in, json_db, indent=4, ensure_ascii=False)