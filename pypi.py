from bs4 import BeautifulSoup
import requests


def get_all_packages():
    pypi_index = 'https://pypi.python.org/simple/'
    response = requests.get(pypi_index)
    soup = BeautifulSoup(response.content, 'html.parser')
    names = [link.text for link in soup.findAll('a')]
    return names


def get_package_data(package_name):
    pypi_API = f'https://pypi.python.org/pypi/{package_name}/json'
    response = requests.get(pypi_API)
    return response.content


packages = get_all_packages()

for n, package in enumerate(packages):
    print(n)
    data = get_package_data(package)
