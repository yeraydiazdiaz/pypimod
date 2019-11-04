from unittest.mock import AsyncMock, Mock

import pytest
import httpx

from pypimod import github


def client_with_response(
    status_code: int = 200, headers: dict = None, body: bytes = b"[]"
) -> httpx.AsyncClient:
    mock_response = Mock(spec=httpx.Response)
    mock_response.status_code = status_code
    mock_response.headers = headers or {"Content-type": "application/json"}
    mock_response.read = AsyncMock(return_value=body)
    mock_client = Mock(spec=httpx.AsyncClient)
    mock_client.request = AsyncMock(return_value=mock_response)
    return mock_client


class TestInstallationBasedAppGitHubApi:
    @pytest.mark.asyncio
    async def test_installation_token_is_not_generated_if_no_error(self, mocker):
        mock_client = client_with_response()
        gh = github.InstallationBasedAppGitHubAPI(mock_client, "pypimod")

        await gh.getitem("repo/yeraydiazdiaz/pypimod/issues/1")

        assert gh.attempts == 1
        assert gh._jwt is gh._installation_token is None

    @pytest.mark.wip
    @pytest.mark.asyncio
    async def test_installation_token_is_generated_if_bad_request(self, mocker):
        mock_client = client_with_response(status_code=401)
        gh = github.InstallationBasedAppGitHubAPI(mock_client, "pypimod")

        await gh.getitem("repo/yeraydiazdiaz/pypimod/issues/1")

        assert gh.attempts == 1
