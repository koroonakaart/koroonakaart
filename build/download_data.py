import traceback
from datetime import datetime
from datetime import timedelta
from shutil import move

import requests
from bs4 import BeautifulSoup
from constants import DEATHS_PATH
from constants import HOSPITALIZATION_PATH
from constants import TEST_LOCATIONS_PATH
from constants import TEST_RESULTS_PATH
from constants import VACCINATIONS_PATH
from utils import log_status
from utils import read_json_from_file
from utils import save_as_json


DEATHS_SELECTOR = ".node-lead-default strong"

TESTING_ENDPOINT = "https://opendata.digilugu.ee/opendata_covid19_test_results.json"
TEST_LOCATION_ENDPOINT = "https://opendata.digilugu.ee/opendata_covid19_test_location.json"
HOSPITALIZATION_ENDPOINT = "https://opendata.digilugu.ee/opendata_covid19_hospitalization_timeline.json"
VACCINATION_ENDPOINT = "https://opendata.digilugu.ee/covid19/vaccination/v3/opendata_covid19_vaccination_total.json"
TERVISEAMET_COVID_DASHBOARD = "https://www.terviseamet.ee/et/koroonaviirus/koroonakaart"


def is_up_to_date(json_data, date_field_name):
    yesterday = datetime.today() - timedelta(1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    file_date_time = datetime.strptime(
        json_data[0][date_field_name].split("T")[0], "%Y-%m-%d"
    )
    if file_date_time >= yesterday:
        return True
    return False


def download_json_data(url, destination):
    log_status(f"Downloading {url} to {destination}")

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(destination, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def scrape_deaths():
    # Load content from Terviset's Covid dashboard and parse it
    log_status("Scraping data on deaths from " + TERVISEAMET_COVID_DASHBOARD)
    html = requests.get(TERVISEAMET_COVID_DASHBOARD).text
    soup = BeautifulSoup(html, "html.parser")

    # Extract number of deaths from page content and update JSON data on deaths
    deaths_container = soup.select(DEATHS_SELECTOR)
    if len(deaths_container) > 0:
        try:
            # Get number of deaths and the current date
            deaths_count = int(deaths_container[0].text.strip())
            current_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

            # Load existing deaths data
            json_deaths = read_json_from_file(DEATHS_PATH)

            # Add new entry to deaths data for current date
            deaths_output = {}
            if len(json_deaths):
                deaths_output = json_deaths
            deaths_output[current_date] = deaths_count

            # Save data on deaths
            save_as_json(DEATHS_PATH + ".tmp", deaths_output)

            # Log status
            log_status("Successfully scraped deaths. Total deaths: " + str(deaths_count))
        except:
            # Log error
            error_message = "Error when scraping data on deaths"
            log_status(error_message + ":")
            log_status(traceback.format_exc())
            raise Exception(error_message)
    else:
        # Log error
        error_message = "Error: could not find page element with data on deaths"
        log_status(error_message)
        raise Exception(error_message)


def main():
    deaths = False
    try:
        scrape_deaths()
        deaths = True
    except:
        log_status("Failed to scrape deaths")
        pass

    # Download data from external services
    log_status("Downloading data from TEHIK: Test results")
    download_json_data(TESTING_ENDPOINT, TEST_RESULTS_PATH + ".tmp")

    log_status("Downloading data from TEHIK: Location data")
    download_json_data(TEST_LOCATION_ENDPOINT, TEST_LOCATIONS_PATH + ".tmp")

    log_status("Downloading data from TEHIK: Hospitalization data")
    download_json_data(HOSPITALIZATION_ENDPOINT, HOSPITALIZATION_PATH + ".tmp")

    log_status("Downloading data from TEHIK: Vaccination data")
    download_json_data(VACCINATION_ENDPOINT, VACCINATIONS_PATH + ".tmp")

    # Validate data from remote endpoints
    #
    # TODO: Add checks that the testing and vaccination data are up to date. We will need to adopt
    #       a different approach than for the test location and hospitalisation data due to the fact
    #       that the data structure of the JSON is different. Checking the "Last-Modified" header of the
    #       response may be the way to go and would handle the possibility that there are no tests or
    #       vaccinations on a particular day.
    
    hospitalization = read_json_from_file(HOSPITALIZATION_PATH + ".tmp")
    if not is_up_to_date(hospitalization, "LastLoadStatisticsDate"):
        raise Exception("Hospitalization data is not up-to-date")

    log_status("All OK, replacing old files with downloaded files")
    if deaths:
        move(DEATHS_PATH + ".tmp", DEATHS_PATH)
    move(TEST_RESULTS_PATH + ".tmp", TEST_RESULTS_PATH)
    move(TEST_LOCATIONS_PATH + ".tmp", TEST_LOCATIONS_PATH)
    move(HOSPITALIZATION_PATH + ".tmp", HOSPITALIZATION_PATH)
    move(VACCINATIONS_PATH + ".tmp", VACCINATIONS_PATH)

