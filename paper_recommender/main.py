import argparse

from db_manager import PaperDBManager


def _parse_user_args():
    """
    Parses the user arguments
    :returns: user arguments
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-d', '--database', help='the name of the database', required=True)
    arg_parser.add_argument('-pwd', '--password', nargs='?', default=None, help='database password, defaults to None')
    arg_parser.add_argument('-u', '--username', nargs='?', default=None, help='database user, defaults to None')
    arg_parser.add_argument('-f', '--files', help='the json files to parse the data from (space separated)',
                            required=True)
    arg_parser.add_argument('-p', '--port', nargs='?', default=27017, help='database port, defaults to 27017')
    return arg_parser.parse_args()


def run_exercise():
    args = _parse_user_args()
    # Establish the db connection and create the data
    db_manager = PaperDBManager.create(database=args.database,
                                       password=args.password,
                                       username=args.username,
                                       port=args.port)
    db_manager.insert_data_from_json(args.files.split(' '))
    db_manager.add_indexes()
    db_manager.close()


if __name__ == '__main__':
    run_exercise()