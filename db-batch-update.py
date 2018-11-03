import config
import csv
from itertools import islice

from utils.args import get_args
from utils.db_connect import connect_to_mysql_db

#
# Writes a local csv to mysql in batches.  Invoke on command line with
# `python db-batch-update.py  -t <table_name> -b <batch_size> -s <start index> -f <filepath>`
#


def get_table_config(table_name):
    # Add new jobs/table configs here.
    jobs = {
        "order": {
            'query': "INSERT INTO orders (quantity, price, product_name) VALUES (%s, %s, %s)",
            'col_types': [int, float, str]
        }
    }

    return jobs[table_name]


def read_file(filename, col_types, batch_count, start):
    """
    :param filename: name of the file (string)
    :param col_types: structure of the table (list)
    :param batch_count: number of records per batch (int)
    :param start: row to start from (int)
    :return: yields records in batches
    """
    batch = []
    with open(filename) as csv_file:
        # if your csv is not space delimited, change this
        reader = csv.reader(csv_file, delimiter='\t')
        count = 0

        for i, row in islice(enumerate(reader), start, None):
            typed_row = convert_types(row, col_types)
            batch.append(typed_row)
            count += 1

            if count % batch_count == 0:
                yield batch, count
                batch = []

        # after the last batch yield the remainder
        if batch:
            yield batch, count


def convert_types(row, col_types):
    return [col_types[col](row[col]) for col in range(len(row))]


def process(args):
    """
    :param args: parsed args
    :return: executes query in jobs.table_name for each batch
    """
    table_props = get_table_config(args.write_table)
    col_types = table_props['col_types']
    batch_size = args.batch_size
    start = args.start_row
    file_path = args.file_path

    for batch, count in read_file(file_path, col_types, batch_size, start):
        # cursor.executemany(table_props['query'], batch)
        # connection.commit()
        # print(cursor._last_executed)
        print("Processed {} rows".format(count))


if __name__ == "__main__":

    try:
        cli_args = [
            {
                "short": "-b",
                "help": "number of records to process per batch",
                "dest": "batch_size",
                "type": int,
            },
            {
                "short": "-f",
                "help": "absolute path of csv file",
                "dest": "file_path",
                "type": str
            },
            {
                "short": "-s",
                "help": "row number to start with",
                "dest": "start_row",
                "type": int,
                "default": 0
            },
            {
                "short": "-t",
                "help": "write to table",
                "dest": "write_table",
                "type": str
            }
        ]
        parsed_args = get_args(cli_args)

        connection = connect_to_mysql_db(config.DATABASES['cmos_db']['connection'])
        cursor = connection.cursor()
        process(parsed_args)

    except Exception as e:
        print(e)
    finally:
        connection.close()
        print("Connection closed. Total affected rows = {}".format(cursor.rowcount))
