from urllib.parse import urljoin
from typing import Optional, Dict, Any

import httpx
import pendulum

from pypimod import exceptions as exc
from pypimod import logging, constants

logger = logging.get_logger(__name__)


async def get_project_summary(
    project_name: str, client: Optional[httpx.AsyncClient] = None
) -> Dict[str, str]:
    """Fetches the project's information from the PyPI API."""
    try:
        project_data = await get_project_data_by_name(project_name, client)
    except httpx.exceptions.HTTPError as e:
        raise exc.PyPIAPIError(
            f"Error retriving data from PyPI API: {e.response.status_code}"
        ) from e

    return get_project_summary_from_project_data(project_data)


# TODO: add retries
async def get_project_data_by_name(
    project_name: str, client: Optional[httpx.AsyncClient] = None
) -> Dict[str, Dict[str, Any]]:
    if not client:
        async with httpx.AsyncClient() as client:
            return await _get_pypi_api_project_data(project_name, client)
    else:
        return await _get_pypi_api_project_data(project_name, client)


async def _get_pypi_api_project_data(
    project_name: str, client: httpx.AsyncClient
) -> Dict[str, Dict[str, Any]]:
    response = await client.get(
        urljoin(constants.BASE_PYPI_URL, "/".join(("pypi", project_name, "json")))
    )
    # TODO: handle connection errors
    response.raise_for_status()

    return response.json()


def get_project_summary_from_project_data(
    project_data: Dict[str, Dict[str, Any]]
) -> Dict[str, str]:
    """Returns a summary of project data from the PyPI API for a project."""
    summary = {
        "name": project_data["info"]["name"],
        "summary": project_data["info"]["summary"],
        "version": project_data["info"]["version"],
        "author": project_data["info"]["author"],
        "author_email": project_data["info"]["author_email"],
        "project_urls": project_data["info"]["project_urls"],
    }

    try:
        last_release = _get_last_release_info(project_data)
        summary["last_release_datetime"] = pendulum.parse(last_release["upload_time"])
    except exc.UninstallablePackageError:
        summary["last_release_datetime"] = None

    return summary


def _get_last_release_info(project_data: dict) -> dict:
    """The PyPI API returns the last version number but the releases are
    as dict of version number to release file information, one dict
    per release file.

    This function returns the first release file of the current version
    or raises UninstallablePackageError.
    """
    latest_version = project_data["info"]["version"]
    try:
        return project_data["releases"][latest_version][0]
    except (KeyError, IndexError) as e:
        raise exc.UninstallablePackageError(
            "Latest version of package has no releases"
        ) from e
