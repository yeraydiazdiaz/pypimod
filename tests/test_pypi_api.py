import pendulum
import pytest

from pypimod.sources import pypi_api


@pytest.mark.integration
def test_pypi_api(mocker, pypi_api_httpx):
    mocker.patch(
        "pypimod.sources.pypi_api.get_project_data_by_name", return_value=pypi_api_httpx
    )

    summary = pypi_api.get_project_summary("httpx")

    assert summary["name"] == "httpx"
    assert summary["summary"] == pypi_api_httpx["info"]["summary"]
    assert summary["version"] == pypi_api_httpx["info"]["version"]
    assert summary["author"] == pypi_api_httpx["info"]["author"]
    assert summary["author_email"] == pypi_api_httpx["info"]["author_email"]
    assert summary["project_url"] == pypi_api_httpx["info"]["project_url"]
    assert summary["release_url"] == pypi_api_httpx["info"]["release_url"]
    assert summary["last_release_datetime"] == "2019-10-10T14:20:49"
    assert (
        summary["last_release_elapsed_time"]
        == pendulum.parse(summary["last_release_datetime"]).diff_for_humans()
    )
