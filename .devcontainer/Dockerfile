# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT=3-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

ENV PYTHONUNBUFFERED 1

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp


# Use the PostgreSQL apt repository to install Postgres command line tools (see https://www.postgresql.org/download/linux/debian/)
# Create the file repository configuration:
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' \
# Import the repository signing key:
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# [Optional] Uncomment this section to install additional OS packages.
ARG POSTGRES_VERSION="14"
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends postgresql-client-${POSTGRES_VERSION} \

# Clean up apt-get as per https://github.com/hadolint/hadolint/wiki/DL3009
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Install Liquibase
ARG LIQUIBASE_VERSION=4.16.1
ARG LIQUIBASE_DOWNLOAD_DIR=/tmp/liquibase
ARG LIQUIBASE_INSTALL_DIR=/usr/local/bin/liquibase/
RUN export LIQUIBASE_BUNDLE=liquibase-${LIQUIBASE_VERSION}.zip \
    && mkdir -p ${LIQUIBASE_DOWNLOAD_DIR} \
    && mkdir -p ${LIQUIBASE_INSTALL_DIR} \
    && cd ${LIQUIBASE_DOWNLOAD_DIR} || exit \
    && wget -q --show-progress https://github.com/liquibase/liquibase/releases/download/v${LIQUIBASE_VERSION}/${LIQUIBASE_BUNDLE} \
    && unzip ${LIQUIBASE_BUNDLE} \
    && cp -r ${LIQUIBASE_DOWNLOAD_DIR}/. ${LIQUIBASE_INSTALL_DIR} \
    && chmod +x ${LIQUIBASE_INSTALL_DIR}liquibase \
    && rm -rf ${LIQUIBASE_DOWNLOAD_DIR}

# Install Gauge
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -SsL https://downloads.gauge.org/stable | sh \
    && su vscode -c "gauge install python" \
    && su vscode -c "gauge install html-report" \
    && su vscode -c "gauge install screenshot"
