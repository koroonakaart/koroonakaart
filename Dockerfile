############################
# STEP 1 fetch data from TEHIK and aggregate it to into data.json
############################
# https://hub.docker.com/_/python
FROM python:3.7-buster AS fetch_data

WORKDIR /app
COPY . .
RUN cd TEHIK_Open_Data_Loading_Scripts && \
    pip3 install -r requirements.txt && \
    python3 deaths_scraper.py && \
    python3 main.py

#########################
# STEP 2 build frontend
#########################
# https://hub.docker.com/_/node
FROM node:erbium-buster AS build_frontend

WORKDIR /app
COPY . .

COPY --from=fetch_data /app/data/data.json /app/koroonakaart/src/data.json
RUN cd koroonakaart && \
    npm install --silent && \
    npm run build

#########################
# STEP 3 build the image (Nginx serving frontend)
#########################
# https://hub.docker.com/_/nginx
FROM nginx:1.19.6-alpine

# Nginx needs to redirect requests like '/et' etc to index.html
RUN sed -i '/index.html index.htm;/ i try_files $uri /index.html;' /etc/nginx/conf.d/default.conf

COPY --from=build_frontend /app/koroonakaart/dist /usr/share/nginx/html
COPY --from=fetch_data /app/data/data.json /usr/share/nginx/html/data.json
