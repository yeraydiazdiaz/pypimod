# pypimod - A tool for PyPI moderators

A tool for PyPI moderators to perform different tasks such as:

- Quick surfacing of useful links related to a package
- Retrieval of relevant statistics

# CLI

1. `pypimod info <PROJECT>`:
    - links to standard + admin links for project and owner
    - release information
2. `pypimod stats <PROJECT>`:
    - stats for a selected period of time
3. `pypimod check <PROJECT>`:
    - download release (default to latest) to tmp dir
    - perform checks:
        + line count
        + installable?

## Status

Very much alpha. Initially written as a helper tool for PEP 541 requests
and created separately to Warehouse for quicker exploration.

## Future ideas

Some of tasks could be performed in the Warehouse codebase leveraging PyPA's
credentials. Another option would be to make this a GitHub bot similar to
Python's [bedevere](https://github.com/python/bedevere).

It is very likely this will evolve beyond the scope of PEP 541 soon,
for example for requests for upload limits.
