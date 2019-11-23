from urllib.parse import urljoin
import typing

from bs4 import BeautifulSoup
import httpx

from pypimod import exceptions

BASE_PYPI_URL = "https://pypi.org"
PYPI_PROJECT_URL = urljoin(BASE_PYPI_URL, "/project/{}/#history")
PYPI_ADMIN_PROJECT_URL = urljoin(BASE_PYPI_URL, "/admin/projects/{}")


async def get_pypi_urls(project_name: str) -> dict:
    """Returns useful URLs for quick access."""
    project_url = PYPI_PROJECT_URL.format(project_name)
    soup = await fetch_project_page_soup(project_url)
    return {
        "pypi_project_url": project_url,
        "pypi_author_email": get_pypi_author_email_from_body_soup(soup),
        "pypi_maintainers_urls": get_pypi_maintainer_urls_from_body_soup(soup),
        "pypi_admin_project_url": PYPI_ADMIN_PROJECT_URL.format(project_name),
    }


async def fetch_project_page_soup(project_url: str) -> BeautifulSoup:
    async with httpx.AsyncClient() as client:
        response = await client.get(project_url)

    try:
        response.raise_for_status()
    except httpx.exceptions.HTTPError as e:
        raise exceptions.PyPIWebError(
            "Error fetching project URL {}: {}".format(
                project_url, response.status_code
            )
        ) from e

    return BeautifulSoup(response.text, "lxml")


def get_pypi_maintainer_urls_from_body_soup(
    response_soup: BeautifulSoup
) -> typing.List[str]:
    return [
        urljoin(BASE_PYPI_URL, maintainer["href"])
        for maintainer in response_soup.find(
            string="Maintainers"
        ).parent.parent.find_all("a")
    ]


def get_pypi_author_email_from_body_soup(response_soup: BeautifulSoup) -> str:
    author_href = response_soup.find(string="Author:").parent.parent.find("a")["href"]
    _, author_email = author_href.split(":")
    return author_email
