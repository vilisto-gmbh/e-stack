#!/usr/bin/env bash
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "app_db" <<-EOSQL

  CREATE USER migrations_db_user WITH PASSWORD '${MIGRATIONS_DB_USER_PASSWORD}';
  GRANT ALL PRIVILEGES ON DATABASE app_db TO migrations_db_user;
  ALTER SCHEMA app_schema OWNER TO migrations_db_user;
  ALTER SCHEMA orchestrator OWNER TO migrations_db_user;

  CREATE USER seed_db_user WITH PASSWORD '${SEED_DB_USER_PASSWORD}';
  GRANT ALL PRIVILEGES ON SCHEMA app_schema TO seed_db_user;
  ALTER DEFAULT PRIVILEGES FOR ROLE migrations_db_user IN SCHEMA app_schema
    GRANT ALL PRIVILEGES ON TABLES TO seed_db_user;

  CREATE USER interface_db_user WITH PASSWORD '${INTERFACE_DB_USER_PASSWORD}';
  GRANT ALL PRIVILEGES ON SCHEMA app_schema TO interface_db_user;
  ALTER DEFAULT PRIVILEGES FOR ROLE migrations_db_user IN SCHEMA app_schema
    GRANT ALL PRIVILEGES ON TABLES TO interface_db_user;

  CREATE USER frontend_db_user WITH PASSWORD '${FRONTEND_DB_USER_PASSWORD}';
  GRANT USAGE ON SCHEMA app_schema TO frontend_db_user;
  ALTER DEFAULT PRIVILEGES FOR ROLE migrations_db_user IN SCHEMA app_schema
    GRANT SELECT ON TABLES TO frontend_db_user;

  CREATE USER orchestrator_db_user WITH PASSWORD '${ORCHESTRATOR_DB_USER_PASSWORD}';
  GRANT ALL PRIVILEGES ON SCHEMA orchestrator TO orchestrator_db_user;
  ALTER DEFAULT PRIVILEGES FOR ROLE orchestrator_db_user IN SCHEMA orchestrator
    GRANT ALL PRIVILEGES ON TABLES TO orchestrator_db_user;

EOSQL

