import asyncio

import aiohttp

from gidgethub import aiohttp as gh_aiohttp
from gidgethub import routing, sansio
from quart import Quart, request

from pypimod.config import settings
from pypimod import routing as pypimod_routing, logging

app = Quart(__name__)

router = routing.Router(pypimod_routing.router)

logger = logging.getLogger(__name__)


@app.errorhandler(500)
def error_handler(exc):
    logger.exception(exc)
    return "Error", 500


@app.route("/", methods=["POST"])
async def main():
    body = await request.get_data()
    event = sansio.Event.from_http(request.headers, body, secret=settings.GITHUB_SECRET)
    if event.event != "ping":
        async with aiohttp.ClientSession() as session:
            # TODO: add caching
            gh = gh_aiohttp.GitHubAPI(
                session, "yeraydiazdiaz/pypimod", oauth_token=settings.GITHUB_AUTH
            )
            await asyncio.sleep(1)  # give GitHub time to reach consistency
            await router.dispatch(event, gh, session=session)

    return ""


if __name__ == "__main__":  # pragma: nocover
    app.run(host=settings.SERVER_HOST, port=settings.SERVER_PORT, debug=False)
