"""Download module to get tv schedules"""


import requests
import pandas as pd

from parsers import ESPNParser

# URL_DATE = 'http://espn.uol.com.br/programacao?date=2017-08-13'
URL = 'http://espn.uol.com.br/programacao'


def main():
    '''Donwloads and generates csv file for the tv schedule.'''
    response = requests.get(URL)

    parser = ESPNParser()
    channels_data = parser.parse(response.text)

    data = pd.DataFrame(channels_data)
    data.to_csv('out.csv', encoding='utf-8')


if __name__ == '__main__':
    main()
