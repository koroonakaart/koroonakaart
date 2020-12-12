#!/bin/bash

declare -A output_array
output_array[git_output]=$(git -C .. pull origin 2>&1 > /dev/null)
output_array[pip_output]=$(pip3 install -r requirements.txt 2>&1 > /dev/null)
output_array[deaths_scraper]=$(python3 deaths_scraper.py 2>&1 > /dev/null)
output_array[main_python]=$(python3 main.py 2>&1 > /dev/null)

# Avoid 30 seconds of downtime and save a copy of 1 version
rm -rf ../../backup
mkdir ../../backup
cp -Ra ../../koroonakaart ../../backup
ln -srfn ../../backup/koroonakaart/koroonakaart/dist ../../current

# Copy data.json into js src folder
cp -af ../data/data.json ../koroonakaart/src

cd ../koroonakaart
output_array[npm]=$(npm run build 2>&1 > /dev/null)
cd - 2>&1 > /dev/null

ln -srfn ../../koroonakaart/koroonakaart/dist ../../current

. ./after_data_updated.sh
