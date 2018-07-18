from utils.baseutils import get_directory, get_filepath
from utils.db_utils import load_db, update_db

import os


def kw_cache_wrapper(cache_key='temp_key', cache_name='temp.json', debug=False):
    # https://stackoverflow.com/questions/5929107/decorators-with-parameters
    def real_decorator(function_in):
        try:
            db_dir = get_directory("aodh-backend/db")
        except SystemError:
            db_dir = get_directory("/db")
        db_filename = cache_name
        db_filepath = os.path.join(db_dir, db_filename)

        if not os.path.isfile(db_filepath):
            with open(db_filepath, 'w') as f:
                print('new file made at {}'.format(db_filepath))
                f.write('{}')
        else:
            with open(db_filepath, 'r+', encoding='utf-8') as f:
                test = f.read()
                if len(test) == 0:
                    print('file is empty! making it json compatible.')
                    f.write('{}')

        def wrapper(*args, **kwargs):
            # before
            db_path = get_filepath(db_filepath)

            cache_db = load_db(database_path=db_path, debug=debug)
            try:
                cached_output = cache_db[cache_key]
                if debug: print('local keyword pair found!')
                return cached_output
            except:
                print('running function to cache: {}'.format(db_path))
                # ---------------------------------------------
                output_to_cache = function_in(*args, **kwargs)
                # ---------------------------------------------
                # after
                cache_db[cache_key] = output_to_cache
                update_db(cache_db, database_path=db_filepath)
                return output_to_cache
        return wrapper
    return real_decorator
