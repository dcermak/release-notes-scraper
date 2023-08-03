# release-notes-scraper

This simple script can be used to grab the release notes for projects from
github that do not keep a `CHANGELOG`, but publish their release notes via the
releases page.


## Prerequisites

You will need the following tools:

- Python 3.10 or later
- [`poetry`](https://python-poetry.org/)

Additionally, you have to clone this repository and initialize poetry:
```ShellSession
❯ git clone https://github.com/dcermak/release-notes-scraper.git
❯ poetry install
```

## Usage

To grab the changelog of a the project `octocat/foobar`, run:

```ShellSession
❯ poetry run ./release-notes-scraper.py octocat foobar
1.0.5

- We did cool stuff!
```

You can also specify the maximum version to be included in the output via the
CLI flag `--max-version` and the minimum version that should **not** be included
(i.e. the next release after `$min_version` will be present) in the output via
the CLI flag `--min-version`:

```ShellSession
❯ poetry run ./release-notes-scraper.py octocat foobar --min-version 1.0.5
```
