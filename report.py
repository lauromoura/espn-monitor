'''Basic reporting'''

import argparse

import pandas as pd


def main():
    '''Shows some basic reports'''
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', action='store', metavar='FILE',
                        help='Input file')
    parser.add_argument('--list-others', action='store_true',
                        help='List programs in category "others"')

    args = parser.parse_args()

    data = pd.DataFrame.from_csv(args.filename, encoding='utf-8',)
    data['duration'] = pd.to_timedelta(data['duration'])

    print("Total de horas agrupadas por categoria e canal")
    #pylint: disable=maybe-no-member
    group = data.groupby(['category', 'channel'])['duration'].sum()
    print(group.sort_values(ascending=False))
    print()
    print("Total de horas agrupadas por categoria apenas")
    group = data.groupby('category')['duration'].sum()
    print(group.sort_values(ascending=False))

    if args.list_others:
        print()
        print(data[data['category'] == 'outros']['name'])

if __name__ == '__main__':
    main()
