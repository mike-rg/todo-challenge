#!/bin/bash
set -e
psql -U "$POSTGRES_USER" postgres -c "DROP DATABASE IF EXISTS $POSTGRES_DB";
psql -U "$POSTGRES_USER" postgres -c "CREATE DATABASE $POSTGRES_DB";
