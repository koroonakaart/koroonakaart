from datetime import timezone
from time import sleep
import traceback

import pytz
import requests
from dateutil.parser import parse as parsedate

from chart_data_functions import *
from constants import MANUAL_DATA_PATH
from constants import DEATHS_PATH
from constants import HOSPITALIZATION_PATH
from constants import TEST_LOCATIONS_PATH
from constants import TEST_RESULTS_PATH
from constants import VACCINATIONS_PATH
from constants import OUTPUT_FILE_LOCATION
from constants import age_groups
from constants import counties
from constants import county_mapping
from constants import county_sizes
from utils import log_status
from utils import read_json_from_file
from utils import get_json_from_csv_file
from utils import save_as_json


ESTONIA_TIMEZONE = pytz.timezone("Europe/Helsinki")
TODAY_DMYHM = datetime.today().astimezone(ESTONIA_TIMEZONE).strftime("%d/%m/%Y, %H:%M")
YESTERDAY_YMD = datetime.strftime(datetime.today() - timedelta(1), "%Y-%m-%d")


######## CONFIGURATION SETTINGS ########

DATE_SETTINGS = {
    # The date of the first Covid-19 case in Estonia. Most charts start from this date.
    "first_case_date": "2020-02-26",
    # Vaccination started in Estonia on 27 December 2020. Time series charts related
    # to vaccination start one day earlier.
    "vaccination_start_date": "2020-12-26",
}


def main():
    # Log status
    log_status("Starting to generate chart data at " + str(TODAY_DMYHM))


    # 1.  Create date ranges for charts

    log_status("Creating date ranges for charts")
    case_dates = pd.date_range(start=DATE_SETTINGS["first_case_date"], end=YESTERDAY_YMD)
    vaccination_dates = pd.date_range(start=DATE_SETTINGS["vaccination_start_date"], end=YESTERDAY_YMD)


    # 2.  Calculate data related to deaths

    try:
        deaths = read_json_from_file(DEATHS_PATH)
        manual_data = read_json_from_file(MANUAL_DATA_PATH)
    except:
        # Log error
        log_status('Error when loading local data:')
        log_status(traceback.format_exc())
        exit()

    log_status("Calculating data related to deaths")

    manual_data["deceased"].update(deaths)
    deceased = list(manual_data["deceased"].values())
    n_deaths = deceased[-1]
    n_deaths_change = int(deceased[-1]) - int(deceased[-2])


    # 3.  Calculate data related to test results

    # Define columns to import
    column_list = [
        'Gender',
        'AgeGroup',
        'County',
        'ResultValue',
        'StatisticsDate'
    ]

    test_results = get_json_from_csv_file(TEST_RESULTS_PATH, column_list)
    
    log_status("Calculating data related to test results")

    # Find count of confirmed cases
    n_confirmed_cases = np.sum([res["ResultValue"] == "P" for res in test_results])

    # Find total number of tests
    n_tests_administered = len(test_results)
    log_status("Total number of tests: " + str(n_tests_administered))

    infections_by_county = get_infection_count_by_county(test_results, county_mapping)
    county_by_day = get_county_by_day(test_results, case_dates, county_mapping, county_sizes)
    confirmed_cases_by_county = get_confirmed_cases_by_county(test_results, county_mapping)
    tests_per_day_chart_data = get_tests_per_day_chart_data(test_results, case_dates)
    cumulative_cases_chart_data = get_cumulative_cases_chart_data(
        test_results,
        case_dates,
        tests_per_day_chart_data
    )
    cumulative_tests_chart_data = get_cumulative_tests_chart_data(test_results, case_dates)
    positive_test_by_age_chart_data = get_positive_tests_by_age_chart_data(test_results)
    positive_negative_chart_data = get_positive_negative_chart_data(test_results, county_mapping)
    county_daily_active = get_county_daily_active(test_results, case_dates, county_mapping, county_sizes)

    # Delete test result data from memory
    del test_results

    infections_by_county_10000 = get_infections_data_by_count_10000(infections_by_county, county_sizes)
    tests_pop_ratio = get_test_data_pop_ratio(infections_by_county_10000)
    new_cases_per_day_chart_data = get_new_cases_per_day_chart_data(cumulative_cases_chart_data)
    n_active_cases = cumulative_cases_chart_data["active"][-1]
    n_active_cases_change = (cumulative_cases_chart_data["active"][-1] - cumulative_cases_chart_data["active"][-2])
    per_100k = cumulative_cases_chart_data["active100k"][-1]
    active_infections_by_county = [
        {"MNIMI": k, "sequence": v, "drilldown": k}
        for k, v in county_daily_active["countyByDayActive"].items()
    ]
    active_infections_by_county_100k = [
        [k, round(v[-1] / county_sizes[k] * 100000, 2)]
        for k, v in county_daily_active["countyByDayActive"].items()
    ]


    # 4.  Calculate data related to test locations

    test_locations = read_json_from_file(TEST_LOCATIONS_PATH)

    municipalities_data = get_municipality_data(test_locations, county_mapping)

    # Delete test location data from memory
    del test_locations


    # 5.  Calculate data related to hospitalisation

    hospitalization = read_json_from_file(HOSPITALIZATION_PATH)

    log_status("Calculating data related to hospitalisation")

    # Set hospitalised and ICU time-series
    hospital = get_hospital_data(hospitalization, DATE_SETTINGS["first_case_date"])
    # TODO: Based on cross-checking with the hospitalisation data published by TEHIK, the data listed
    #       in the manual_data.json file with the field name "intensive" appears to show the number
    #       of patients on ventilation. We should fix the terminology and make sure that the intensive
    #       and on ventilation statistics are being calculated correctly.
    intensive = list(get_in_intensive_data(hospitalization, manual_data["intensive"]).values())
    on_ventilation = list(get_on_ventilation_data(hospitalization).values())
    # Delete hospitalization data from memory
    del hospitalization

    hospitalised = hospital["activehospitalizations"]
    n_on_ventilation = on_ventilation[-1]
    n_on_ventilation_change = int(on_ventilation[-1]) - int(on_ventilation[-2])


    # 6.  Calculate data related to vaccination

    vaccination = read_json_from_file(VACCINATIONS_PATH)

    log_status("Calculating data related to vaccination")

    vaccinated_people_chart_data = get_vaccinated_people_chart_data(vaccination, vaccination_dates)

    last_day_vaccination_data = [x for x in vaccination if x["MeasurementType"] == "Vaccinated" and x["VaccinationSeries"] == 1][-1]
    last_day_completed_vaccination_data = [x for x in vaccination if x["MeasurementType"] == "FullyVaccinated" and x["VaccinationSeries"] == 1][-1]
    last_day_doses_administered_data = [x for x in vaccination if x["MeasurementType"] == "DosesAdministered" and x["VaccinationSeries"] == 1][-1]
    # Delete vaccination data from memory
    del vaccination

    n_fully_vaccinated = last_day_completed_vaccination_data["TotalCount"]
    n_fully_vaccinated_change = last_day_completed_vaccination_data["DailyCount"]
    n_fully_vaccinated_percentage = last_day_completed_vaccination_data["PopulationCoverage"]
    n_vaccinated_at_least_one_dose = last_day_vaccination_data["TotalCount"]
    n_vaccinated_at_least_one_dose_change = last_day_vaccination_data["DailyCount"]
    n_vaccinated_at_least_one_dose_percentage = last_day_vaccination_data["PopulationCoverage"]
    # vaccination_number_total = (n_vaccinated_at_least_one_dose - n_fully_vaccinated)
    # vaccination_number_last_day = (n_vaccinated_at_least_one_dose_change - n_fully_vaccinated_change)


    # 7.  Create and save final JSON

    log_status("Compiling final JSON")

    final_json = {
        "updatedOn": TODAY_DMYHM,
        "confirmedCasesNumber": str(n_confirmed_cases),
        # TODO: For consistency, we should include the change in the number of confirmed cases as well.
        "hospitalisedNumber": str(hospital["activehospitalizations"][-1]),
        "hospitalChanged": str(hospital["activehospitalizations"][-1] - hospital["activehospitalizations"][-2]),
        "onVentilation": on_ventilation,
        "onVentilationNumber": n_on_ventilation,
        "onVentilationChanged": n_on_ventilation_change,
        "deceased": deceased,
        "deceasedNumber": str(n_deaths),
        "deceasedChanged": str(n_deaths_change),
        "testsAdministeredNumber": str(n_tests_administered),
        # TODO: For consistency, we should include the change in the number of tests as well.
        "activeCasesNumber": str(n_active_cases),
        "activeChanged": str(n_active_cases_change),
        "perHundred": str(per_100k), # TODO: This should be given a clearer name.
        "dates2": [str(x.date()) for x in case_dates],  # TODO: Change key to "caseDates"
        "dates3": [str(x.date()) for x in vaccination_dates],  # TODO: Change key to "vaccinationDates"
        "counties": counties,
        "age_groups": age_groups,
        "dataInfectionsByCounty": infections_by_county,
        "dataInfectionsByCounty10000": infections_by_county_10000,
        "dataActiveInfectionsByCounty100k": active_infections_by_county_100k,
        "dataActiveInfectionsByCounty": active_infections_by_county,
        "dataTestsPopRatio": tests_pop_ratio,
        "countyByDay": county_by_day,
        "dataCountyDailyActive": county_daily_active,
        "dataConfirmedCasesByCounty": confirmed_cases_by_county,
        "dataCumulativeCasesChart": cumulative_cases_chart_data,
        "dataNewCasesPerDayChart": new_cases_per_day_chart_data,
        "dataCumulativeTestsChart": cumulative_tests_chart_data,
        "dataTestsPerDayChart": tests_per_day_chart_data,
        "dataPositiveTestsByAgeChart": positive_test_by_age_chart_data,
        "dataPositiveNegativeChart": positive_negative_chart_data,
        "dataVaccinatedPeopleChart": vaccinated_people_chart_data,
        "dataMunicipalities": municipalities_data,
        "hospital": hospital, # TODO: Rename this to make it clearer what data it contains.
        # "vaccinationNumberTotal": vaccination_number_total,
        # "vaccinationNumberLastDay": vaccination_number_last_day,
        "fullyVaccinatedNumber": n_fully_vaccinated,
        "fullyVaccinatedNumberChange": n_fully_vaccinated_change,
        "fullyVaccinatedNumberPercentage": n_fully_vaccinated_percentage,
        "vaccinatedAtLeastOneDoseNumber": n_vaccinated_at_least_one_dose,
        "vaccinatedAtLeastOneDoseChange": n_vaccinated_at_least_one_dose_change,
        "vaccinatedAtLeastOneDosePercentage": n_vaccinated_at_least_one_dose_percentage,
    }

    # Dump JSON output
    log_status("Dumping JSON output")
    save_as_json(OUTPUT_FILE_LOCATION, final_json)

    # Log finish time
    finish = datetime.today().astimezone(ESTONIA_TIMEZONE).strftime("%d/%m/%Y, %H:%M")
    log_status("Finished update process at " + finish)


if __name__ == "__main__":
    main()

