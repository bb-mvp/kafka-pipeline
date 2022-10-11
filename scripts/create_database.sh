#!/bin/bash

echo "SELECT 'CREATE DATABASE $DATABASE_NAME' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DATABASE_NAME')\gexec" | psql
