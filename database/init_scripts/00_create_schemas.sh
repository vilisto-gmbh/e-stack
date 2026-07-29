#!/usr/bin/env bash
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "app_db" <<-EOSQL
  CREATE SCHEMA app_schema;
  CREATE SCHEMA orchestrator;
EOSQL
