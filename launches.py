import argparse
from pprint import pprint

import sys
from typing import List, NewType, Tuple, Iterable

import urllib3
from bs4 import BeautifulSoup

# to suppress the warning: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised
urllib3.disable_warnings()

month = dict(
    January='Jan',
    February='Feb',
    March='Mar',
    April='Apr',
    May='May',
    June='Jun',
    July='Jul',
    August='Aug',
    September='Sep',
    October='Oct',
    November='Nov',
    December='Dec',
)

Launch_Name = NewType('Launch_Name', str)
Launch_Date = NewType('Launch_Date', str)
Launch = NewType('Launch', Tuple[Launch_Date, Launch_Name])


def launches() -> Iterable[Launch]:
    url = 'http://spaceflightnow.com/launch-schedule/'
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, 'lxml')
    missions = soup.findAll('div', attrs={'class': 'datename'})
    spacex_missions = [(list(m.children)[0].text, list(m.children)[1].text) for m in missions]
    clean = [(d.replace("NET ", "").replace(".", ""), n.replace(u' \u2022', ":")) for d, n in spacex_missions]
    return clean


def max_length(items):
    return max(len(i) for i in items)


def next_launch(rocket: str = None) -> Launch:
    for date, name in launches():
        if rocket: # Are we filtering on rocket name?
            if rocket in name:
                return (date, name)
        else: # no filter
            return (date, name)


def print_next_launch_for_rocket(rocket: str, alias: str = None) -> None:
    """
    Print a string indicating the next launch for the given rocket.

    :param rocket: If this string is contained in the mission name, we match.
    :param alias: When printing results, this alias will be used instead of the rocket name, if supplied.
    """
    if alias:
        prefix = alias
    else:
        prefix = rocket

    print_launch_date(launch=next_launch(rocket=rocket), prefix=prefix + ": ")


def print_launch_date(launch: Launch, prefix: str = ""):
    date, name = launch
    print("{}{}".format(prefix, date))


def print_launches():
    space_for_date = 3 + max_length(d for d, n in launches())
    template = "{: <" + str(space_for_date) + "} {}"

    for date, name in launches():
        print(template.format(date, name))


def print_next_launch_date():
    print_launch_date(launch=next_launch())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find out about upcoming rocket launches.')
    parser.add_argument('--rocket', help='Get next launch for the specified rocket.')
    parser.add_argument('--alias', help='Use this name for the rocket when printing results.')

    args = vars(parser.parse_args())

    if args['rocket']:
        print_next_launch_for_rocket(rocket=args['rocket'], alias=args['alias'])
    else:
        print_launches()