#!/bin/bash

liquibase \
  --classpath="$LIQUIBASE_CLASSPATH" \
  --hub-mode="$LIQUIBASE_HUB_MODE" \
  --strict="$LIQUIBASE_STRICT" \
  --headless="$LIQUIBASE_HEADLESS" \
  update \
  --changelog-file="$LIQUIBASE_CHANGELOG_FILE" \
  --url="$LIQUIBASE_COMMAND_URL" \
  --username="$LIQUIBASE_COMMAND_USERNAME" \
  --password="$LIQUIBASE_COMMAND_PASSWORD" \
