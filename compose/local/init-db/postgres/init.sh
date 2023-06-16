#!/bin/bash
set -e

# Especifica el nombre del archivo de dump
DUMP_FILE="initdb.dump"

# Restaurar la base de datos
psql -U "$POSTGRES_USER" postgres -c "DROP DATABASE IF EXISTS $POSTGRES_DB"
psql -U "$POSTGRES_USER" postgres -c "CREATE DATABASE $POSTGRES_DB"
pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" "$DUMP_FILE"

echo "Database restoration completed successfully."
