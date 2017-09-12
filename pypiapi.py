import copy
import os
import xml.etree.cElementTree as ET

from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
import ujson


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
        data = ujson.loads(response.content)
        return data


class Package():
    def __init__(self, data):
        self.data = copy.deepcopy(data)
        self.parse_info()

    @property
    def info(self):
        return self.data['info']

    @property
    def releases(self):
        return self.data['releases']

    @property
    def urls(self):
        return self.data['urls']

    def parse_info(self):
        FIELDS = ('name', 'license', 'summary', 'home_page', 'author',
                  'author_email', 'maintainer', 'keywords',
                  'platform', 'version')
        info_data = {}

        for field in FIELDS:
            field_value = self.info.pop(field, None)
            info_data[field] = field_value
            setattr(self, field, field_value)
        return info_data





def parse_package_info(package_data):
    data = {}
    info = package_data['info']

    data['name'] = info.pop('name', None)
    data['license'] = info.pop('license', None)
    data['summary'] = info.pop('summary', None)
    data['home_page'] = info.pop('home_page', None)
    data['author'] = info.pop('author', None)
    data['author_email'] = info.pop('author_email', None)
    data['maintainer'] = info.pop('maintainer', None)
    data['keywords'] = info.pop('keywords', None)
    data['platform'] = info.pop('platform', None)
    data['version'] = info.pop('version', None)

    release = package_data['releases'][data['version']]
    if release != []:
        for field in ('filename', 'size', 'upload_time'):
            data[field] = release.pop(field, None)
    else:


    return data



def parse_package_data(package_data):
    data = package_data.deepcopy()
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



p = Pypi()
data = p.get_package_data("imagesoup")
imagesoup = Package(data)
imagesoup.version
data['info']['version']
data['info']['name']
