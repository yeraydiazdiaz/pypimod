from gidgethub.abc import GitHubAPI

from pypimod.config import settings


async def add_pep541_label(gh: GitHubAPI, issue: dict, label: str) -> None:
    uri = f"repos/{settings.GITHUB_REPO}/issues/{issue['number']}"
    print(f"Adding PEP541 label: {uri}")
    # TODO: get labels first and append only if necessary
    await gh.patch(uri, data={"labels": [label]})
