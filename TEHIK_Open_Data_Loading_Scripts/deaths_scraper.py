import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

from helpers import NpEncoder
from chart_data_functions import *

url = 'https://www.terviseamet.ee/et/koroonaviirus/koroonakaart'
html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')

DEATH_FILE_LOCATION = 'deaths.json'

def printToJson(fileLocation, dataDict):
    with open(fileLocation, "w", encoding="utf-8") as f:
        json.dump(dataDict, f, cls=NpEncoder, ensure_ascii=False)

def read_json_from_file(path) -> any:
     with open(path) as f:
         data = json.load(f)
     return data

deaths_container = soup.select('.node-lead-default strong')
if len(deaths_container) > 0:
    deaths_count = int(deaths_container[0].text.strip())
    current_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    json_deaths = read_json_from_file(DEATH_FILE_LOCATION)

    deaths_output = {}
    if len(json_deaths):
        deaths_output = json_deaths

    deaths_output[current_date] = deaths_count

    printToJson(DEATH_FILE_LOCATION, deaths_output)
