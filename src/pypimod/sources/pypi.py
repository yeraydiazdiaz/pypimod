import typing

PYPI_PROJECT_URL = "https://pypi.org/project/{}"
PYPI_ADMIN_PROJECT_URL = "https://pypi.org/admin/projects/{}"


def project_urls(project_name: str) -> typing.Dict[str]:
    return [
        PYPI_PROJECT_URL.format(project_name),
        PYPI_ADMIN_PROJECT_URL.format(project_name),
    ]
