#!/bin/bash
errormsg=$(sqitch deploy --target "db:pg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}")
rescode=$?
errormsg_stripped=$(echo $errormsg | cut -f -3 -d" ")

errormsg=$(sqitch verify --target "db:pg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}" 2>&1)

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