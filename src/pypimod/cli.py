import logging

import click
import pendulum
import jwt

from pypimod import server
from pypimod.sources import pypi_api, bigquery
from pypimod.config import settings


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s %(thread)s] %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("project_name")
@click.option("--stats/--no-stats", default=False, show_default=True)
@click.option("-d", "--days", type=int, default=31, show_default=True)
def info(project_name: str, stats: bool = False, days: int = 31):
    """Retrieve project data from PyPI and print a summary."""
    summary = pypi_api.get_project_summary(project_name)
    if stats:
        summary[
            f"downloads_last_{days}_days"
        ] = bigquery.get_project_downloads_last_n_days(project_name, days)
    for k, v in summary.items():
        click.echo(f"{k}: {v}")


@cli.command()
def check(project_name: str):
    """Download release to temporary directory and perform analysis."""
    raise NotImplementedError


@cli.command()
@click.option("-h", "--host", type=str)
@click.option("-p", "--port", type=int)
@click.option("--debug/--no-debug", default=False, show_default=True)
def serve(host: str = None, port: int = None, debug: bool = False) -> None:
    """Start the GitHub bot server."""
    host = host or settings.SERVER_HOST
    port = port or settings.SERVER_PORT
    server.app.run(host, port=port, debug=debug)


@cli.command()
@click.argument("key")
def generate_jwt(key: str) -> None:
    # Private key contents
    with open(key) as fd:
        private_pem = fd.read()
    now = pendulum.now()
    payload = {
        # issued at time
        "iat": int(now.timestamp()),
        # JWT expiration time (10 minute maximum)
        "exp": int(now.add(minutes=10).timestamp()),  # rotate?
        # GitHub App's identifier
        "iss": settings.GITHUB_APP_ID,
    }
    encoded = jwt.encode(payload, private_pem, algorithm="RS256")
    click.echo(encoded)
