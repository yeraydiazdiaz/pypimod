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
author_email: yeraydiazdiaz@gmail.com
project_url: https://pypi.org/project/lunr/
release_url: https://pypi.org/project/lunr/0.5.5/
last_release_datetime: 2019-04-28T15:25:03
```

## `pypimod serve`

Start a GitHub bot server. The server will listen by default on port 8080
and will respond to webhook requests from GitHub as part of the
[`pypimod` app](https://github.com/apps/pypimod).

When PEP 541 issues are created the bot will apply the correct label and
post a comment with information about the project.

## `pypimod check <PROJECT>` Not yet implemented

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
credentials.

It is very likely this will evolve beyond the scope of PEP 541 soon,
for example for requests for upload limits.
