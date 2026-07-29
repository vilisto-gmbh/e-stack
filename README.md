# E-stack

Out-of-the-box-framework for data pipelines including database, frontend and orchestration services. This architecture was originally built for energy time series data but can be used for any type of data.
All services are containerized and meant to be run locally via docker compose.

# Setup

## Environment

Define environment variables with basic configuration in a file called `.env` in the root directory:
```bash
cp .env-example .env
```
| Name | Description | Example |
| --- | --- | --- |
| POSTGRES_PORT | Port that TimescaleDB listens on | 5432 |
| POSTGRES_HOST | TimescaleDB host | db |
| POSTGREST_HOST | PostgREST host | db |
| PGRST_SERVER_PORT | Port that PostgREST is served on | 3000 |
| PGRST_ADMIN_SERVER_PORT | Admin  port for PostgREST | 3001 |
| GRAFANA_PORT | Port that Grafana is served on | 9000 |
| DAGSTER_WS_PORT | Port that Dagster Webserver is served on | 4000 |
| DAGSTER_UC_PORT | Port that Dagster User Code is served on | 4001 |

Sensitive data is stored in secrets:
```bash
cp secrets/examples/* secrets/
```

## Running the stack

Build a fresh docker stack using
```bash
docker compose up
```

When rebuilding from scratch use
```bash
docker compose up --force-recreate --renew-anon-volumes --remove-orphans --build
```

## Starting fresh

Remove data that is being persisted cross containers which is app data, migrations, orchestrator data and frontend data:
```bash
rm -r database/data/*
rm -r frontend/data/*
```

# Services

## database
Uses a [timescale](https://timescale.readthedocs.io/en/latest/) SQL database. Whenever rebuilding everything from scratch remember to get rid of all data in the data directory:

This database serves as storage for sqitch and dagster meta data as well. Each service stores its data in its own namespace however.

## db-interface
Uses [postgREST](https://docs.postgrest.org/en/v14/) as an interface to the database.

## db-migrations
Uses [sqitch](https://sqitch.org/docs/) for database management and version control. 

## frontend
Uses a [grafana](https://grafana.com/docs/) frontend.

## orchestrator
Uses [dagster](https://docs.dagster.io/) for job orchestration.
