import json

import requests
import ujson

from pypiapi import Pypi


def get_json_data():
    packages = ['requests', 'numpy', 'imagesoup', 'pandas', 'keras', 'ipython',
                'beautifulsoup4', 'selenium', 'pillow', 'matplotlib']
    jsonAPI = 'https://pypi.python.org/pypi/{}/json'
    data = []
    for p in packages:
        response = requests.get(jsonAPI.format(p))
        data.append(response.content)
    return data


def test_load_json(data, lib):
    for i in data:
        j = lib.loads(i)


if __name__ == '__main__':
    pypi = Pypi()
    data = get_json_data()
    %timeit test_load_json(data * 10, lib=json)
    %timeit test_load_json(data * 10, lib=ujson)


    jsonAPI = 'https://pypi.python.org/pypi/requests/json'
    r = requests.get(jsonAPI)

    %timeit -r 50 ujson.loads(r.content)
    %timeit -r 50 ujson.loads(r.text)
