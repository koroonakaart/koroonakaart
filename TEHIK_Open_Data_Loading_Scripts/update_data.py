from datetime import timezone
from time import sleep
import traceback

import pytz
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse as parsedate

from chart_data_functions import *
from constants import age_groups
from constants import counties
from constants import county_mapping
from constants import county_sizes
from utils import log_status
from utils import read_json_from_file
from utils import save_as_json


estonian_timezone = pytz.timezone("Europe/Helsinki")
today = datetime.today().astimezone(estonian_timezone).strftime("%d/%m/%Y, %H:%M")
yesterday = datetime.strftime(datetime.today() - timedelta(1), "%Y-%m-%d")


######## CONFIGURATION SETTINGS ########

DATE_SETTINGS = {
    "dates1_start": "2020-03-15", # TODO: It's unclear what this date relates to. Remove?
    "dates2_start": "2020-02-26", # The date of the first Covid-19 case in Estonia. Most charts start from this date.
    "dates3_start": "2020-12-26", # Vaccination started in Estonia on 27 December 2020. Time series charts related
                                  # to vaccination start one day earlier.
}

######## CONFIGURE IO LOCATIONS ########

TESTING_ENDPOINT = "https://opendata.digilugu.ee/opendata_covid19_test_results.json"
TEST_LOCATION_ENDPOINT = "https://opendata.digilugu.ee/opendata_covid19_test_location.json"
HOSPITALISATION_ENDPOINT = "https://opendata.digilugu.ee/opendata_covid19_hospitalization_timeline.json"
VACCINATION_ENDPOINT = "https://opendata.digilugu.ee/covid19/vaccination/v2/opendata_covid19_vaccination_total.json"
TERVISEAMET_COVID_DASHBOARD = "https://www.terviseamet.ee/et/koroonaviirus/koroonakaart"
MANUAL_DATA_FILE_LOCATION = "../data/manual_data.json"
DEATHS_FILE_LOCATION = "../data/deaths.json"
OUTPUT_FILE_LOCATION = "../data/data.json"


def get_json_data(url):
    max_retries = 3
    for retry in range(1, max_retries + 1):
        try:
            # Request remote data
            response = requests.get(url=url)

            # Process response
            if response.status_code == 200:
                return response.json()
            else:
                log_status('Endpoint unavailable. Status code: ' + str(response.status_code))
        except:
            # Log error
            log_status('Error when retrieving remote data:')
            log_status(traceback.format_exc())

        # Retry?
        if retry < max_retries:
            log_status("Retrying...")
            sleep(5)

    # Unable to get remote data
    return None


def is_up_to_date(json_data, date_field_name):
    yesterday = datetime.today() - timedelta(1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    file_date_time = datetime.strptime(json_data[0][date_field_name].split("T")[0], "%Y-%m-%d")
    if file_date_time >= yesterday:
        return True
    return False


# def is_header_last_modified_up_to_date(url):
#     url_date = parsedate(requests.head(url).headers["Last-Modified"])
#     today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
#     if url_date > today:
#         return True
#     return False


def main():
    # Log status
    log_status("Starting data update process at " + str(today))

    # Get current number of deaths from Terviseamet's Covid dashboard
    try:
        scrape_deaths()
    except:
        log_status("Aborting data update.")
        exit()

    # Load data from external services
    log_status("Downloading data from TEHIK: Test results")
    json_testing = get_json_data(TESTING_ENDPOINT)
    log_status("Downloading data from TEHIK: Location data")
    json_test_location = get_json_data(TEST_LOCATION_ENDPOINT)
    log_status("Downloading data from TEHIK: Hospitalisation data")
    json_hospitalisation = get_json_data(HOSPITALISATION_ENDPOINT)
    log_status("Downloading data from TEHIK: Vaccination data")
    json_vaccination = get_json_data(VACCINATION_ENDPOINT)

    # Validate data from remote endpoints
    # TODO: Add checks that the testing and vaccination data are up to date. We will need to adopt
    #       a different approach than for the test location and hospitalisation data due to the fact
    #       that the data structure of the JSON is different. Checking the "Last-Modified" header of the
    #       response may be the way to go and would handle the possibility that there are no tests or
    #       vaccinations on a particular day.
    ok = True
    if json_testing is None:
        log_status("Unable to retrieve testing data")
        ok = False
    if json_test_location is None:
        log_status("Unable to retrieve location data")
        ok = False
    elif not is_up_to_date(json_test_location, "LastStatisticsDate"):
        log_status("Location data is not up-to-date")
        ok = False
    if json_hospitalisation is None:
        log_status("Unable to retrieve hospitalisation data")
        ok = False
    elif not is_up_to_date(json_hospitalisation, "LastLoadStatisticsDate"):
        log_status("Hospitalisation data is not up-to-date")
        ok = False
    if json_vaccination is None:
        log_status("Unable to retrieve vaccination data")
        ok = False
    # TODO: Review whether this check is needed. I have commented it out for now.
    # if not is_header_last_modified_up_to_date(TEST_LOCATION_ENDPOINT):
    #     log_status("Location data last modified is not up-to-date")
    #     ok = False

    if not ok:
        log_status("One or more of the TEHIK APIs has not been updated or could not be retrieved.")
        log_status("Aborting data update.")
        exit()

    # Load locally-stored data
    log_status("Loading local data files")
    try:
        json_deaths = read_json_from_file(DEATHS_FILE_LOCATION)
        json_manual = read_json_from_file(MANUAL_DATA_FILE_LOCATION)
    except:
        # Log error
        log_status('Error when loading local data:')
        log_status(traceback.format_exc())
        exit()

    # Log status
    log_status("Calculating main statistics")

    # Statsbar
    # Find count of confirmed cases
    n_confirmed_cases = np.sum([res["ResultValue"] == "P" for res in json_testing])

    # Find total number of tests
    n_tests_administered = len(json_testing)

    # Create date ranges for charts
    dates1 = pd.date_range(start=DATE_SETTINGS["dates1_start"], end=yesterday)
    dates2 = pd.date_range(start=DATE_SETTINGS["dates2_start"], end=yesterday)
    dates3 = pd.date_range(start=DATE_SETTINGS["dates3_start"], end=yesterday)

    # Set recovered, deceased, hospitalised and ICU time-series
    hospital = get_hospital_data(json_hospitalisation, DATE_SETTINGS["dates2_start"])
    recovered = hospital["discharged"]
    json_manual["deceased"].update(json_deaths)
    deceased = list(json_manual["deceased"].values())
    hospitalised = hospital["activehospitalizations"]
    intensive = list(get_in_intensive_data(json_hospitalisation, json_manual["intensive"]).values())
    on_ventilation = list(get_on_ventilation_data(json_hospitalisation).values())

    n_deaths = deceased[-1]
    n_deaths_change = int(deceased[-1]) - int(deceased[-2])

    # Get data for each chart
    log_status("Calculating data for charts")
    infections_by_county = get_infection_count_by_county(json_testing, county_mapping)
    infections_by_county_10000 = get_infections_data_by_count_10000(infections_by_county, county_sizes)
    tests_pop_ratio = get_test_data_pop_ratio(infections_by_county_10000)
    county_by_day = get_county_by_day(json_testing, dates2, county_mapping, county_sizes)
    confirmed_cases_by_county = get_confirmed_cases_by_county(json_testing, county_mapping)
    cumulative_cases_chart_data = get_cumulative_cases_chart_data(
        json_testing, recovered, deceased, hospitalised, intensive, on_ventilation, dates2
    )
    new_cases_per_day_chart_data = get_new_cases_per_day_chart_data(cumulative_cases_chart_data)
    cumulative_tests_chart_data = get_cumulative_tests_chart_data(json_testing, dates2)
    tests_per_day_chart_data = get_tests_per_day_chart_data(json_testing, dates2)
    positive_test_by_age_chart_data = get_positive_tests_by_age_chart_data(json_testing)
    positive_negative_chart_data = get_positive_negative_chart_data(json_testing, county_mapping)
    vaccinated_people_chart_data = get_vaccinated_people_chart_data(json_vaccination, dates3)
    county_daily_active = get_county_daily_active(json_testing, dates2, county_mapping, county_sizes)
    n_active_cases = cumulative_cases_chart_data["active"][-1]
    n_active_cases_change = (cumulative_cases_chart_data["active"][-1] - cumulative_cases_chart_data["active"][-2])
    active_infections_by_county = [
        {"MNIMI": k, "sequence": v, "drilldown": k}
        for k, v in county_daily_active["countyByDayActive"].items()
    ]
    active_infections_by_county_100k = [
        [k, round(v[-1] / county_sizes[k] * 100000, 2)]
        for k, v in county_daily_active["countyByDayActive"].items()
    ]
    municipalities_data = get_municipality_data(json_test_location, county_mapping)
    per_100k = cumulative_cases_chart_data["active100k"][-1]

    # Calculate vaccination data
    log_status("Calculating vaccination data")
    last_day_vaccination_data = [x for x in json_vaccination if x["MeasurementType"] == "Vaccinated"][-1]
    last_day_completed_vaccination_data = [x for x in json_vaccination if x["MeasurementType"] == "FullyVaccinated"][-1]
    # TODO: Doses administered
    # last_day_doses_administered_data = [x for x in json_vaccination if x['MeasurementType'] == 'DosesAdministered'][-1]
    completed_vaccination_number_total = last_day_completed_vaccination_data["TotalCount"]
    completed_vaccination_number_last_day = last_day_completed_vaccination_data["DailyCount"]
    all_vaccination_number_total = last_day_vaccination_data["TotalCount"]
    all_vaccination_number_last_day = last_day_vaccination_data["DailyCount"]
    vaccination_number_total = (all_vaccination_number_total - completed_vaccination_number_total)
    vaccination_number_last_day = (all_vaccination_number_last_day - completed_vaccination_number_last_day)
    fully_vaccinated_from_total_vaccinated_percentage = round(
        completed_vaccination_number_total * 100 / (all_vaccination_number_total), 2
    )

    # Create dictionary for final JSON
    log_status("Compiling final JSON")
    final_json = {
        "updatedOn": today,
        "confirmedCasesNumber": str(n_confirmed_cases),
        # TODO: For consistentcy, we should calculate the change in the number of confirmed cases as well.
        "hospitalisedNumber": str(hospital["activehospitalizations"][-1]),
        "hospitalChanged": str(hospital["activehospitalizations"][-1] - hospital["activehospitalizations"][-2]),
        "deceasedNumber": str(n_deaths),
        "deceasedChanged": str(n_deaths_change),
        "recoveredNumber": str(hospital["discharged"][-1]),
        "recoveredChanged": str(hospital["discharged"][-1] - hospital["discharged"][-2]),
        "testsAdministeredNumber": str(n_tests_administered),
        # TODO: For consistentcy, we should calculate the change in the number of tests as well.
        "activeCasesNumber": str(n_active_cases),
        "activeChanged": str(n_active_cases_change),
        "perHundred": str(per_100k), # TODO: What per hundred? This should be given a better name.
        # TODO: I can't find anywhere in the app where "dates1" is used. Is it needed?
        "dates1": [str(x.date()) for x in dates1],
        "dates2": [str(x.date()) for x in dates2],
        "dates3": [str(x.date()) for x in dates3],
        "counties": counties,
        "age_groups": age_groups,
        "dataInfectionsByCounty": infections_by_county,
        "dataInfectionsByCounty10000": infections_by_county_10000,
        "dataActiveInfectionsByCounty100k": active_infections_by_county_100k,
        "dataActiveInfectionsByCounty": active_infections_by_county,
        "dataTestsPopRatio": tests_pop_ratio,
        "countyByDay": county_by_day,
        "dataCountyDailyActive": county_daily_active,
        "dataConfirmedCasesByCounties": confirmed_cases_by_county,
        "dataCumulativeCasesChart": cumulative_cases_chart_data,
        "dataNewCasesPerDayChart": new_cases_per_day_chart_data,
        "dataCumulativeTestsChart": cumulative_tests_chart_data,
        "dataTestsPerDayChart": tests_per_day_chart_data,
        "dataPositiveTestsByAgeChart": positive_test_by_age_chart_data,
        "dataPositiveNegativeChart": positive_negative_chart_data,
        "dataVaccinatedPeopleChart": vaccinated_people_chart_data,
        "dataMunicipalities": municipalities_data,
        "hospital": hospital,
        "vaccinationNumberTotal": vaccination_number_total,
        "vaccinationNumberLastDay": vaccination_number_last_day,
        "completedVaccinationNumberTotal": completed_vaccination_number_total,
        "completedVaccinationNumberLastDay": completed_vaccination_number_last_day,
        "allVaccinationNumberTotal": all_vaccination_number_total,
        "allVaccinationNumberLastDay": all_vaccination_number_last_day,
        "allVaccinationFromPopulationPercentage": last_day_vaccination_data["PopulationCoverage"],
        "completelyVaccinatedFromTotalVaccinatedPercentage": fully_vaccinated_from_total_vaccinated_percentage,
    }

    # Dump JSON output
    log_status("Dumping JSON output")
    save_as_json(OUTPUT_FILE_LOCATION, final_json)

    # Log finish time
    finish = datetime.today().astimezone(estonian_timezone).strftime("%d/%m/%Y, %H:%M")
    log_status("Finished update process at " + finish)


def scrape_deaths():
    # Load content from Terviset's Covid dashboard and parse it
    log_status("Scraping data on deaths from " + TERVISEAMET_COVID_DASHBOARD)
    html = requests.get(TERVISEAMET_COVID_DASHBOARD).text
    soup = BeautifulSoup(html, "html.parser")

    # Extract number of deaths from page content and update JSON data on deaths
    deaths_container = soup.select(".node-lead-default strong")
    if len(deaths_container) > 0:
        try:
            # Get number of deaths and the current date
            deaths_count = int(deaths_container[0].text.strip())
            current_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

            # Load existing deaths data
            json_deaths = read_json_from_file(DEATHS_FILE_LOCATION)

            # Add new entry to deaths data for current date
            deaths_output = {}
            if len(json_deaths):
                deaths_output = json_deaths
            deaths_output[current_date] = deaths_count

            # Save data on deaths
            save_as_json(DEATHS_FILE_LOCATION, deaths_output)

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


if __name__ == "__main__":
    main()

