from urllib.parse import urljoin

BASE_PYPI_URL = "https://pypi.org"
PYPI_PROJECT_URL = urljoin(BASE_PYPI_URL, "/project/{name}")
PYPI_RELEASE_URL = urljoin(PYPI_PROJECT_URL, "/{release}")
PYPI_ADMIN_PROJECT_URL = urljoin(BASE_PYPI_URL, "/admin/projects/{name}")
