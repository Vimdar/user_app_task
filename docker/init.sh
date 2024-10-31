#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER ${DBUSER} WITH ENCRYPTED PASSWORD '${DBPASS}' NOSUPERUSER NOCREATEDB NOCREATEROLE;
    ALTER USER ${DBUSER} CREATEDB;
    CREATE DATABASE ${DBNAME} WITH ENCODING 'UTF8';
    -- change ALL to restrict more if needed
    GRANT ALL PRIVILEGES ON DATABASE ${DBNAME} TO ${DBUSER};
    \connect ${DBNAME};
    CREATE SCHEMA ${DBSCHEMA};
    GRANT ALL ON SCHEMA ${DBSCHEMA} TO ${DBUSER};
EOSQL