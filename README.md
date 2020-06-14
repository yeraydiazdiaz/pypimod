# pypimod - A tool for PyPI moderators

A tool for PyPI moderators to perform different tasks such as:

- Quick surfacing of useful links related to a package
- Retrieval of relevant statistics

# CLI

## `pypimod info <PROJECT>`

Display project information for a project name.

- `--stats` will retrieve stats from BigQuery
- `--days N` for the last N days, defaults to 31

```
$ pypimod info lunr
name: lunr
summary: A Python implementation of Lunr.js
version: 0.5.5
author: Yeray Diaz Diaz
project_url: https://pypi.org/project/lunr/
release_url: https://pypi.org/project/lunr/0.5.5/
last_release_datetime: 2019-04-28T15:25:03
```

## BigQuery setup

To retrieve stats from BigQuery you will need to setup a Google Cloud project
and generate and download service account JSON. The service account must
have the "BigQuery Job User IAM role".

`pypimod` will cache results of queries in the `.cache` directory to avoid
incurring in excessive costs, you will need to manually remove these
cached results files to refresh retrieval of statistics.
