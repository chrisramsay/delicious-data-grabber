#!/usr/bin/env python

"""
Rough and ready script to grab some data from del.icio.us
"""

import urllib
import datetime
import json
from bs4 import BeautifulSoup

def get_entry(bookmark):
    """
    Grab an entry
    """
    entry = {}
    title = bookmark.find_all('div', class_='articleTitlePan')[0]
    entry['title'] = title.a.attrs['title']
    href = bookmark.find_all('div', class_='articleInfoPan')[0].find_all('p')[0]
    entry['url'] = href.a.attrs['href']
    entry['add_date'] = str(datetime.datetime.fromtimestamp(int(bookmark.attrs['date'])))
    entry['add_epoch'] = bookmark.attrs['date']
    entry['private'] = 0
    try:
        tags = bookmark.find_all('ul', class_='tagName')[0].find_all('li')
        entry['tags'] = [f.a.text for f in tags]
    except IndexError:
        entry['tags'] = ''
    comment = None
    for item in [l for l in bookmark.find('div', class_='thumbTBriefTxt').children]:
        try:
            comment = item.p.contents[0]
        except AttributeError:
            continue
    if comment is not None:
        entry['comment'] = comment
    else:
        entry['comment'] = entry['title']
    return entry

if __name__ == '__main__':

    LINKS = []

    for i in range(1, 97):
        url = 'https://del.icio.us/chrisramsay?&page=%i' % i
        r = urllib.urlopen(url)
        soup = BeautifulSoup(r, 'html.parser')
        thumbs = soup.find_all("div", class_="articleThumbBlockOuter")
        final = [get_entry(t) for t in thumbs]
        LINKS += final

    print json.dumps(LINKS)
