import sys
import unicodedata
from ast import literal_eval

import requests
from bs4 import BeautifulSoup
import bs4


def find_parens(s):
    toret = {}
    pstack = []
    for i, c in enumerate(s):
        if c == '[':
            pstack.append(i)
        elif c == ']':
            if len(pstack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            toret[pstack.pop()] = i
    if len(pstack) > 0:
        raise IndexError("No matching opening parens at: " + str(pstack.pop()))
    return toret

full_url = "http://speller.cs.pusan.ac.kr/results"

query = sys.argv[1]
#q = query.decode('utf-8')
q = query
q = unicodedata.normalize("NFC", q)
#q = q.encode('utf-8')

r = requests.post(full_url, data={'text1': q})

soup = BeautifulSoup(r.content, "lxml")
# javascript portion
s = soup.find_all('script')[-1].text
paren_start = 39
paren_end = find_parens(s)[paren_start]

for x, y in [(k['orgStr'], k['candWord']) for k in literal_eval(s[paren_start:paren_end+1])[0]['errInfo']]:
    #print("{}\n\t->".format(x.contents[0].encode('utf-8'))),
    print("{}\n\t->{}\n".format(x, y))
    # print("{}\n\t->".format(x)),
    # #print("{}".format('\n\t-> '.join([x for x in y.contents if type(x) != bs4.element.Tag]).encode('utf-8')))
    # print("{}".format('\n\t-> '.join([x for x in yif type(x) != bs4.element.Tag])))
else:
    print("Done.")
