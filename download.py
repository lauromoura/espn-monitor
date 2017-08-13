"""Download module to get tv schedules"""


from datetime import date

import pandas as pd

from parsers import ESPNFetcher



def main():
    '''Donwloads and generates csv file for the tv schedule'''

    fetcher = ESPNFetcher()

    channels_data = fetcher.get(target_date=date.today())

    channels_data.to_csv('%s-%s.csv' % (fetcher.name(), date.today()), encoding='utf-8')


if __name__ == '__main__':
    main()
