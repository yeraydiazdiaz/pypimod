from copy import deepcopy

import httpx
import pendulum
import pytest

from pypimod.sources import pypi_api
from pypimod import exceptions


@pytest.mark.asyncio
async def test_pypi_api(mocker, pypi_api_httpx):
    mock_response = mocker.Mock(spec=httpx.Response)
    mock_response.json.return_value = pypi_api_httpx
    mock_client = mocker.Mock(spec=httpx.AsyncClient)
    mock_client.get.return_value = mock_response

    summary = await pypi_api.get_project_summary("httpx", client=mock_client)
    assert set(summary.keys()) == {
        "name",
        "summary",
        "version",
        "author",
        "author_email",
        "project_urls",
        "last_release_datetime",
    }
    assert summary["name"] == "httpx"
    assert summary["summary"] == pypi_api_httpx["info"]["summary"]
    assert summary["version"] == pypi_api_httpx["info"]["version"]
    assert summary["author"] == pypi_api_httpx["info"]["author"]
    assert summary["author_email"] == pypi_api_httpx["info"]["author_email"]
    assert summary["project_urls"] == pypi_api_httpx["info"]["project_urls"]
    assert summary["last_release_datetime"] == pendulum.parse("2019-10-10T14:20:49")


@pytest.mark.asyncio
async def test_pypi_api_creates_client_if_none_is_passed(mocker, pypi_api_httpx):
    mock_response = mocker.Mock(spec=httpx.Response)
    mock_response.json.return_value = pypi_api_httpx
    mock_client = mocker.Mock(spec=httpx.AsyncClient)
    mock_client.get.return_value = mock_response
    mock_aenter = mocker.patch.object(
        httpx.AsyncClient, "__aenter__", return_value=mock_client,
    )

    _ = await pypi_api.get_project_summary("httpx")

    assert mock_aenter.called


@pytest.mark.asyncio
async def test_pypi_api_invalid_release(mocker, pypi_api_httpx):
    no_release_response = deepcopy(pypi_api_httpx)
    no_release_response["releases"][no_release_response["info"]["version"]] = []
    mock_response = mocker.Mock(spec=httpx.Response)
    mock_response.json.return_value = no_release_response
    mock_client = mocker.Mock(spec=httpx.AsyncClient)
    mock_client.get.return_value = mock_response

    summary = await pypi_api.get_project_summary("httpx", client=mock_client)

    assert summary["last_release_datetime"] is None


@pytest.mark.asyncio
async def test_pypi_api_http_error(mocker, pypi_api_httpx):
    mock_response = mocker.Mock(spec=httpx.Response, status_code=404)
    mock_response.raise_for_status.side_effect = httpx.exceptions.HTTPError(
        response=mock_response
    )
    mock_client = mocker.Mock(spec=httpx.AsyncClient)
    mock_client.get.return_value = mock_response

    with pytest.raises(exceptions.PyPIAPIError):
        await pypi_api.get_project_summary("httpx", client=mock_client)
