import copy
import os
import xml.etree.cElementTree as ET

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

    def parse_version_release(self, version):
        ''' Biggest release file '''
        FIELDS = ('filename', 'size', 'upload_time')
        release = self.releases.pop(version, None)

        if release != []:
            max_size = max(map(lambda x: x['size'], release))
            release_data = next(filter(lambda x: x['size'] == max_file, release))
            DESIRED_FIELDS = lambda x: x[0] in FIELDS
            return dict(filter(DESIRED_FIELDS, r.items()))
        else:
            return None


p = Pypi()
data = p.get_package_data("requests")
imagesoup = Package(data)
v = imagesoup.version
r = imagesoup.parse_version_release(v)
r


for i in filter(lambda x: x in ('size', 'upload_time'), r):
    print(i)

list(filter(lambda x: [max(i['size']) for i in x], r))


max_file = max(map(lambda x: x['size'], r))




imagesoup.version
data['info']['version']
data['info']['name']
