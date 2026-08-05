#! /bin/sh
set -e

export_file_env_var() {
  var="$1"
  file_var="${var}_FILE"
  eval "file_path=\${$file_var}" 

  if [ -f "$file_path" ];
  then export "$var"="$(cat "$file_path")";
  else echo "No secret for ${var} environment variable provided.";
  fi
}

export_file_env_var SEED_DB_USER_PASSWORD
export DB_URI=postgresql://seed_db_user:${SEED_DB_USER_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/app_db

if [ -f "/temp_data/sentinel" ]; then
  echo "Found sentinel, skipping seed_db execution."; 
else
  psql $DB_URI -c "\copy app_schema.energy_data(time, power, th_amb, th_amb_prev_day, is_workday) FROM '/src/data/sample_data.csv' DELIMITER ';' CSV HEADER;";
  touch /temp_data/sentinel;
  echo "Executed seed_db and left sentinel.";
fi
