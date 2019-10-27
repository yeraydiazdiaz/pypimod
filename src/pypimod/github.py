from gidgethub.abc import GitHubAPI

from pypimod.config import settings
from pypimod import logging

logger = logging.getLogger(__name__)


async def add_pep541_label(gh: GitHubAPI, issue: dict, label: str) -> None:
    uri = f"repos/{settings.GITHUB_REPO}/issues/{issue['number']}"
    logger.info("Adding PEP541 label: %s", uri)
    # TODO: get labels first and append only if necessary
    await gh.patch(uri, data={"labels": [label]})
