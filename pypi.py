import json
import os

from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
from tinydb import TinyDB, Query



def get_all_packages():
    pypi_index = 'https://pypi.python.org/simple/'
    response = requests.get(pypi_index)
    soup = BeautifulSoup(response.content, 'html.parser')
    names = [link.text for link in soup.findAll('a')]
    return names


def get_package_data(package_name):
    pypi_API = f'https://pypi.python.org/pypi/{package_name}/json'
    response = requests.get(pypi_API)
    try:
        response.raise_for_status()
    except HTTPError as e:
        print(str(e))
        return None
    data = json.loads(response.content)
    return data


def filter_package_data(data):
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

    #TO DO CLASSIFIERS

    return wanted


pypi_packages = get_all_packages()
print(f'Found {len(pypi_packages)} packages.')

test = pypi_packages[0:1000]

os.remove('packagedata.json')
db = TinyDB('packagedata.json')

for n, package in enumerate(test):
    print(n + 1, package)
    data = get_package_data(package)
    if data:
        package_data = filter_package_data(data)
        db.insert(package_data)
