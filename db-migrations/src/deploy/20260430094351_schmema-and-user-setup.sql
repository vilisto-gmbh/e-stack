-- Deploy 20260430094351_schmema-and-user-setup.sql to pg --

\set user_name `echo $DB_USER`
\set user_password `echo $DB_USER_PASSWORD`
\set schema_name `echo $SCHEMA_NAME`

create schema if not exists :schema_name;
create user :user_name with password :'user_password';
grant all privileges on schema :schema_name to :user_name;
grant all privileges on schema public to :user_name;
