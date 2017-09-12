from datetime import datetime, timedelta
import requests

from bigqueryapi import login_client
from pypiapi import Pypi, parse_package_data


if __name__ == '__main__':
    SERVICE_ACCOUNT = 'rafael-alves-ribeiro@badgepypi.iam.gserviceaccount.com'
    JSON_KEY = 'key.json'
    PROJECT_ID = 'badgepypi'

    pypi = Pypi()
    packages = pypi.find_all_packages()

    for package in

    bq_client = login_client(PROJECT_ID, SERVICE_ACCOUNT, JSON_KEY)

    os.remove('packagedata.json')
    db = TinyDB('packagedata.json')

    for n, package in enumerate(test):
        print(n + 1, package)
        data = get_package_data(package)
        if data:
            package_data = filter_package_data(data)
            db.insert(package_data)
