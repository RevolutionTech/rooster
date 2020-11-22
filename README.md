# Rooster
#### A tool to review activity on GitHub for daily standup

[![Build Status](https://travis-ci.com/RevolutionTech/rooster.svg?branch=master)](https://travis-ci.com/RevolutionTech/rooster)
[![codecov](https://codecov.io/gh/RevolutionTech/rooster/branch/master/graph/badge.svg)](https://codecov.io/gh/RevolutionTech/rooster)

## Setup

### Installation

Use [poetry](https://github.com/sdispater/poetry) to install Python dependencies:

    poetry install

### Configuration

Rooster reads in environment variables from your local `.env` file. See `.env-sample` for configuration options. Be sure to [generate your own secret key](http://stackoverflow.com/a/16630719).

With everything installed and all files in place, you may now create the database tables. You can do this with:

    poetry run python manage.py migrate

### Deployment

Rooster is deployed as a `zappa` app on AWS Lambda. To modify the deployment settings, first you will need to decrypt the `zappa_settings.json.enc` to `zappa_settings.json`:

    openssl aes-256-cbc -k $DECRYPT_PASSWORD -in zappa_settings.json.enc -out zappa_settings.json -d

where `$DECRYPT_PASSWORD` contains the key that the settings were encrypted with.

Then, generate a Docker container and run the container to execute zappa commands, such as `deploy`:

    poetry run zappa deploy

Once deployed, you will need to set environment variables on the generated Lambda. See `ProdConfig` for additional environment variables used in production.

You may also need to update `ALLOWED_HOSTS` in `ProdConfig` to match the assigned URL for the Lambda. Once completed, the assigned URL should be running Rooster.

If any changes to `zappa_settings.json` are made, the file should be re-encrypted before being committed. The following bash functions may be helpful for encrypting/decrypting:

    function encrypt_openssl () { openssl aes-256-cbc -k $DECRYPT_PASSWORD -in "$1" -out "$1".enc; }
    function decrypt_openssl () { openssl aes-256-cbc -k $DECRYPT_PASSWORD -in "$1".enc -out "$1" -d; }
