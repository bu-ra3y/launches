import re
import sys
from pathlib import Path

import PyQt4
from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebPage
from bs4 import BeautifulSoup

"""
This module contains code to bring back info about the reentry of TIANGONG 1. 

You can have this display on your Macbook Pro Touchbar using BetterTouchTool > TouchBar > Add Widget.
 
 Either use "Run Applescript" with code like:

    return do shell script "/Users/will/miniconda3/envs/ROCKETS/bin/python -W ignore
    /Users/will/PycharmProjects/rockets/reentries.py" 

 Or use "Shell script" with code like:
    /bin/bash -c /Users/will/miniconda3/envs/ROCKETS/bin/python -W ignore /Users/will/PycharmProjects/rockets/reentries.py

 Note the '-W ignore' option to Python so that it doesn't report errors on STDERR

"""



this_file:Path = Path(__file__)
data_file:Path = (this_file.parent / "data" / this_file.name).with_suffix('.txt')


def persist_answer(string: str):
    data_file.parent.mkdir(exist_ok=True, parents=True) # make sure the directory exists
    if data_file.exists():
        data_file.unlink() # first remove the data file
    data_file.write_text(string)

def recall_answer():
    try:
        return f"{data_file.read_text()}*"
    except FileNotFoundError:
        return "TIANGONG 1: ?"

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



try:
    url = 'http://www.satview.org/?sat_id=37820U'
    client_response = Client(url=url)
    source = client_response.mainFrame().toHtml()
    soup = BeautifulSoup(source, 'lxml')
    # string is like: TIANGONG 1 - Time to Reenter: 52d 0h 36m 21s
    reentry_string = \
        soup.find_all('div', attrs={'id': 'main_track'})[0]\
            .find_all('div', attrs={'id': 'infobar'})[0].findChild('b').text
except:
    print(f"{recall_answer()}")
else:
    match = re.compile("^(?P<debris>.*) - Time to Reenter: (?P<time>.*)$").search(reentry_string)
    debris = match.groupdict()['debris']
    time_string = match.groupdict()['time']
    time_match = re.compile("^(?P<days>\d+)d (?P<hours>\d+)h (?P<minutes>\d+)m (?P<seconds>\d+)s$").search(time_string)
    days = time_match.groupdict()['days']
    hours = time_match.groupdict()['hours']
    report = f"{debris}: {days}d:{hours}h"
    persist_answer(string=report)
    print(report)

