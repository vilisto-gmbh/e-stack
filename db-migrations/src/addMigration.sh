#!/bin/bash

if [ -z "$1" ]; then
  echo "No argument supplied. Usage: ./addMigration.sh <script_name> '<script_description>'  "
  exit 1
fi

if [ -z "$2" ]; then
  echo "No description supplied. Please add a description of the script. Usage: ./addMigration.sh <script_name> '<script_description>' "
  exit 1
fi

FILE="$(date +'%Y%m%d%H%M%S')_${1// /_}.sql"


FILE_SQITCH_PLAN="$(date +'%Y%m%d%H%M%S')_${1// /_}" 
TIMESTAMP=`date +%Y-%m-%dT%H:%M:%SZ`
BENUTZER="$USER"
HOST="james_prescott_joule"

echo "$FILE_SQITCH_PLAN"" ""$TIMESTAMP"" ""$BENUTZER"""  "<""$USER""@""$HOST"">"" ""#"" ""$2" >> ./sqitch.plan

# Deploy script
echo "-- Deploy $FILE to pg --" > ./deploy/$FILE

# Verify script
echo "-- Verify $FILE --" > ./verify/$FILE

# Revert script
echo "-- Revert $FILE --" > ./revert/$FILE
