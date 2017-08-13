"""Download module to get tv schedules"""


import argparse
from datetime import date, datetime

import pandas as pd

from parsers import ESPNFetcher



ARGUMENT_DATE = '%Y-%m-%d'


def valid_date(string):
    try:
        return datetime.strptime(string, ARGUMENT_DATE).date()
    except ValueError:
        msg = 'Not a valid date: "{0}".'.format(string)
        raise argparse.ArgumentTypeError(msg)


def main():
    '''Donwloads and generates csv file for the tv schedule'''

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start', help='First date to fetch',
                        required=False, default=date.today(),
                        type=valid_date)

    args = parser.parse_args()

    print(args)

    fetcher = ESPNFetcher()

    channels_data = fetcher.get(args.start)

    channels_data.to_csv('%s-%s.csv' % (fetcher.name(), args.start), encoding='utf-8')


if __name__ == '__main__':
    main()
