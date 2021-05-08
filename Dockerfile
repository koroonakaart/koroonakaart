############################
# STEP 1 fetch data from TEHIK and aggregate it to into data.json
############################
# https://hub.docker.com/_/python
FROM python:3-slim AS fetch_data
ENV PATH=$PATH:/root/.poetry/bin \
    PYTHONPATH=/app

WORKDIR /app

# Prepare environment separately to improve caching
RUN set -exu \
 && apt-get update \
 && apt-get install -y curl \
 && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# Install Python dependencies - they change less often than code so caches better
COPY pyproject.toml poetry.lock ./

RUN set -exu \
 && python -m pip install --upgrade pip \
 && poetry install

# Run the Python scripts themselves
COPY build build
COPY data data
RUN set -exu \
 && poetry run download \
 && ls -lhaF data

RUN set -exu \
 && mkdir -p koroonakaart/src/data \
 && poetry run generate \
 && ls -lhaF koroonakaart/src/data

#########################
# STEP 2 build frontend
#########################
# https://hub.docker.com/_/node
FROM node:lts-slim AS build_frontend

WORKDIR /app
COPY koroonakaart koroonakaart

COPY --from=fetch_data /app/koroonakaart/src/data/*.json /app/koroonakaart/src/data/
RUN set -exu \
 && cd koroonakaart \
 && npm install --silent \
 && npm run build

#########################
# STEP 3 build the image (Nginx serving frontend)
#########################
# https://hub.docker.com/_/nginx
FROM nginx:mainline-alpine AS runtime

# Nginx needs to redirect requests like '/et' etc to index.html
RUN set -exu \
 && sed -i '/index.html index.htm;/ i try_files $uri /index.html;' /etc/nginx/conf.d/default.conf \
 && mkdir -p /usr/share/nginx/html/data/

COPY --from=build_frontend /app/koroonakaart/dist /usr/share/nginx/html
COPY --from=build_frontend /app/koroonakaart/src/data/*.json /usr/share/nginx/html/data/
