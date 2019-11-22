from typing import Optional
from urllib.parse import urljoin

import httpx
import pendulum

from pypimod import exceptions as exc

PYPI_BASE_URL = "https://pypi.org"


async def get_project_summary(
    project_name: str, client: Optional[httpx.AsyncClient] = None
):
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
) -> dict:
    if not client:
        async with httpx.AsyncClient() as client:
            return await _get_pypi_api_project_data(project_name, client)
    else:
        return await _get_pypi_api_project_data(project_name, client)


async def _get_pypi_api_project_data(
    project_name: str, client: httpx.AsyncClient
) -> dict:
    response = await client.get(
        urljoin(PYPI_BASE_URL, "/".join(("pypi", project_name, "json")))
    )
    # TODO: handle connection errors
    response.raise_for_status()

    return response.json()


def get_project_summary_from_project_data(project_data: dict) -> dict:
    """Returns a summary of project data from the PyPI API for a project."""
    summary = {
        "name": project_data["info"]["name"],
        "summary": project_data["info"]["summary"],
        "version": project_data["info"]["version"],
        "author": project_data["info"]["author"],
        "project_url": project_data["info"]["project_url"],
        "release_url": project_data["info"]["release_url"],
    }

    try:
        last_release = _get_last_release_info(project_data)
        summary["last_release_datetime"] = last_release["upload_time"]
        summary["last_release_elapsed_time"] = pendulum.parse(
            summary["last_release_datetime"]
        ).diff_for_humans()
    except exc.UninstallablePackageError as e:
        summary["last_release_datetime"] = f"ERROR: {e}"

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
