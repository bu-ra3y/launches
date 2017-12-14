from pprint import pprint

import sys
import urllib3
from bs4 import BeautifulSoup

# to suppress the warning: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised
urllib3.disable_warnings()

month = dict(
    January = 'Jan',
    February = 'Feb',
    March = 'Mar',
    April = 'Apr',
    May = 'May',
    June = 'Jun',
    July = 'Jul',
    August = 'Aug',
    September = 'Sep',
    October = 'Oct',
    November = 'Nov',
    December = 'Dec',
)


def print_missions(missions):
    space_for_date = 3 + max_length(d for d, n in missions)
    template = "{: <"+ str(space_for_date) +"} {}"

    for date, name in missions:
        print_mission(template, date, name)

def print_mission(template, date, name):
    print(template.format(date, name))


def max_length(items):
    return max(len(i) for i in items)

def upcoming_launches():
    url = 'http://spaceflightnow.com/launch-schedule/'
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, 'lxml')
    missions = soup.findAll('div', attrs={'class': 'datename'})
    spacex_missions = [(list(m.children)[0].text, list(m.children)[1].text) for m in missions if 'Falcon' in list(m.children)[1].text]
    clean = [(d.replace("NET ", "").replace(".", ""), n) for d, n in spacex_missions]
    return clean


def print_upcoming_launches():
    print_missions(upcoming_launches())

def print_next_launch_date():
    next = upcoming_launches()[0][0]
    print("SpaceX: " + next)