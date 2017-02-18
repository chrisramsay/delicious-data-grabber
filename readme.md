

```python
from bs4 import BeautifulSoup
import datetime
import pprint
import urllib
import json
```


```python
url = 'https://del.icio.us/someoneorother?&page=1'
r = urllib.urlopen(url)
```


```python
soup = BeautifulSoup(r, 'html.parser')
```


```python
thumbs = soup.find_all("div", class_="articleThumbBlockOuter")
```


```python
len(thumbs)
```




    10



Essentially, we need 6 things:

* title
* url
* add date
* private
* tags
* comment (or title if no description)

```
{
    "add_date": "2014-10-30 18:08:05 -0400",
    "comment": "This article describes JavaScript for Automation, a new feature in OS X Yosemite.",
    "private": "0",
    "tags": [
        "javascript",
        "mac",
        "osx",
        "yosemite"
    ],
    "title": "JavaScript for Automation Release Notes",
    "url": "https://developer.apple.com/library/mac/releasenotes/InterapplicationCommunication/RN-JavaScriptForAutomation/index.html#//apple_ref/doc/-%20uid/TP40014508"
}
```


```python
entry = {}
one = thumbs[0]
```


```python
title = one.find_all('div', class_='articleTitlePan')[0]
entry['title'] = title.a.attrs['title']
print entry
```

    {'title': u'GitHub API v3 | GitHub Developer Guide'}



```python
href = one.find_all('div', class_='articleInfoPan')[0].find_all('p')[0]
entry['url'] = href.a.attrs['href']
print entry
```

    {'url': u'https://developer.github.com/v3/', 'title': u'GitHub API v3 | GitHub Developer Guide'}



```python
entry['add_date'] = str(datetime.datetime.fromtimestamp(int(one.attrs['date'])))
entry['add_epoch'] = one.attrs['date']
print entry
```

    {'url': u'https://developer.github.com/v3/', 'add_date': '2016-11-05 14:10:53', 'tags': [u'api', u'github'], 'comment': u'A description here', 'title': u'GitHub API v3 | GitHub Developer Guide'}



```python
try:
    tags = one.find_all('ul', class_='tagName')[0].find_all('li')
except IndexError:
    tags = ''
```


```python
entry['tags'] = [f.a.text for f in tags]
print entry
```

    {'url': u'https://developer.github.com/v3/', 'add_date': '2016-11-05 14:10:53', 'tags': [u'api', u'github'], 'title': u'GitHub API v3 | GitHub Developer Guide'}



```python
comment = None
for a in [l for l in one.find('div', class_='thumbTBriefTxt').children]:
    try:
        comment = a.p.contents[0]
    except AttributeError:
        continue
```


```python
if comment is not None:
    entry['comment'] = comment
else:
    entry['comment'] = entry['title']
print entry
```

    {'url': u'https://developer.github.com/v3/', 'add_date': '2016-11-05 14:10:53', 'tags': [u'api', u'github'], 'comment': u'A description here', 'title': u'GitHub API v3 | GitHub Developer Guide'}



```python
json.dumps(entry)
```




    '{"url": "https://developer.github.com/v3/", "add_date": "2016-11-05 14:10:53", "tags": ["api", "github"], "comment": "A description here", "title": "GitHub API v3 | GitHub Developer Guide"}'



Next, let's make a function that basically does the above.


```python
def get_entry(bookmark):
    entry = {}
    title = bookmark.find_all('div', class_='articleTitlePan')[0]
    entry['title'] = title.a.attrs['title']
    href = bookmark.find_all('div', class_='articleInfoPan')[0].find_all('p')[0]
    entry['url'] = href.a.attrs['href']
    entry['add_date'] = str(datetime.datetime.fromtimestamp(int(bookmark.attrs['date'])))
    entry['private'] = 0
    try:
        tags = bookmark.find_all('ul', class_='tagName')[0].find_all('li')
        entry['tags'] = [f.a.text for f in tags]
    except IndexError:
        tags = None
    comment = None
    for a in [l for l in bookmark.find('div', class_='thumbTBriefTxt').children]:
        try:
            comment = a.p.contents[0]
        except AttributeError:
            continue
    if comment is not None:
        entry['comment'] = comment
    else:
        entry['comment'] = entry['title']
    return entry
```

Testing:


```python
get_entry(thumbs[0])
```




    {'add_date': '2016-11-05 14:10:53',
     'comment': u'A description here',
     'private': 0,
     'tags': [u'api', u'github'],
     'title': u'GitHub API v3 | GitHub Developer Guide',
     'url': u'https://developer.github.com/v3/'}


