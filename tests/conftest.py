import json

from pathlib import Path
from unittest.mock import AsyncMock

import pytest
import trustme

from gidgethub.abc import GitHubAPI
from google.cloud import bigquery

from pypimod import server


def _read_asset(name):
    path = Path(__file__).parent / "assets" / name
    with open(path, "r") as fd:
        return fd.read()


@pytest.fixture
def pypi_api_httpx():
    return json.loads(_read_asset("httpx.json"))


@pytest.fixture
def bq_client(mocker):
    mock_bq_client = mocker.Mock(spec=bigquery.Client)
    mocker.patch(
        "pypimod.sources.bigquery.get_bigquery_client", return_value=mock_bq_client
    )
    return mock_bq_client


@pytest.fixture
def app():
    return server.app


@pytest.fixture
def gh(mocker):
    """A mock gidgethub.GitHubAPI."""
    mock = AsyncMock(spec=GitHubAPI)
    mocker.patch("pypimod.github.InstallationBasedAppGitHubAPI", return_value=mock)
    return mock


@pytest.fixture(scope="session")
def cert_authority():
    return trustme.CA()


@pytest.fixture(scope="session")
def ca_cert_pem(cert_authority):
    return cert_authority.private_key_pem.bytes()
