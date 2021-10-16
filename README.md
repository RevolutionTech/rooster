# Rooster
#### A tool to review activity on GitHub for daily standup

## Deprecated

This project is no longer being maintained by the owner. Rooster has been moved to a [Cascade](https://www.cascade.io/) workflow.

---

![CI](https://github.com/RevolutionTech/rooster/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/RevolutionTech/rooster/branch/main/graph/badge.svg)](https://codecov.io/gh/RevolutionTech/rooster)

## Setup

### Installation

Use [poetry](https://github.com/sdispater/poetry) to install Python dependencies:

    poetry install

### Configuration

Rooster reads in environment variables from your local `.env` file. See `.env-sample` for configuration options. Be sure to [generate your own secret key](http://stackoverflow.com/a/16630719).

With everything installed and all files in place, you may now create the database tables. You can do this with:

    poetry run python manage.py migrate
