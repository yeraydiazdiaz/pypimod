import pytest

from pypimod.sources import bigquery


@pytest.mark.integration
@pytest.mark.asyncio
async def test_downloads_last_n_days_returns_downloads(bq_client):
    bq_client.query.return_value.result.return_value = (("httpx", 100),)
    n_downloads = await bigquery.get_project_downloads_last_n_days("httpx", 1)
    assert n_downloads == 100
    assert bq_client.query.called_once_with("")
