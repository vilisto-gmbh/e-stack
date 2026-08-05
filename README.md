# E-stack

Out-of-the-box-framework for data pipelines including database, frontend and orchestration services. This architecture was originally built for energy time series data but can be used for any type of data.
All services are containerized and meant to be run locally via docker compose.

# Setup

## Environment

Define environment variables with basic configuration in a file called `.env` in the root directory:
```bash
cp .env-example .env
```
| Name | Description | Default |
| --- | --- | --- |
| POSTGRES_HOST | TimescaleDB host | db |
| POSTGRES_PORT | Port that TimescaleDB listens on | 5432 |
| POSTGREST_HOST | PostgREST host | db-if |
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

## Terminating the stack

End the stack but persist the data via
```bash
docker compose down
```
Start totally fresh by dropping all persisted data including database contents, db-seed sentinels and frontend setup via
```bash
docker compose down --volumes
```

# Services

## database

Uses a [timescale](https://timescale.readthedocs.io/en/latest/) SQL database. Initilization includes the creationof 
    - app_db database
    - app_schema
    - orchestrator schema
    - postgres superuser
    - migrations_db_user who owns all entities created out of db-migrations
    - seed_db_user who inherits all privileges on app_schema and its tables from migrations_db_user
    - interface_db_user who inherits all privileges on app_schema and its tables from migrations_db_user
    - frontend_db_user who has read privileges on app_schema and its tables 
    - orchestator_db_user who inherits all privileges on orchestator schema and its tables from migrations_db_user
This database serves as storage for app, migration and orchestrator data.

## db-migrations

Uses [sqitch](https://sqitch.org/docs/) for database management and version control. In order to add a new migration run  
```bash
sh addMigration.sh <migration name> "<brief description of migration>"
```
Migrations are run against the database every time the stack is started. In order to run a migration against a running stack, use
```bash
docker compose up --no-deps db-migrations
```

## db-seed
This PSQL service populates the database with data specified in `db-seed/data`. After a successfull `seed_db` run, it leaves a sentinel in the db-seed volume which avoids multiple population runs.

## db-interface

Uses [postgREST](https://docs.postgrest.org/en/v14/) as an interface to the database.

## frontend

Uses a [grafana](https://grafana.com/docs/) frontend. Access the frontend via [http://localhost:9000](http://localhost:9000) assuming you have not modified the GRAFANA_PORT environment variable, otherwise use that port. Use admin as user name and the password set in the frontend_db_user_password secret.

## orchestrator

Uses [dagster](https://docs.dagster.io/) for job orchestration. Access the orchestratro web server via [http://localhost:4000](http://localhost:4000) assuming you have not modified the DAGSTER_WS_PORT environment variable, otherwise use that port. For the deployment setup used in this stack, refer to the official dagster documentation.

### Smoke test
Run the stack, navigate to the webserver, click on Lineage -> processed_csv -> Materialize selected. The asset should successfully materialize.

### Adding user code
Add your own python code to orchestrator/src/orchestrator.
