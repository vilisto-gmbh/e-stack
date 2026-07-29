#!/bin/bash
if [ -f $MIGRATIONS_DB_USER_PASSWORD_FILE ];
then export MIGRATIONS_DB_USER_PASSWORD="$(cat $MIGRATIONS_DB_USER_PASSWORD_FILE)";
else echo "No migrations_db_user_password secret provided.";
fi

errormsg=$(sqitch deploy --target "db:pg://migrations_db_user:${MIGRATIONS_DB_USER_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/app_db")
rescode=$?
errormsg_stripped=$(echo $errormsg | cut -f -3 -d" ")

errormsg=$(sqitch verify --target "db:pg://migrations_db_user:${MIGRATIONS_DB_USER_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/app_db" 2>&1)

if [ "$errormsg_stripped" = "Nothing to deploy" ]
then
    echo "The command exited with return code $rescode because of the error $errormsg"
    echo "Exiting with return code 0, as decided to ignore the error type"
    res=0
elif [ "$errormsg_stripped" = "Cannot find change" ]
then
    echo "The command exited with return code $rescode because of the error $errormsg"
    echo "Exiting with return code 0, as decided to ignore the error type"
    res=0
else
    echo $errormsg
    echo $rescode
    res=$rescode
fi
exit $res
