import argparse

# wrapper around argparse std library


def get_args(args):
    """
    :param args: dict of arg configs
    :return: parsed args
    """
    parser = argparse.ArgumentParser()

    for arg in args:
        parser.add_argument(
            arg['short'],
            help=arg.get('help'),
            dest=arg.get('dest'),
            type=arg.get('type'),
            default=arg.get('default')
        )

    return parser.parse_args()

