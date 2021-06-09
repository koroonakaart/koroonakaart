from datetime import datetime
from datetime import timedelta
from shutil import move

from bs4 import BeautifulSoup
from build.constants import DEATHS_PATH
from build.constants import HOSPITALIZATION_PATH
from build.constants import TEST_LOCATIONS_PATH
from build.constants import TEST_RESULTS_PATH
from build.constants import VACCINATIONS_PATH
from build.utils import analyze_memory
from build.utils import analyze_time
from build.utils import logger
from build.utils import read_json_from_file
from build.utils import save_as_json
import requests
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential

DEATHS_SELECTOR = ".node-lead-default strong"
TESTING_ENDPOINT = "https://opendata.digilugu.ee/opendata_covid19_test_results.json"
TEST_LOCATION_ENDPOINT = (
    "https://opendata.digilugu.ee/opendata_covid19_test_location.json"
)
HOSPITALIZATION_ENDPOINT = (
    "https://opendata.digilugu.ee/opendata_covid19_hospitalization_timeline.json"
)
VACCINATION_ENDPOINT = "https://opendata.digilugu.ee/covid19/vaccination/v2/opendata_covid19_vaccination_total.json"
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


@retry(stop=stop_after_attempt(10), wait=wait_exponential(min=2, max=30))
def download_json_data(url, dst):
    logger.info("Downloading {url} to {dst}", url=url, dst=dst)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dst, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


@retry(stop=stop_after_attempt(10), wait=wait_exponential(min=2, max=30))
def scrape_deaths():
    # Load content from Terviset's Covid dashboard and parse it
    logger.info("Scraping data on deaths from {url}", url=TERVISEAMET_COVID_DASHBOARD)
    html = requests.get(TERVISEAMET_COVID_DASHBOARD).text
    soup = BeautifulSoup(html, "html.parser")

    # Extract number of deaths from page content and update JSON data on deaths
    deaths_container = soup.select(DEATHS_SELECTOR)
    if len(deaths_container) > 0:
        # Get number of deaths and the current date
        deaths_count = int(deaths_container[0].text.strip())
        current_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        # Load existing deaths data
        previous_deaths = read_json_from_file(DEATHS_PATH)

        # Add new entry to deaths data for current date
        deaths = {}
        if len(previous_deaths):
            deaths = previous_deaths
        deaths[current_date] = deaths_count

        # Save data on deaths
        save_as_json(DEATHS_PATH + ".tmp", deaths)

        # Log status
        logger.info(
            "Successfully scraped deaths. Total deaths: {deaths}", deaths=deaths_count
        )
    else:
        # Log error
        raise Exception("Error: could not find page element with data on deaths")


@analyze_time
@analyze_memory
def main():
    scrape_deaths()

    # Load data from external services
    logger.info("Downloading data from TEHIK: Test results")
    download_json_data(TESTING_ENDPOINT, TEST_RESULTS_PATH + ".tmp")

    logger.info("Downloading data from TEHIK: Location data")
    download_json_data(TEST_LOCATION_ENDPOINT, TEST_LOCATIONS_PATH + ".tmp")

    logger.info("Downloading data from TEHIK: Hospitalization data")
    download_json_data(HOSPITALIZATION_ENDPOINT, HOSPITALIZATION_PATH + ".tmp")

    logger.info("Downloading data from TEHIK: Vaccination data")
    download_json_data(VACCINATION_ENDPOINT, VACCINATIONS_PATH + ".tmp")

    # Validate data from remote endpoints
    hospitalization = read_json_from_file(HOSPITALIZATION_PATH + ".tmp")
    if not is_up_to_date(hospitalization, "LastLoadStatisticsDate"):
        raise Exception("Hospitalization data is not up-to-date")

    logger.info("All ok, replacing old files with downloaded files")
    move(DEATHS_PATH + ".tmp", DEATHS_PATH)
    move(TEST_RESULTS_PATH + ".tmp", TEST_RESULTS_PATH)
    move(TEST_LOCATIONS_PATH + ".tmp", TEST_LOCATIONS_PATH)
    move(HOSPITALIZATION_PATH + ".tmp", HOSPITALIZATION_PATH)
    move(VACCINATIONS_PATH + ".tmp", VACCINATIONS_PATH)
