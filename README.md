# pypimod - A tool for PyPI moderators

A tool for PyPI moderators to perform different tasks such as:

- Quick surfacing of useful links related to a package
- Retrieval of relevant statistics

# CLI

## `pypimod info <PROJECT>`

- Links to standard + admin links for project and owner
- Release information
- `--stats` will retrieve stats from BigQuery
- `--days N` for the last N days, defaults to 31

## `pypimod check <PROJECT>`

- Download release (default to latest) to tmp dir
- Perform checks on downloaded release

## Status

Very much alpha. Initially written as a helper tool for PEP 541 requests
and created separately to Warehouse for quicker exploration.

## BigQuery setup

To retrieve stats from BigQuery you will need to setup a Google Cloud project
and generate and download service account JSON. The service account must
have the "BigQuery Job User IAM role".

`pypimod` will cache results of queries in the `dev` directory to avoid
incurring in excessive costs, you will need to manually remove these
cached results files to refresh retrieval of statistics.

## Future ideas

Some of tasks could be performed in the Warehouse codebase leveraging PyPA's
credentials. Another option would be to make this a GitHub bot similar to
Python's [bedevere](https://github.com/python/bedevere).

It is very likely this will evolve beyond the scope of PEP 541 soon,
for example for requests for upload limits.
