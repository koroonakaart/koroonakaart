import traceback

from bs4 import BeautifulSoup
from chart_data_functions import *
import requests
from utils import log_status
from utils import read_json_from_file
from utils import save_as_json

url = "https://www.terviseamet.ee/et/koroonaviirus/koroonakaart"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

DEATH_FILE_LOCATION = "../data/deaths.json"

log_status("Crawling data on deaths from " + url)
deaths_container = soup.select(".node-lead-default strong")
if len(deaths_container) > 0:
    try:
        deaths_count = int(deaths_container[0].text.strip())
        current_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        json_deaths = read_json_from_file(DEATH_FILE_LOCATION)

        deaths_output = {}
        if len(json_deaths):
            deaths_output = json_deaths

        deaths_output[current_date] = deaths_count

        save_as_json(DEATH_FILE_LOCATION, deaths_output)

        # Log status
        log_status("Successfully crawled deaths. Total deaths: " + str(deaths_count))
    except:
        # Log error
        log_status("Error when crawling data on deaths:")
        log_status(traceback.format_exc())
else:
    # Log error
    log_status("Error: could not find page element with data on deaths")
