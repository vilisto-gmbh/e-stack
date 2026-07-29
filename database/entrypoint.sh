#!/usr/bin/env bash
set -e

export_file_env_var() {
  local var="$1"
  local file_var="${var}_FILE"

  if [ -f "${!file_var}" ];
  then export "$var"="$(cat "${!file_var}")";
  else echo "No secret for ${var} environment variable provided.";
  fi
}

export_file_env_var MIGRATIONS_DB_USER_PASSWORD
export_file_env_var INTERFACE_DB_USER_PASSWORD
export_file_env_var FRONTEND_DB_USER_PASSWORD
export_file_env_var ORCHESTRATOR_DB_USER_PASSWORD

exec docker-entrypoint.sh "$@"
