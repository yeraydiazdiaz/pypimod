import re

import gidgethub.routing
from gidgethub.sansio import Event
from gidgethub.abc import GitHubAPI

from pypimod import github

router = gidgethub.routing.Router()


PEP541_RE = re.compile(r".*PEP\W?541.*", flags=re.I)
PEP541_LABEL = "PEP 541"
PROJECT_NAME_RE = re.compile(r".*[`\"'](\w+)[`\"'].*", flags=re.I)


@router.register("issues", action="opened")
@router.register("issues", action="edited")
async def pep541_issue_opened(event: Event, gh: GitHubAPI, *args, **kwargs) -> None:
    issue = event.data["issue"]
    if not PEP541_RE.match(issue["title"]):
        return

    if not is_issue_labeled_with_pep541(issue):
        await github.add_pep541_label(gh, issue, PEP541_LABEL)

    project_name_match = PROJECT_NAME_RE.match(issue["title"])
    if project_name_match:
        await github.add_comment_with_project_info(
            gh, issue, project_name_match.group(1)
        )


def is_issue_labeled_with_pep541(issue: dict) -> bool:
    if any(label["name"] == PEP541_LABEL for label in issue.get("labels", [])):
        return True

    return False
