############################
# STEP 1 fetch data from TEHIK and aggregate it to into data.json
############################
# https://hub.docker.com/_/python
FROM python:3-slim AS fetch_data
ENV PATH=$PATH:/root/.poetry/bin

WORKDIR /app

# Prepare environment separately to improve caching
RUN set -exu \
 && apt-get update \
 && apt-get install -y curl \
 && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# Install Python dependencies - they change less often than code so caches better
RUN mkdir TEHIK_Open_Data_Loading_Scripts
COPY TEHIK_Open_Data_Loading_Scripts/pyproject.toml TEHIK_Open_Data_Loading_Scripts/poetry.lock TEHIK_Open_Data_Loading_Scripts

RUN set -exu \
 && cd TEHIK_Open_Data_Loading_Scripts \
 && python -m pip install --upgrade pip \
 && poetry install

# Run the Python scripts themselves
COPY . .
RUN set -exu \
 && cd TEHIK_Open_Data_Loading_Scripts \
 && poetry run python deaths_scraper.py \
 && poetry run python main.py \
 && ls -lhaF ../data

#########################
# STEP 2 build frontend
#########################
# https://hub.docker.com/_/node
FROM node:lts-slim AS build_frontend

WORKDIR /app
COPY . .

COPY --from=fetch_data /app/data/data.json /app/koroonakaart/src/data.json
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
RUN sed -i '/index.html index.htm;/ i try_files $uri /index.html;' /etc/nginx/conf.d/default.conf

COPY --from=build_frontend /app/koroonakaart/dist /usr/share/nginx/html
COPY --from=build_frontend /app/data/data.json /usr/share/nginx/html/data.json
