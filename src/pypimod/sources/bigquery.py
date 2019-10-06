from collections import OrderedDict
from typing import Dict

from google.cloud import bigquery

from pypimod.config import settings
from pypimod.utils import cache_results

PROJECT_DOWNLOADS_LAST_N_DAYS = """
SELECT project, SUM(downloads)
FROM (
    SELECT file.project as project,
       DATE(timestamp) as date,
       details.installer.name as installer_name,
       COUNT(*) as downloads
    FROM `{table}`
    WHERE _TABLE_SUFFIX BETWEEN
        FORMAT_DATE(
            "%Y%m%d",
            DATE_ADD(CURRENT_DATE(), INTERVAL -{n_days} day))
        AND
        FORMAT_DATE(
            "%Y%m%d",
            DATE_ADD(CURRENT_DATE(), INTERVAL -1 day))
    GROUP BY file.project, date, installer_name
)
WHERE project = '{project_name}'
  AND installer_name = 'pip'
GROUP BY project
"""


def get_bigquery_client() -> bigquery.Client:
    credentials = settings.GC_CREDENTIALS
    project = settings.GC_PROJECT
    # Service account requires the BigQuery Job User IAM role
    return bigquery.Client.from_service_account_json(credentials, project=project)


@cache_results
def get_project_downloads_last_n_days(project_name: str, n_days: int) -> int:
    query_string = PROJECT_DOWNLOADS_LAST_N_DAYS.format(
        project_name=project_name, n_days=n_days, table=settings.BQ_PYPI_DOWNLOADS_TABLE
    )
    return _do_downloads_query(query_string)[project_name]


def _do_downloads_query(query_string: str) -> Dict[str, int]:
    bq = get_bigquery_client()
    query = bq.query(query_string)
    results: OrderedDict = OrderedDict()
    for row in query.result():
        results[row[0]] = row[1]
    return results
