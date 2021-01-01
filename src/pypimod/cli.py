import asyncio

import attr
import click

from pypimod import exceptions
from pypimod.projects import service


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
        summary = asyncio.run(
            service.get_project_data(project_name, 0 if not stats else days)
        )
        for k, v in attr.asdict(summary).items():
            click.echo(f"{k}: {v}")
    except exceptions.PyPIAPIError as e:
        click.echo(e, err=True)
