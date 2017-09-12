from datetime import date, timedelta
from bigquery import get_client


def login_client(project_id, service_account, json_key_file):
    '''
       project_id: BigQuery project id as listed in the Google Developers
                   Console.
       service_account: Service account email address as listed in the Google
                        Developers Console.
       json_key_file: JSON key provided by Google.
    '''

    service_account = service_account
    client = get_client(json_key_file=json_key_file, readonly=True)
    return client


def last_n_days(n, packages):
    actual_date = date.today().strftime('%Y-%m-%d')
    past_date = (date.today() - timedelta(days=n)).strftime('%Y-%m-%d')
    #packages = python_packages()

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
