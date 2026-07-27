# Intro

IMPORTANT: Parts of this software are being filed for patent, registration number 24176723.5: "Method, System and Computer Program
for Determining an Efficiency of an Energy-Saving Measure in Buildings".

# Setup

Build the docker stack for the first time via
```bash
docker compose up
```

When rebuilding from scratch use
```bash
docker compose up --force-recreate --renew-anon-volumes --remove-orphans --build
```

# Services

## database
Uses a [timescale](https://timescale.readthedocs.io/en/latest/) SQL database. Whenever rebuilding everything from scratch remember to get rid of all data in the data directory:

```bash
rm -r database/data/*
```

## db-interface
Uses [postgREST](https://docs.postgrest.org/en/v14/) as an interface to the database.

## db-migrations
Uses [sqitch](https://sqitch.org/docs/) for database management and version control. 

## frontend
Uses a [grafana](https://grafana.com/docs/) frontend.

## orchestrator
Uses [dagster](https://docs.dagster.io/) for job orchestration.