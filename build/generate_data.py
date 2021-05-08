from datetime import datetime
from datetime import timedelta

from build.chart_data_functions import get_confirmed_cases_by_county
from build.chart_data_functions import get_county_by_day
from build.chart_data_functions import get_county_daily_active
from build.chart_data_functions import get_cumulative_cases_chart_data
from build.chart_data_functions import get_cumulative_tests_chart_data
from build.chart_data_functions import get_hospital_data
from build.chart_data_functions import get_in_intensive_data
from build.chart_data_functions import get_infection_count_by_county
from build.chart_data_functions import get_infections_data_by_count_10000
from build.chart_data_functions import get_municipality_data
from build.chart_data_functions import get_new_cases_per_day_chart_data
from build.chart_data_functions import get_on_ventilation_data
from build.chart_data_functions import get_positive_negative_chart_data
from build.chart_data_functions import get_positive_tests_by_age_chart_data
from build.chart_data_functions import get_test_data_pop_ratio
from build.chart_data_functions import get_tests_per_day_chart_data
from build.chart_data_functions import get_vaccinated_people_chart_data
from build.constants import AGE_GROUPS
from build.constants import COUNTIES_INCL_UNKNOWN
from build.constants import COUNTY_MAPPING
from build.constants import COUNTY_POPULATION
from build.constants import DEATHS_PATH
from build.constants import HOSPITALIZATION_PATH
from build.constants import MANUAL_DATA_PATH
from build.constants import OUTPUT_PATH
from build.constants import TEST_LOCATIONS_PATH
from build.constants import TEST_RESULTS_PATH
from build.constants import VACCINATIONS_PATH
from build.utils import logger
from build.utils import read_json_from_file
from build.utils import save_as_json
import numpy as np
import pandas as pd
import pytz

ESTONIA_TZ = pytz.timezone("Europe/Helsinki")
TODAY_DMYHM = datetime.today().astimezone(ESTONIA_TZ).strftime("%d/%m/%Y, %H:%M")
YESTERDAY_YMD = datetime.strftime(datetime.today() - timedelta(1), "%Y-%m-%d")

######## CONFIGURATION SETTINGS ########

DATE_SETTINGS = {
    # "dates1_start": "2020-03-15", # TODO: It's unclear what this date relates to. Remove? Commented out for now.
    "dates2_start": "2020-02-26",  # The date of the first Covid-19 case in Estonia. Most charts start from this date.
    "dates3_start": "2020-12-26",  # Vaccination started in Estonia on 27 December 2020. Time series charts related
    # to vaccination start one day earlier.
}


def main():
    # Log status
    logger.info("Starting data update process")

    test_results = read_json_from_file(TEST_RESULTS_PATH)
    test_locations = read_json_from_file(TEST_LOCATIONS_PATH)
    hospitalization = read_json_from_file(HOSPITALIZATION_PATH)
    vaccination = read_json_from_file(VACCINATIONS_PATH)

    # Load locally-stored data
    logger.info("Loading local data files")
    deaths = read_json_from_file(DEATHS_PATH)
    manual_data = read_json_from_file(MANUAL_DATA_PATH)

    # Log status
    logger.info("Calculating main statistics")

    # Statsbar
    # Find count of confirmed cases
    n_confirmed_cases = np.sum([res["ResultValue"] == "P" for res in test_results])

    # Find total number of tests
    n_tests_administered = len(test_results)

    # Create date ranges for charts
    # dates1 = pd.date_range(start=DATE_SETTINGS["dates1_start"], end=yesterday)
    dates2 = pd.date_range(start=DATE_SETTINGS["dates2_start"], end=YESTERDAY_YMD)
    dates3 = pd.date_range(start=DATE_SETTINGS["dates3_start"], end=YESTERDAY_YMD)

    # Set recovered, deceased, hospitalised and ICU time-series
    hospital = get_hospital_data(hospitalization, DATE_SETTINGS["dates2_start"])
    recovered = hospital["discharged"]
    manual_data["deceased"].update(deaths)
    deceased = list(manual_data["deceased"].values())
    hospitalised = hospital["activehospitalizations"]
    # TODO: Based on cross-checking with the hospitalization data publishedby TEHIK, the data listed
    #       in the manual_data.json file with the field name "intensive" appears to show the number
    #       of patients on ventilation. We should fix the terminology and make sure that the intensive
    #       and on ventilation statistics are being calculated correctly.
    intensive = list(
        get_in_intensive_data(hospitalization, manual_data["intensive"]).values()
    )
    on_ventilation = list(get_on_ventilation_data(hospitalization).values())

    n_deaths = deceased[-1]
    n_deaths_change = int(deceased[-1]) - int(deceased[-2])

    # Get data for each chart
    logger.info("Calculating data for charts")
    infections_by_county = get_infection_count_by_county(test_results, COUNTY_MAPPING)
    infections_by_county_10000 = get_infections_data_by_count_10000(
        infections_by_county, COUNTY_POPULATION
    )
    tests_pop_ratio = get_test_data_pop_ratio(infections_by_county_10000)
    county_by_day = get_county_by_day(
        test_results, dates2, COUNTY_MAPPING, COUNTY_POPULATION
    )
    confirmed_cases_by_county = get_confirmed_cases_by_county(
        test_results, COUNTY_MAPPING
    )
    cumulative_cases_chart_data = get_cumulative_cases_chart_data(
        test_results,
        recovered,
        deceased,
        hospitalised,
        intensive,
        on_ventilation,
        dates2,
    )
    new_cases_per_day_chart_data = get_new_cases_per_day_chart_data(
        cumulative_cases_chart_data
    )
    cumulative_tests_chart_data = get_cumulative_tests_chart_data(test_results, dates2)
    tests_per_day_chart_data = get_tests_per_day_chart_data(test_results, dates2)
    positive_test_by_age_chart_data = get_positive_tests_by_age_chart_data(test_results)
    positive_negative_chart_data = get_positive_negative_chart_data(
        test_results, COUNTY_MAPPING
    )
    vaccinated_people_chart_data = get_vaccinated_people_chart_data(vaccination, dates3)
    county_daily_active = get_county_daily_active(
        test_results, dates2, COUNTY_MAPPING, COUNTY_POPULATION
    )
    n_active_cases = cumulative_cases_chart_data["active"][-1]
    n_active_cases_change = (
        cumulative_cases_chart_data["active"][-1]
        - cumulative_cases_chart_data["active"][-2]
    )
    active_infections_by_county = [
        {"MNIMI": k, "sequence": v, "drilldown": k}
        for k, v in county_daily_active["countyByDayActive"].items()
    ]
    active_infections_by_county_100k = [
        [k, round(v[-1] / COUNTY_POPULATION[k] * 100000, 2)]
        for k, v in county_daily_active["countyByDayActive"].items()
    ]
    municipalities_data = get_municipality_data(test_locations, COUNTY_MAPPING)
    per_100k = cumulative_cases_chart_data["active100k"][-1]

    # Calculate vaccination data
    logger.info("Calculating vaccination data")
    last_day_vaccination_data = [
        x for x in vaccination if x["MeasurementType"] == "Vaccinated"
    ][-1]
    last_day_completed_vaccination_data = [
        x for x in vaccination if x["MeasurementType"] == "FullyVaccinated"
    ][-1]
    # TODO: Doses administered
    # last_day_doses_administered_data = [x for x in json_vaccination if x['MeasurementType'] == 'DosesAdministered'][-1]
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
    fully_vaccinated_from_total_vaccinated_percentage = round(
        completed_vaccination_number_total * 100 / (all_vaccination_number_total), 2
    )

    # Create dictionary for final JSON
    logger.info("Compiling final JSON")
    final_json = {
        "updatedOn": TODAY_DMYHM,
        "confirmedCasesNumber": str(n_confirmed_cases),
        # TODO: For consistency, we should include the change in the number of confirmed cases as well.
        "hospitalisedNumber": str(hospital["activehospitalizations"][-1]),
        "hospitalChanged": str(
            hospital["activehospitalizations"][-1]
            - hospital["activehospitalizations"][-2]
        ),
        "deceasedNumber": str(n_deaths),
        "deceasedChanged": str(n_deaths_change),
        "recoveredNumber": str(hospital["discharged"][-1]),
        "recoveredChanged": str(
            hospital["discharged"][-1] - hospital["discharged"][-2]
        ),
        "testsAdministeredNumber": str(n_tests_administered),
        # TODO: For consistency, we should include the change in the number of tests as well.
        "activeCasesNumber": str(n_active_cases),
        "activeChanged": str(n_active_cases_change),
        "perHundred": str(per_100k),  # TODO: This should be given a clearer name.
        # TODO: I can't find anywhere in the app where "dates1" is used. Is it needed? Commented out for now.
        # "dates1": [str(x.date()) for x in dates1],
        "dates2": [str(x.date()) for x in dates2],
        "dates3": [str(x.date()) for x in dates3],
        "counties": COUNTIES_INCL_UNKNOWN,
        "age_groups": AGE_GROUPS,
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
        "hospital": hospital,  # TODO: Rename this to make it clearer what data it contains.
        "vaccinationNumberTotal": vaccination_number_total,
        "vaccinationNumberLastDay": vaccination_number_last_day,
        "completedVaccinationNumberTotal": completed_vaccination_number_total,
        "completedVaccinationNumberLastDay": completed_vaccination_number_last_day,
        "allVaccinationNumberTotal": all_vaccination_number_total,
        "allVaccinationNumberLastDay": all_vaccination_number_last_day,
        "allVaccinationFromPopulationPercentage": last_day_vaccination_data[
            "PopulationCoverage"
        ],
        "completelyVaccinatedFromTotalVaccinatedPercentage": fully_vaccinated_from_total_vaccinated_percentage,
    }

    # Dump JSON output
    save_as_json(OUTPUT_PATH, final_json)

    # Log finish time
    logger.info("Finished update process")


if __name__ == "__main__":
    main()
