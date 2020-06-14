import asyncio

import click

from pypimod import exceptions
from pypimod.sources import pypi_api, bigquery, pypi_web


@click.group()
def cli():
    pass


@cli.command()
@click.argument("project_name")
@click.option("--stats/--no-stats", default=False, show_default=True)
@click.option("-d", "--days", type=int, default=31, show_default=True)
def info(project_name: str, stats: bool = False, days: int = 31):
    """Retrieve project data from PyPI and print a summary."""
    try:
        summary = asyncio.run(get_project_info(project_name))
        if stats:
            summary[
                f"downloads_last_{days}_days"
            ] = bigquery.get_project_downloads_last_n_days(project_name, days)
        for k, v in summary.items():
            click.echo(f"{k}: {v}")
    except exceptions.PyPIAPIError as e:
        click.echo(e, err=True)


async def get_project_info(project_name: str) -> dict:
    results = await asyncio.gather(
        pypi_api.get_project_summary(project_name),
        pypi_web.get_pypi_urls(project_name),
        return_exceptions=True,
    )
    project_info: dict = {}
    for result in results:
        if isinstance(result, Exception):
            click.echo(result, err=True)
        project_info.update(result)

    return project_info
