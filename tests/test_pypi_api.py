from unittest.mock import Mock

import httpx
import pendulum
import pytest

from pypimod.sources import pypi_api


@pytest.mark.asyncio
@pytest.mark.integration
async def test_pypi_api(mocker, pypi_api_httpx):
    mock_response = Mock(spec=httpx.Response)
    mock_response.json.return_value = pypi_api_httpx
    mock_client = Mock(spec=httpx.AsyncClient)
    mock_client.get.return_value = mock_response

    summary = await pypi_api.get_project_summary("httpx", client=mock_client)

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
