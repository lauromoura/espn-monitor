from datetime import datetime, timedelta
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
import pandas as pd

from categories import get_category

URL = 'http://espn.uol.com.br/programacao'
DATE_FORMAT = '%d/%m/%Y %H:%M %z'

def date_from_str(string, has_tz=False, tz="-0300"):
    if not has_tz:
        string += ' ' + tz

    return datetime.strptime(string, DATE_FORMAT)

def parse_channel(channel_section, channel_name):
    '''Parses channel schedule into a dict'''
    program_div = channel_section.div

    program_list = []
    programs = program_div.find_all('article')

    for program in programs:
        program_data = {}

        # start_time = datetime.strptime(program.time['datetime'],
        start_str = program.a.find('span', class_='_start').text
        start_time = date_from_str(start_str)

        end_str = program.a.find('span', class_='_end').text
        end_time = date_from_str(end_str)

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


def main():
    response = requests.get(URL)

    soup = BeautifulSoup(response.text, 'html.parser')

    channels_div = soup.find(id='channels')

    sections = channels_div.find_all('section')

    channels_data = []

    for section in sections:
        channel_name = section.find('h4').text
        channels_data += parse_channel(section, channel_name)

    data = pd.DataFrame(channels_data)
    data.to_csv('out.csv', encoding='utf-8')


if __name__ == '__main__':
    main()
