from datetime import timezone
from time import sleep

from chart_data_functions import *
from constants import age_groups
from constants import counties
from constants import county_mapping
from constants import county_sizes
from dateutil.parser import parse as parsedate
import pytz
import requests
from utils import log_status
from utils import read_json_from_file
from utils import save_as_json

estonian_timezone = pytz.timezone("Europe/Helsinki")
today = datetime.today().astimezone(estonian_timezone).strftime("%d/%m/%Y, %H:%M")
yesterday = datetime.strftime(datetime.today() - timedelta(1), "%Y-%m-%d")

######## CONFIGURE MANUAL DATA ########

MANUAL_DATA = {
    "updatedOn": today,
    "deceasedNumber": 125,
    "datesEnd": yesterday,
    "dates1Start": "2020-03-15",
    "dates2Start": "2020-02-26",
    "dates3Start": "2020-12-26",
}

######## CONFIGURE IO LOCATIONS ########

API_ENDPOINT = "https://opendata.digilugu.ee/opendata_covid19_test_results.json"
MUNICIPALITIES_ENDPOINT = (
    "https://opendata.digilugu.ee/opendata_covid19_test_location.json"
)
HOSPITAL_ENDPOINT = (
    "https://opendata.digilugu.ee/opendata_covid19_hospitalization_timeline.json"
)
VACCINE_ENDPOINT = "https://opendata.digilugu.ee/covid19/vaccination/v2/opendata_covid19_vaccination_total.json"
MANUAL_DATA_FILE_LOCATION = "../data/manual_data.json"
DEATHS_FILE_LOCATION = "../data/deaths.json"
OUTPUT_FILE_LOCATION = "../data/data.json"


def get_json_data(url) -> any:
    # Open data endpoint
    r = requests.get(url=url)
    return r.json()


def is_up_to_date(dictionary, key):
    yesterday = datetime.today() - timedelta(1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    file_date_time = datetime.strptime(dictionary[0][key].split("T")[0], "%Y-%m-%d")
    if file_date_time >= yesterday:
        return True
    return False


def is_header_last_modified_up_to_date(url):
    url_date = parsedate(requests.head(url).headers["Last-Modified"])
    today = datetime.utcnow().replace(
        hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc
    )
    if url_date > today:
        return True
    return False


if __name__ == "__main__":
    # Log status
    log_status("Starting data update process at " + str(today))

    # Load the data from external services
    max_retries = 15
    for retry in range(1, max_retries + 1):
        log_status("Downloading data from TEHIK: Test results")
        json_data = get_json_data(API_ENDPOINT)
        log_status("Downloading data from TEHIK: Location data")
        municipalities = get_json_data(MUNICIPALITIES_ENDPOINT)
        log_status("Downloading data from TEHIK: Hospitalisation data")
        json_hospital = get_json_data(HOSPITAL_ENDPOINT)
        log_status("Downloading data from TEHIK: Vaccination data")
        json_vaccine = get_json_data(VACCINE_ENDPOINT)
        log_status("Loading local data files")
        json_deaths = read_json_from_file(DEATHS_FILE_LOCATION)
        json_manual = read_json_from_file(MANUAL_DATA_FILE_LOCATION)

        ok = True

        if not is_up_to_date(municipalities, "LastStatisticsDate"):
            log_status("Location data is not up-to-date")
            ok = False

        if not is_up_to_date(json_hospital, "LastLoadStatisticsDate"):
            log_status("Hospitalization data is not up-to-date")
            ok = False

        if not is_header_last_modified_up_to_date(MUNICIPALITIES_ENDPOINT):
            log_status("Location data last modified is not up-to-date")
            ok = False

        if not ok:
            log_status("One or more of the TEHIK APIs has not been updated.")

            if retry >= max_retries:
                exit()
            else:
                log_status("Retrying...")
                sleep(5)
        else:
            # Everything up-to-date
            break

    # Log status
    log_status("Calculating main statistics")

    # Date of update
    updated_on = MANUAL_DATA["updatedOn"]

    # Statsbar
    # Find count of confirmed cases
    confirmed_cases_number = np.sum([res["ResultValue"] == "P" for res in json_data])

    # Find total number of tests
    tests_administered_number = len(json_data)

    # Calculate active number of cases

    # Set date ranges
    dates_range_end = MANUAL_DATA["datesEnd"]

    dates1_range_start = MANUAL_DATA["dates1Start"]
    dates1_range_end = dates_range_end

    dates2_range_start = MANUAL_DATA["dates2Start"]
    dates2_range_end = dates_range_end

    dates3_range_start = MANUAL_DATA["dates3Start"]
    dates3_range_end = dates_range_end

    # Create date ranges for charts
    dates1 = pd.date_range(start=dates1_range_start, end=dates1_range_end)
    dates2 = pd.date_range(start=dates2_range_start, end=dates2_range_end)
    dates3 = pd.date_range(start=dates3_range_start, end=dates3_range_end)

    # Create copy
    json_copy = json_data
    municipalities_copy = municipalities
    hospital_copy = json_hospital
    hospital = get_hospital_data(hospital_copy, dates2_range_start)

    # Set recovered, deceased, hospitalised and ICU time-series
    recovered = hospital["discharged"]
    json_manual["deceased"].update(json_deaths)
    deceased = list(json_manual["deceased"].values())
    hospitalised = hospital["activehospitalizations"]
    intensive = list(
        get_in_intensive_data(json_hospital, json_manual["intensive"]).values()
    )
    on_ventilation = list(get_on_ventilation_data(json_hospital).values())

    deceased_number = deceased[-1]
    deceased_changed = int(deceased[-1]) - int(deceased[-2])

    # Get data for each chart
    log_status("Calculating data for charts")
    infections_by_county = get_infection_count_by_county(json_copy, county_mapping)
    infections_by_county_10000 = get_infections_data_by_count_10000(
        infections_by_county, county_sizes
    )
    tests_pop_ratio = get_test_data_pop_ratio(infections_by_county_10000)
    county_by_day = get_county_by_day(json_copy, dates2, county_mapping, county_sizes)
    confirmed_cases_by_county = get_confirmed_cases_by_county(json_copy, county_mapping)
    cumulative_cases_chart_data = get_cumulative_cases_chart_data(
        json_copy, recovered, deceased, hospitalised, intensive, on_ventilation, dates2
    )
    new_cases_per_day_chart_data = get_new_cases_per_day_chart_data(
        cumulative_cases_chart_data
    )
    cumulative_tests_chart_data = get_cumulative_tests_chart_data(json_copy, dates2)
    tests_per_day_chart_data = get_tests_per_day_chart_data(json_copy, dates2)
    positive_test_by_age_chart_data = get_positive_tests_by_age_chart_data(json_copy)
    positive_negative_chart_data = get_positive_negative_chart_data(
        json_copy, county_mapping
    )
    vaccinated_people_chart_data = get_vaccinated_people_chart_data(
        json_vaccine, dates3
    )
    county_daily_active = get_county_daily_active(
        json_copy, dates2, county_mapping, county_sizes
    )
    active_cases_number = cumulative_cases_chart_data["active"][-1]
    active_changed = (
        cumulative_cases_chart_data["active"][-1]
        - cumulative_cases_chart_data["active"][-2]
    )
    active_infections_by_county = [
        {"MNIMI": k, "sequence": v, "drilldown": k}
        for k, v in county_daily_active["countyByDayActive"].items()
    ]
    active_infections_by_county_100k = [
        [k, round(v[-1] / county_sizes[k] * 100000, 2)]
        for k, v in county_daily_active["countyByDayActive"].items()
    ]
    municipalities_data = get_municipality_data(municipalities_copy, county_mapping)
    per_100k = cumulative_cases_chart_data["active100k"][-1]

    # Calculate vaccination data
    log_status("Calculating vaccination data")
    last_day_vaccination_data = [
        x for x in json_vaccine if x["MeasurementType"] == "Vaccinated"
    ][-1]
    last_day_completed_vaccination_data = [
        x for x in json_vaccine if x["MeasurementType"] == "FullyVaccinated"
    ][-1]
    # TODO: Doses administered
    # lastDayDosesAdministeredData = [x for x in json_vaccine if x['MeasurementType'] == 'DosesAdministered'][-1]
    completed_vaccination_number_total = last_day_completed_vaccination_data[
        "TotalCount"
    ]
    completed_vaccination_number_last_day = last_day_completed_vaccination_data[
        "DailyCount"
    ]
    all_vaccination_number_total = last_day_vaccination_data["TotalCount"]
    all_vaccination_number_last_day = last_day_vaccination_data["DailyCount"]
    vaccination_number_total = (
        all_vaccination_number_total - completed_vaccination_number_total
    )
    vaccination_number_last_day = (
        all_vaccination_number_last_day - completed_vaccination_number_last_day
    )
    completely_vaccinated_from_total_vaccinated_percentage = round(
        completed_vaccination_number_total * 100 / (all_vaccination_number_total), 2
    )

    # Create dictionary for final JSON
    log_status("Compiling final JSON")
    final_json = {
        "updatedOn": updated_on,
        "confirmedCasesNumber": str(confirmed_cases_number),
        "activeCasesNumber": str(active_cases_number),
        "perHundred": str(per_100k),
        "hospitalisedNumber": str(hospital["activehospitalizations"][-1]),
        "deceasedNumber": str(deceased_number),
        "recoveredNumber": str(hospital["discharged"][-1]),
        "testsAdministeredNumber": str(tests_administered_number),
        "hospitalChanged": str(
            hospital["activehospitalizations"][-1]
            - hospital["activehospitalizations"][-2]
        ),
        "deceasedChanged": str(deceased_changed),
        "recoveredChanged": str(
            hospital["discharged"][-1] - hospital["discharged"][-2]
        ),
        "activeChanged": str(active_changed),
        "dates1": list(map(lambda x: str(x.date()), dates1)),
        "dates2": list(map(lambda x: str(x.date()), dates2)),
        "dates3": list(map(lambda x: str(x.date()), dates3)),
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
        "allVaccinationFromPopulationPercentage": last_day_vaccination_data[
            "PopulationCoverage"
        ],
        "completelyVaccinatedFromTotalVaccinatedPercentage": completely_vaccinated_from_total_vaccinated_percentage,
    }

    # Dump JSON output
    log_status("Dumping JSON output")
    save_as_json(OUTPUT_FILE_LOCATION, final_json)

    # Log finish time
    finish = datetime.today().astimezone(estonian_timezone).strftime("%d/%m/%Y, %H:%M")
    log_status("Finished update process at " + finish)
