import asyncio

from datetime import datetime
from enum import Enum, auto
from typing import List, Optional, Dict

import attr

from pypimod import sources, logging, constants, exceptions

logger = logging.get_logger(__name__)


class ProjectStatus(Enum):
    ACTIVE = auto()
    INVALID = auto()
    ABANDONED = auto()


@attr.s(auto_attribs=True, slots=True)
class ProjectData:
    name: str
    summary: str
    version: str
    author: str
    author_email: str
    project_urls: Dict[str, str]
    last_release_datetime: Optional[datetime] = None
    maintainers_urls: List[str] = []
    downloads_days: int = 0
    downloads_count: int = -1

    @property
    def is_valid(self):
        return self.last_release_datetime is not None

    @property
    def project_url(self):
        return constants.PYPI_PROJECT_URL.format(self.name)

    @property
    def release_url(self):
        return constants.PYPI_RELEASE_URL.format(self.name, self.last_release)


async def get_project_data(project_name: str, stats_days: int = 0) -> ProjectData:
    """Retrieves project data for a project name from different sources.

    Download stats will not be fetched by default, supply a positive integer
    to retrieve download stats for the corresponding number of days.
    """
    tasks = [
        sources.pypi_api.get_project_summary(project_name),
        sources.pypi_web.get_pypi_urls(project_name),
    ]
    if stats_days < 0:
        raise exceptions.InvalidArgument("Stats days must be 0 or a positive integer")
    elif stats_days > 0:
        tasks.append(
            sources.bigquery.get_project_downloads_last_n_days(project_name, stats_days)
        )

    results = await asyncio.gather(*tasks, return_exceptions=True)

    project_data, *rest = results
    if isinstance(project_data, Exception):
        raise project_data

    project_data = ProjectData(**project_data)
    web_result = rest[0]
    if isinstance(web_result, Exception):
        logger.exception(
            "Error retrieving additional information for project %s",
            project_name,
            exc_info=web_result,
        )
    else:
        project_data.maintainers_urls = web_result

    if stats_days > 0:
        bq_result = rest[-1]
        if isinstance(bq_result, Exception):
            logger.exception(
                "Error retrieving stats information for project %s", project_name
            )
        else:
            project_data.downloads_days = stats_days
            project_data.downloads_count = bq_result

    return project_data
