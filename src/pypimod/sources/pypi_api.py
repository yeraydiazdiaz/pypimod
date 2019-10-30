import asyncio
from typing import Optional
from urllib.parse import urljoin

import httpx
import pendulum

PYPI_BASE_URL = "https://pypi.org"


def get_project_summary(project_name: str):
    # TODO: add an async version? Feels wrong somehow...
    project_data = asyncio.run(get_project_data_by_name(project_name))
    return get_project_summary_from_project_data(project_data)


def get_project_summary_from_project_data(project_data: dict) -> dict:
    """Returns a summary of project data from the PyPI API for a project."""
    summary = {
        "name": project_data["info"]["name"],
        "summary": project_data["info"]["summary"],
        "version": project_data["info"]["version"],
        "author": project_data["info"]["author"],
        "author_email": project_data["info"]["author_email"],
        "project_url": project_data["info"]["project_url"],
        "release_url": project_data["info"]["release_url"],
    }
    summary["last_release_datetime"] = project_data["releases"][summary["version"]][0][
        "upload_time"
    ]
    summary["last_release_elapsed_time"] = (
        pendulum.now() - pendulum.parse(summary["last_release_datetime"])
    ).in_words()
    return summary


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
