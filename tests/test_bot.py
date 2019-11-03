from unittest.mock import AsyncMock

import pytest


@pytest.mark.asyncio
async def test_server_returns_empty_200_for_ping_event(mocker, app) -> None:
    client = app.test_client()
    mocker.patch(
        "pypimod.server.sansio.Event.from_http", return_value=mocker.Mock(event="ping")
    )

    response = await client.post("/")

    assert response.status_code == 200
    assert await response.get_data() == b""


@pytest.mark.asyncio
async def test_server_adds_pep541_label_on_issue_opened(mocker, app, gh) -> None:
    client = app.test_client()
    data = {
        "issue": {"title": "PEP 541: transfer of project foobar", "number": 1234},
        "action": "opened",
    }
    mocker.patch(
        "pypimod.server.sansio.Event.from_http",
        return_value=mocker.Mock(event="issues", data=data),
    )

    response = await client.post("/")

    assert response.status_code == 200
    assert gh.patch.await_count == 1
    assert gh.patch.await_args_list[0][1]["data"]["labels"] == ["PEP 541"]


@pytest.mark.asyncio
async def test_server_does_not_add_pep541_label_on_issue_already_labeled(
    mocker, app, gh
) -> None:
    client = app.test_client()
    data = {
        "issue": {
            "title": "PEP 541: transfer of project foobar",
            "number": 1234,
            "labels": [{"name": "PEP 541"}],
        },
        "action": "opened",
    }
    mocker.patch(
        "pypimod.server.sansio.Event.from_http",
        return_value=mocker.Mock(event="issues", data=data),
    )

    response = await client.post("/")

    assert response.status_code == 200
    assert gh.patch.await_count == 0


@pytest.mark.asyncio
async def test_server_does_not_overwrite_existing_labels(mocker, app, gh) -> None:
    client = app.test_client()
    data = {
        "issue": {
            "title": "PEP 541: transfer of project foobar",
            "number": 1234,
            "labels": [{"name": "documentation"}],
        },
        "action": "opened",
    }
    mocker.patch(
        "pypimod.server.sansio.Event.from_http",
        return_value=mocker.Mock(event="issues", data=data),
    )

    response = await client.post("/")

    assert response.status_code == 200
    assert gh.patch.await_count == 1
    assert gh.patch.await_args_list[0][1]["data"]["labels"] == [
        "documentation",
        "PEP 541",
    ]


@pytest.mark.asyncio
async def test_server_comments_on_issue_with_pypi_api_stats(mocker, app, gh) -> None:
    mocker.patch(
        "pypimod.github.pypi_api.get_project_summary",
        return_value={"project_name": "lunr"},
    )
    client = app.test_client()
    data = {
        "issue": {"title": "PEP 541: transfer of project `foobar`", "number": 1234},
        "action": "opened",
        "labels": [{"name": "PEP 541"}],
    }
    mocker.patch(
        "pypimod.server.sansio.Event.from_http",
        return_value=mocker.Mock(event="issues", data=data),
    )

    response = await client.post("/")

    assert response.status_code == 200
    assert gh.post.await_count == 1
    assert "lunr" in gh.post.await_args[1]["data"]["body"]
