import json
import os
import xml.etree.cElementTree as ET

from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError


class Pypi():
    def __init__(self):
        self.index = 'https://pypi.python.org/simple/'
        self.jsonAPI = 'https://pypi.python.org/pypi/{}/json'

    def find_all_packages(self):
        HTML = requests.get('https://pypi.python.org/simple/').text
        body = ET.fromstring(HTML).find('body')
        packages = [link.text for link in body.findall('a')]
        return packages

    def get_package_data(self, package_name):
        response = requests.get(self.jsonAPI.format(package_name))
        try:
            response.raise_for_status()
        except HTTPError as e:
            print(str(e))
            return None
        data = json.loads(response.content)
        return data


def parse_package_data(data):
    INFO_DATA = ('name', 'license', 'summary', 'home_page', 'author',
                 'author_email', 'maintainer', 'keywords',
                 'platform', 'version')

    releases = data.pop('releases', None)
    urls = data.pop('urls', None)

    wanted = {}
    data_fields = list(data['info'].keys())
    for field in data_fields:
        if field in INFO_DATA:
            wanted[field] = data['info'].pop(field, None)

    RELEASE_DATA = ('filename', 'size', 'upload_time')
    LAST_RELEASE = releases[wanted['version']]
    for release_file in LAST_RELEASE:
        if release_file['filename'].endswith('tar.gz'):
            for field in RELEASE_DATA:
                wanted[field] = release_file.pop(field, None)
            break
    else:  # Some packages dont have tar.gz, Try to get the last file from list
        if LAST_RELEASE == []:
            for field in RELEASE_DATA:
                wanted[field] = None
        else:
            LAST_FILE = -1
            release_file = LAST_RELEASE[LAST_FILE]
            for field in RELEASE_DATA:
                wanted[field] = release_file.pop(field, None)

    # TO DO CLASSIFIERS

    return wanted
