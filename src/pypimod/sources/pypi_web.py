from urllib.parse import urljoin
from typing import List, Tuple

from bs4 import BeautifulSoup
import httpx

from pypimod import exceptions, constants


async def get_pypi_urls(project_name: str) -> List[str]:
    """Fetch the projects PyPI page and return author email and maintainer URLs."""
    project_url = constants.PYPI_PROJECT_URL.format(name=project_name)
    soup = await fetch_project_page_soup(project_url)
    return get_pypi_maintainer_urls_from_body_soup(soup)


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


def get_pypi_maintainer_urls_from_body_soup(response_soup: BeautifulSoup) -> List[str]:
    return [
        urljoin(constants.BASE_PYPI_URL, maintainer["href"])
        for maintainer in response_soup.find(
            string="Maintainers"
        ).parent.parent.find_all("a")
    ]


def get_pypi_author_email_from_body_soup(response_soup: BeautifulSoup) -> str:
    author = response_soup.find(string="Author:")
    if author is None:
        return ""

    author_href = author.parent.parent.find("a")["href"]
    _, author_email = author_href.split(":")
    return author_email
