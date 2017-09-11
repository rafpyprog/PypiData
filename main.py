from datetime import datetime, timedelta

import requests
from bigquery import get_client






def login_bigquery():
    # BigQuery project id as listed in the Google Developers Console.
    project_id = 'badgepypi'
    # Service account email address as listed in the Google Developers Console.
    service_account = 'rafael-alves-ribeiro@badgepypi.iam.gserviceaccount.com'
    # JSON key provided by Google
    json_key = 'key.json'
    client = get_client(json_key_file=json_key, readonly=True)
    return client


def python_packages():
    names = ['ansible', 'beautifulsoup4', 'celery', 'django', 'flask',
             'imagesoup', 'ipython', 'keras', 'kivy', 'luigi', 'numpy',
             'nltk', 'matplotlib', 'pandas', 'pillow', 'requests',
             'scipy', 'scikit-learn', 'scrapy', 'selenium', 'tornado']

    string = ', '.join('"' + i + '"' for i in names)
    return string


def get_all_packages_name():
    sql_query('SELECT DISTINCT file.project FROM TABLE_DATE_RANGE[]')


def last_n_days(n):
    actual_date = date.today().strftime('%Y-%m-%d')
    past_date = (date.today() - timedelta(days=n)).strftime('%Y-%m-%d')
    packages = python_packages()

    sql_query = f'''SELECT
                       file.project,
                       COUNT(*) as download_count
                   FROM
                       TABLE_DATE_RANGE( [the-psf:pypi.downloads], TIMESTAMP("{past_date}"), TIMESTAMP("{actual_date}") )
                   WHERE
                       file.project IN ({packages})
                   GROUP BY
                       file.project
                   ORDER BY
                       download_count
                 '''
    return sql_query



client = login_bigquery()
# Submit an async query.
job_id, _results = client.query(last_n_days(n=365))

# Check if the query has finished running.
complete, row_count = client.check_job(job_id)

# Retrieve the results.
results = client.get_query_rows(job_id)

results





#date = datetime.fromtimestamp(results[0]['timestamp'])
