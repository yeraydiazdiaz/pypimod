import base64

from typing import Any, Dict
from typing import Optional as Opt
from typing import Tuple

import httpx
import jwt
import pendulum

from gidgethub.abc import GitHubAPI
from gidgethub import httpx as gh_httpx
from gidgethub import BadRequest

from pypimod import logging
from pypimod.config import settings
from pypimod.sources import pypi_api


logger = logging.getLogger(__name__)


async def add_pep541_label(gh: GitHubAPI, issue: dict, label: str) -> None:
    uri = f"repos/{settings.GITHUB_REPO_PATH}/issues/{issue['number']}"
    logger.info("Adding PEP541 label: %s", uri)
    if "labels" in issue:
        labels = [label["name"] for label in issue["labels"]]
        labels.append(label)
    else:
        labels = [label]
    await gh.patch(uri, data={"labels": labels})


async def add_comment_with_project_info(
    gh: GitHubAPI, issue: dict, project_name: str
) -> None:
    try:
        summary = await pypi_api.get_project_summary(project_name)
    except httpx.exceptions.HTTPError as exc:
        if exc.response.status_code == 404:
            text = f"Could not find project `{project_name}` in the PyPI JSON API."
        else:
            raise
    else:
        text = "Here is the relevant information from the PyPI JSON API for project {}:\n".format(
            project_name
        )
        for key, value in summary.items():
            humanized_key = key.replace("_", " ").capitalize()
            text += f"- {humanized_key}: {value} \n"

    uri = f"repos/{settings.GITHUB_REPO_PATH}/issues/{issue['number']}/comments"
    await gh.post(uri, data={"body": text})


class InstallationBasedAppGitHubAPI(gh_httpx.GitHubAPI):
    """Subclass to handle recreating new installation tokens for GitHub apps."""

    MAX_RETRIES = 3

    def __init__(self, client: httpx.AsyncClient, *args: Any, **kwargs: Any) -> None:
        super().__init__(client, *args, **kwargs)
        self.errors = 0
        self._jwt = None
        self._installation_token = None

    async def _make_request(
        self,
        method: str,
        url: str,
        url_vars: Dict,
        data: Any,
        accept: str,
        jwt: Opt[str] = None,
        oauth_token: Opt[str] = None,
    ) -> Tuple[bytes, Opt[str]]:
        # TODO: we're wasting a round trip here because we reuse this instance
        # to bootstrap the refreshing of the token. Feels like this should
        # not be a subclass but a wrapper but will do for now.
        try:
            return await super()._make_request(
                method, url, url_vars, data, accept, jwt=jwt, oauth_token=oauth_token
            )
        except BadRequest:
            self.errors += 1
            if self.errors == self.MAX_RETRIES:
                logger.error(
                    "Regenerating installation tokens failed %d times, giving up",
                    self.MAX_RETRIES,
                )
                raise
            logger.info("Bad request raised, trying again with new installation token")
            await self._refresh_token()
            return await self._make_request(
                method,
                url,
                url_vars,
                data,
                accept,
                jwt=None,
                oauth_token=self._installation_token,
            )

    async def _refresh_token(self):
        logger.debug("Refreshing token")
        self._jwt = encrypt_jwt().decode()
        installation = await self.get_installation()
        self._installation_token = await self.get_installation_access_token(
            installation
        )

    async def get_installation(self):
        async for installation in self.getiter(
            "/app/installations",
            jwt=self._jwt,
            accept="application/vnd.github.machine-man-preview+json",
        ):
            if installation["account"]["login"] == settings.GITHUB_OWNER:
                return installation

        raise ValueError(f"Can't find installation by user {settings.GITHUB_OWNER}")

    async def get_installation_access_token(self, installation):
        access_token_url = f"/app/installations/{installation['id']}/access_tokens"
        response = await self.post(
            access_token_url,
            data=b"",
            jwt=self._jwt,
            accept="application/vnd.github.machine-man-preview+json",
        )
        return response["token"]


def encrypt_jwt(key: bytes = None) -> bytes:
    key = key or base64.b64decode(settings.GITHUB_KEY)
    now = pendulum.now()
    payload = {
        "iat": int(now.timestamp()),  # issued at time
        "exp": int(
            now.add(minutes=5).timestamp()
        ),  # JWT expiration time (10 minute maximum)
        "iss": settings.GITHUB_APP_ID,
    }
    logger.debug(payload)
    return jwt.encode(payload, key, algorithm="RS256")
