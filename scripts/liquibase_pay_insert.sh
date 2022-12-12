#!/bin/bash

liquibase \
  --classpath="$LIQUIBASE_CLASSPATH" \
  --hub-mode="$LIQUIBASE_HUB_MODE" \
  --strict="$LIQUIBASE_STRICT" \
  --headless="$LIQUIBASE_HEADLESS" \
  update \
  --changelog-file="$LIQUIBASE_CHANGELOG_FILE" \
  --contexts="load-data" \
  --url="jdbc:postgresql://$DATABASE_HOST:$DATABASE_PORT/$DATABASE_NAME" \
  --username="$DATABASE_USERNAME" \
  --password="$DATABASE_PASSWORD" \
