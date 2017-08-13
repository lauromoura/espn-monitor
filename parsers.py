'''Parsers to generate the channel data for each channel group.'''


import abc
from datetime import datetime

from bs4 import BeautifulSoup
import requests
import pandas as pd

from categories import get_category


class FetcherBase(metaclass=abc.ABCMeta):
    '''Base class for fetcher classes.

    Each channel group will have its own fetcher.'''

    @abc.abstractmethod
    def get(self, target_date):
        '''fetches data for date 'date' into a dataframe'''

    @abc.abstractmethod
    def name(self):
        '''Returns the name of this fetcher'''

@FetcherBase.register
class ESPNFetcher(FetcherBase):
    '''Fetches data from ESPN Brasil channels'''

    DATE_FORMAT = '%d/%m/%Y %H:%M %z'
    URL = 'http://espn.uol.com.br/programacao'
    NAME = 'ESPN'

    def _parse_channels(self, section, channel_name):
        '''Parses channel schedule into a dict'''
        program_div = section.div

        program_list = []
        programs = program_div.find_all('article')

        for program in programs:
            program_data = {}

            # start_time = datetime.strptime(program.time['datetime'],
            start_str = program.a.find('span', class_='_start').text
            start_time = date_from_str(start_str, self.DATE_FORMAT)

            end_str = program.a.find('span', class_='_end').text
            end_time = date_from_str(end_str, self.DATE_FORMAT)

            duration = end_time - start_time

            name = program.span.text

            program_data['start'] = start_time
            program_data['end'] = end_time
            program_data['duration'] = duration
            program_data['name'] = name
            program_data['category'] = get_category(name)
            program_data['channel'] = channel_name

            program_list.append(program_data)

        return program_list

    def _parse(self, input_data):
        '''Parses data into a list of dicts with each program information.'''
        soup = BeautifulSoup(input_data, 'html.parser')
        channels_div = soup.find(id='channels')
        sections = channels_div.find_all('section')

        data = []
        for section in sections:
            channel_name = section.find('h4').text
            data += self._parse_channels(section, channel_name)

        return pd.DataFrame(data)

    def get(self, target_date):
        '''Gets the data for the given date object'''

        params = {'date': str(target_date)}
        response = requests.get(self.URL, params=params)
        response.raise_for_status()

        return self._parse(response.text)

    def name(self):
        '''The fetcher name.'''
        return self.NAME



# Utility functions

def date_from_str(string, fmt, has_tz=False, timezone_offset="-0300"):
    '''Get datetime from the string format, with default timezone.'''
    if not has_tz:
        string += ' ' + timezone_offset

    return datetime.strptime(string, fmt)
