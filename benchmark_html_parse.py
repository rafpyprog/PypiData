import json
import xml.etree.cElementTree as ET

import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
import timeit


HTML = requests.get('https://pypi.python.org/simple/').text

def find_all_packages_ET():
    #HTML = requests.get('https://pypi.python.org/simple/').text
    body = ET.fromstring(HTML).find('body')
    packages = [link.text for link in body.findall('a')]
    return packages


def find_all_packages_lxml():
    #HTML = requests.get('https://pypi.python.org/simple/').text
    tree = fromstring(HTML)
    packages = [link.text for link in tree.body.findall('a')]
    return packages


def find_all_packages(parser):
    #HTML = requests.get('https://pypi.python.org/simple/').content
    soup = BeautifulSoup(HTML, parser)
    packages = [link.text for link in soup.findAll('a')]
    return packages


if __name__ == '__main__':
    n = 10
    print('ET:', timeit.timeit("find_all_packages_ET()", number=n,
          setup="from __main__ import find_all_packages_ET"))
    print('lxml:', timeit.timeit("find_all_packages_lxml()", number=n,
          setup="from __main__ import find_all_packages_lxml"))
    print('BS4-lxml:', timeit.timeit("find_all_packages('lxml')", number=n,
          setup="from __main__ import find_all_packages"))
    print('BS4-html.parser:', timeit.timeit("find_all_packages('html.parser')",
          number=n, setup="from __main__ import find_all_packages"))
