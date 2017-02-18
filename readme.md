
## del.icio.us Link Fetching

Below is an outline for building a rough & ready script to get del.icio.us bookmark data.

Get the modules we need.


```python
from bs4 import BeautifulSoup
import datetime
import pprint
import urllib
import json
```

Fetch a URL, parse with BS to get outer blocks.


```python
url = 'https://del.icio.us/chrisramsay?&page=1'
r = urllib.urlopen(url)
soup = BeautifulSoup(r, 'html.parser')
thumbs = soup.find_all("div", class_="articleThumbBlockOuter")
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
Get the entry title:


```python
entry = {}
one = thumbs[0]
title = one.find_all('div', class_='articleTitlePan')[0]
entry['title'] = title.a.attrs['title']
print entry
```

    {'title': u'GitHub API v3 | GitHub Developer Guide'}


Get the URL:


```python
href = one.find_all('div', class_='articleInfoPan')[0].find_all('p')[0]
entry['url'] = href.a.attrs['href']
print entry
```

    {'url': u'https://developer.github.com/v3/', 'title': u'GitHub API v3 | GitHub Developer Guide'}


Get the save date:


```python
entry['add_date'] = str(datetime.datetime.fromtimestamp(int(one.attrs['date'])))
entry['add_epoch'] = one.attrs['date']
print entry
```

    {'url': u'https://developer.github.com/v3/', 'add_date': '2016-11-05 14:10:53', 'add_epoch': u'1478355053', 'title': u'GitHub API v3 | GitHub Developer Guide'}


Get the tags (if there are any):


```python
try:
    tags = one.find_all('ul', class_='tagName')[0].find_all('li')
except IndexError:
    tags = ''
entry['tags'] = [f.a.text for f in tags]
print entry
```

    {'url': u'https://developer.github.com/v3/', 'add_date': '2016-11-05 14:10:53', 'add_epoch': u'1478355053', 'tags': [u'api', u'github'], 'title': u'GitHub API v3 | GitHub Developer Guide'}


Get any comments:


```python
comment = None
for a in [l for l in one.find('div', class_='thumbTBriefTxt').children]:
    try:
        comment = a.p.contents[0]
    except AttributeError:
        continue
if comment is not None:
    entry['comment'] = comment
else:
    entry['comment'] = entry['title']
print entry
```

    {'comment': u'A description here', 'add_epoch': u'1478355053', 'tags': [u'api', u'github'], 'url': u'https://developer.github.com/v3/', 'title': u'GitHub API v3 | GitHub Developer Guide', 'add_date': '2016-11-05 14:10:53'}


Take a look at the whole bookmark as a JSON string dump:


```python
json.dumps(entry)
```




    '{"comment": "A description here", "add_epoch": "1478355053", "tags": ["api", "github"], "url": "https://developer.github.com/v3/", "title": "GitHub API v3 | GitHub Developer Guide", "add_date": "2016-11-05 14:10:53"}'



Next, let's make a function that basically does the above.


```python
def get_entry(bookmark):
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
link = json.dumps(get_entry(thumbs[2]))
print link
```

    {"comment": "PyFormat: Using % and .format() for great good!", "add_epoch": "1477929520", "tags": ["python", "datetime"], "url": "https://pyformat.info/", "title": "PyFormat: Using % and .format() for great good!", "private": 0, "add_date": "2016-10-31 15:58:40"}


## Making an importable bookmarks HTML file
Desired link text:

```
<DT><A HREF="https://link.com/something" ADD_DATE="1414706885" PRIVATE="0" TAGS="tag1,tag2">Link text</A>
```


```python
bm_load = json.loads(link)
print bm_load
```

    {u'comment': u'PyFormat: Using % and .format() for great good!', u'add_epoch': u'1477929520', u'title': u'PyFormat: Using % and .format() for great good!', u'url': u'https://pyformat.info/', u'tags': [u'python', u'datetime'], u'private': 0, u'add_date': u'2016-10-31 15:58:40'}



```python
'<DT><A HREF="{}" ADD_DATE="{}" PRIVATE="0" TAGS="{}">{}</A>'.format(
    bm_load['url'], bm_load['add_epoch'], ','.join(bm_load['tags']), bm_load['comment']
)
```




    '<DT><A HREF="https://pyformat.info/" ADD_DATE="1477929520" PRIVATE="0" TAGS="python,datetime">PyFormat: Using % and .format() for great good!</A>'




```python

```
