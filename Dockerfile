############################
# STEP 1 fetch data from TEHIK and aggregate it to into data.json
############################
# https://hub.docker.com/_/python
FROM python:3.7-buster AS fetch_data

WORKDIR /app
COPY . .
RUN cd TEHIK_Open_Data_Loading_Scripts \
    python -m pip install --upgrade pip \
    python main.py

#########################
# STEP 2 build frontend
#########################
# https://hub.docker.com/_/node
FROM node:erbium-buster AS build_frontend

WORKDIR /app
COPY . .

COPY --from=fetch_data /app/koroonakaart/src/data.json /app/koroonakaart/src/data.json
RUN cd koroonakaart \
    npm install --silent \
    npm run build

#########################
# STEP 3 build the image (Nginx serving frontend)
#########################
FROM nginx:1.19.2-alpine

COPY --from=build_frontend /app/koroonakaart/dist /usr/share/nginx/html
