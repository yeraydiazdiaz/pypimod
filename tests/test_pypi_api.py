from copy import deepcopy

import httpx
import pendulum
import pytest

from pypimod.sources import pypi_api


@pytest.mark.asyncio
async def test_pypi_api(mocker, pypi_api_httpx):
    mock_response = mocker.Mock(spec=httpx.Response)
    mock_response.json.return_value = pypi_api_httpx
    mock_client = mocker.Mock(spec=httpx.AsyncClient)
    mock_client.get.return_value = mock_response

    summary = await pypi_api.get_project_summary("httpx", client=mock_client)

    assert summary["name"] == "httpx"
    assert summary["summary"] == pypi_api_httpx["info"]["summary"]
    assert summary["version"] == pypi_api_httpx["info"]["version"]
    assert summary["author"] == pypi_api_httpx["info"]["author"]
    assert summary["project_url"] == pypi_api_httpx["info"]["project_url"]
    assert summary["release_url"] == pypi_api_httpx["info"]["release_url"]
    assert summary["last_release_datetime"] == "2019-10-10T14:20:49"
    assert (
        summary["last_release_elapsed_time"]
        == pendulum.parse(summary["last_release_datetime"]).diff_for_humans()
    )


@pytest.mark.asyncio
async def test_pypi_api_invalid_release(mocker, pypi_api_httpx):
    no_release_response = deepcopy(pypi_api_httpx)
    no_release_response["releases"][no_release_response["info"]["version"]] = []
    mock_response = mocker.Mock(spec=httpx.Response)
    mock_response.json.return_value = no_release_response
    mock_client = mocker.Mock(spec=httpx.AsyncClient)
    mock_client.get.return_value = mock_response

    summary = await pypi_api.get_project_summary("httpx", client=mock_client)

    assert summary["name"] == "httpx"
    assert summary["summary"] == pypi_api_httpx["info"]["summary"]
    assert summary["version"] == pypi_api_httpx["info"]["version"]
    assert summary["author"] == pypi_api_httpx["info"]["author"]
    assert summary["project_url"] == pypi_api_httpx["info"]["project_url"]
    assert summary["release_url"] == pypi_api_httpx["info"]["release_url"]
    assert summary["last_release_datetime"].startswith("ERROR")
    assert "last_release_elapsed_time" not in summary
