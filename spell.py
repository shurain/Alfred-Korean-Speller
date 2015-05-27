import sys
import unicodedata

import requests
from bs4 import BeautifulSoup
import bs4


# First, fetch current version of the speller
url = 'http://speller.cs.pusan.ac.kr/'
checker_url = '/lib/check.asp'

r = requests.get(url)
soup = BeautifulSoup(r.content)

frame_src = soup.find_all('frame')[0]['src'].split('/')[-2]

full_url = url + frame_src + checker_url

query = sys.argv[1]
q = query.decode('utf-8')
q = unicodedata.normalize("NFC", q)
q = q.encode('utf-8')

r = requests.post(full_url, data={'text1': q})

soup = BeautifulSoup(r.content)

err = soup.find_all('td', id=lambda x: x and x.startswith('tdErrorWord_'))
rep = soup.find_all('td', id=lambda x: x and x.startswith('tdReplaceWord_'))

for x, y in zip(err, rep):
    print x.contents[0].encode('utf-8'),
    print "\n\t->",
    print '\n\t-> '.join([x for x in y.contents if type(x) != bs4.element.Tag]).encode('utf-8')
