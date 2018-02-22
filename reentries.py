import re
import sys

from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebPage
from bs4 import BeautifulSoup

"""
This module contains code to bring back info about the reentry of TIANGONG 1. 

You can have this display on your Macbook Pro Touchbar using BetterTouchTool > TouchBar > Add Widget.
 
 Either use "Run Applescript" with code like:

    return do shell script "/Users/will/miniconda3/envs/ROCKETS/bin/python 
    /Users/will/PycharmProjects/rockets/reentries.py" 

 Or use "Shell script" with code like:
    /bin/bash -c /Users/will/miniconda3/envs/ROCKETS/bin/python /Users/will/PycharmProjects/rockets/reentries.py

"""


class Client(QWebPage):
    """
    From: https://www.youtube.com/watch?v=FSH77vnOGqU
    We need a web client to render the page, specifically, the data we want is placed on the page by a javascript
    script which is only run by a web client.  So, we have to render the page and then pull the text off it.
    """

    def __init__(self, url: str):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        # noinspection PyUnresolvedReferences
        self.loadFinished.connect(self.on_page_load)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def on_page_load(self):
        self.app.quit()


url = 'http://www.satview.org/?sat_id=37820U'
client_response = Client(url=url)
source = client_response.mainFrame().toHtml()

soup = BeautifulSoup(source, 'lxml')

# string is like: TIANGONG 1 - Time to Reenter: 52d 0h 36m 21s
reentry_string = soup.find_all('div', attrs={'id': 'main_track'})[0].find_all('div', attrs={'id': 'infobar'})[0]\
    .findChild('b').text
match = re.compile("^(?P<object>.*) - Time to Reenter: (?P<time>.*)$").search(reentry_string)
debris = match.groupdict()['object']
time_string = match.groupdict()['time']

# print(f"{object} will land in {time_string}")

time_match = re.compile("^(?P<days>\d+)d (?P<hours>\d+)h (?P<minutes>\d+)m (?P<seconds>\d+)s$").search(time_string)
# print(time_match.groupdict())
days = time_match.groupdict()['days']
hours = time_match.groupdict()['hours']

print(f"{object}: {days}d:{hours}h")
