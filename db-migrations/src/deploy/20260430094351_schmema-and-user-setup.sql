-- Deploy 20260430094351_schmema-and-user-setup.sql to pg --
\set schema_name `echo $SCHEMA_NAME`

\set user_password `echo $DB_USER_PASSWORD`
\set dagster_user_password `echo $DAGSTER_USER_PASSWORD`


create schema if not exists :schema_name;
create schema if not exists dagster;

create user :user_name with password :'user_password';
create user dagster_user with password :'dagster_user_password';

grant all privileges on schema :schema_name to :user_name;
grant all privileges on schema dagster to dagster_user;
