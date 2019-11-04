import base64
import json
import typing

from unittest.mock import AsyncMock, Mock

import httpx
import pytest

from pypimod import github
from pypimod.config import settings


class MockResponse(typing.NamedTuple):
    status_code: int = 200
    headers: dict = {"content-type": "application/json"}
    body: bytes = b"[]"

    def to_response(self):
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = self.status_code
        mock_response.headers = self.headers
        mock_response.read = AsyncMock(return_value=self.body)
        return mock_response


def client_with_responses(responses: typing.List[MockResponse]) -> httpx.AsyncClient:
    responses = [response.to_response() for response in responses]
    mock_client = Mock(spec=httpx.AsyncClient, name="mocked_httpx_client")
    mock_client.request = AsyncMock(side_effect=responses)
    return mock_client


class TestInstallationBasedAppGitHubApi:
    @pytest.mark.asyncio
    async def test_installation_token_is_not_generated_if_no_error(self, mocker):
        mock_client = client_with_responses([MockResponse()])
        gh = github.InstallationBasedAppGitHubAPI(mock_client, "pypimod")

        await gh.getitem("repo/yeraydiazdiaz/pypimod/issues/1")

        assert gh.errors == 0
        assert gh._jwt is gh._installation_token is None

    @pytest.mark.asyncio
    async def test_installation_token_is_generated_if_bad_request(
        self, mocker, ca_cert_pem
    ):
        mocker.patch.object(settings, "GITHUB_KEY", base64.b64encode(ca_cert_pem))
        responses = [
            MockResponse(status_code=401),
            MockResponse(
                body=json.dumps(
                    [{"account": dict(login=settings.GITHUB_OWNER), "id": 1234}]
                ).encode()
            ),
            MockResponse(body=b'{"token": "some_token"}'),
            MockResponse(),
        ]
        mock_client = client_with_responses(responses)
        gh = github.InstallationBasedAppGitHubAPI(mock_client, "pypimod")

        await gh.getitem("repo/yeraydiazdiaz/pypimod/issues/1")

        assert gh._installation_token is not None
        assert gh.errors == 1
