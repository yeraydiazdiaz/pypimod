import asyncio
from concurrent import futures
from collections import OrderedDict
from typing import Dict

from google.cloud import bigquery
import pendulum

from pypimod.config import settings
from pypimod.utils import cache_results

PROJECT_DOWNLOADS_BETWEEN_DATES = """
SELECT project, SUM(downloads)
FROM (
    SELECT file.project as project,
       DATE(timestamp) as date,
       details.installer.name as installer_name,
       COUNT(*) as downloads
    FROM `{table}`
    WHERE _TABLE_SUFFIX BETWEEN
        '{start_date}' AND '{end_date}'
    GROUP BY file.project, date, installer_name
)
WHERE project = '{project_name}'
  AND installer_name = 'pip'
GROUP BY project
"""


async def get_project_downloads_last_n_days(project_name: str, n_days: int) -> int:
    loop = asyncio.get_event_loop()
    with futures.ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(
            executor, get_project_downloads_last_n_days_sync, project_name, n_days
        )


def get_bigquery_client() -> bigquery.Client:
    credentials = settings.GC_CREDENTIALS
    project = settings.GC_PROJECT
    # Service account requires the BigQuery Job User IAM role
    return bigquery.Client.from_service_account_json(credentials, project=project)


def get_project_downloads_last_n_days_sync(project_name: str, n_days: int) -> int:
    end_date = pendulum.today().subtract(days=1)
    start_date = end_date.subtract(days=n_days)

    return get_project_downloads_in_between_dates(project_name, start_date, end_date)


@cache_results
def get_project_downloads_in_between_dates(
    project_name: str, start_date: pendulum.DateTime, end_date: pendulum.DateTime
) -> int:
    query_string = PROJECT_DOWNLOADS_BETWEEN_DATES.format(
        project_name=project_name,
        start_date=start_date.format("YYYYMMDD"),
        end_date=end_date.format("YYYYMMDD"),
        table=settings.BQ_PYPI_DOWNLOADS_TABLE,
    )
    result = _do_downloads_query(query_string)
    if not result:
        return -1
    return result[project_name]


def _do_downloads_query(query_string: str) -> Dict[str, int]:
    bq = get_bigquery_client()
    query = bq.query(query_string)
    results: OrderedDict = OrderedDict()
    for row in query.result():
        results[row[0]] = row[1]
    if not results:
        return {}
    return results
