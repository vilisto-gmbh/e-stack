# E-stack

Out-of-the-box-framework for data pipelines including database, frontend and orchestration services. This architecture was originally built for energy time series data but can be used for any type of data.
All services are containerized and meant to be run locally via docker compose. In order to keep things simple and suited for this purpose, the number of database users was kept as low as possible and passwords are injected using environment variables.

To use the stack in a production environment, make sure to securely inject sensitive data such as passwords, for instance by using docker secrets. It is also advised to create an individual database user with further reduced privileges per service. 

# Setup

## Environment

Define environment variables in a file called `.env` in the root directory:

```bash
cp .env-example .env
```

| Name | Description | Example |
| --- | --- | --- |
| POSTGRES_PORT | Port that database listens on | 5432 |
| POSTGRES_USER | Database superuser name | postgres |
| POSTGRES_PASSWORD | Database superuser password | timescale |
| POSTGRES_DB | Database name| e-stack |
| POSTGRES_HOST | Database host | db |
| DB_USER | Database regular user name | james_prescott_joule |
| DB_USER_PASSWORD | Database regular user password | super_secret_password |
| SCHEMA_NAME | Default user application schema name | energy |
| POSTGREST_HOST | Hostname of the postgREST service | db |
| PGRST_ADMIN_SERVER_PORT | Admin server port for PostgREST | 3001 |
| PGRST_SERVER_PORT | Main server port for postgREST | 3000 |
| GRAFANA_PORT | Port the Grafana frontend is served on | 9000 |
| GF_SECURITY_ADMIN_PASSWORD | Password for the Grafana admin user | highly_secret_password |
| DAGSTER_WS_PORT | Port for the Dagster webserver | 4000 |
| DAGSTER_UC_PORT | Port for the Dagster user code server | 4001 |

## Running the stack

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
This database serves as storage for sqitch and dagster meta data as well. Each service stores its data in its own namespace however.

## db-interface
Uses [postgREST](https://docs.postgrest.org/en/v14/) as an interface to the database.

## db-migrations
Uses [sqitch](https://sqitch.org/docs/) for database management and version control. 

## frontend
Uses a [grafana](https://grafana.com/docs/) frontend.

## orchestrator
Uses [dagster](https://docs.dagster.io/) for job orchestration.
