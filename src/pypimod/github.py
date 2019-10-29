from gidgethub.abc import GitHubAPI

from pypimod.config import settings
from pypimod.sources import pypi_api
from pypimod import logging

logger = logging.getLogger(__name__)


async def add_pep541_label(gh: GitHubAPI, issue: dict, label: str) -> None:
    uri = f"repos/{settings.GITHUB_REPO}/issues/{issue['number']}"
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
    summary = pypi_api.get_project_summary(project_name)
    text = "Here is the relevant information from the PyPI JSON API for project {}:\n".format(
        project_name
    )
    for key, value in summary.items():
        humanized_key = key.replace("_", " ").capitalize()
        text += f"- {humanized_key}: {value} \n"

    uri = f"repos/{settings.GITHUB_REPO}/issues/{issue['number']}/comments"
    await gh.post(uri, data={"body": text})
