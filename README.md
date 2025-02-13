# central-bank-scraper
Scrape the cental banks data.

[![python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org)

## Prerequisites
The package is developed and tested on Python 3.11+. Please make sure you have the correct Python version installed.


## Setup
`curl -sSL "https://install.python-poetry.org" | python - &&`
`cd central-bank-scraoer`
`poetry install --sync`

## Deploy dockerized locally (headless)
Setup local database with password:

`poetry run python scripts/set_sql_login.py create_new postgres postgresql://postgres:postgres@db:5432/test_db`


Copy and setup configuration file

`cp deploy/.env.template .env`

Build the image:

`docker build . -t central_banks_scrapper`

Run using:

`docker compose -f docker-compose.yml -f docker-compose-db.yml`

