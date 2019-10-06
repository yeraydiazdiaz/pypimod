import logging

import click

from pypimod.sources import pypi_api, bigquery


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
    # Generate PyPI URL and check if it returns 200 and warn otherwise
    # Generate PyPI JSON API URLs, retrieve and gather information from them
    summary = pypi_api.get_project_summary(project_name)
    if stats:
        summary[
            f"downloads_last_{days}_days"
        ] = bigquery.get_project_downloads_last_n_days(project_name, days)
    for k, v in summary.items():
        click.echo(f"{k}: {v}")


@cli.command()
def check(project_name: str):
    # Download release to temporary directory and perform analysis for
    # empty packages
    raise NotImplementedError
