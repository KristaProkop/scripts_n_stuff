import MySQLdb


def connect_to_mysql_db(db):
    """
    :param db: database config dict
    :return: db connection obj
    """
    connection = MySQLdb.connect(
        host=db['host'],
        user=db['user'],
        passwd=db['passwd'],
        db=db['db']
    )
    if connection.open:
        print('connected to db {}'.format(db['db']))
    return connection
