import numpy as np
import pandas as pd

from build.chart_data_functions import get_cumulative_cases_chart_data
from build.chart_data_functions import get_cumulative_tests_chart_data
from build.chart_data_functions import get_hospital_data
from build.chart_data_functions import get_in_intensive_data
from build.chart_data_functions import get_new_cases_per_day_chart_data
from build.chart_data_functions import get_on_ventilation_data
from build.chart_data_functions import get_tests_per_day_chart_data
from build.constants import DATE_SETTINGS, STATS_BAR_PATH, POPULATION
from build.constants import DEATHS_PATH
from build.constants import HOSPITALIZATION_PATH
from build.constants import MANUAL_DATA_PATH
from build.constants import TEST_RESULTS_PATH
from build.constants import TODAY_DMYHM
from build.constants import VACCINATIONS_PATH
from build.constants import YESTERDAY_YMD
from build.utils import analyze_memory
from build.utils import analyze_time
from build.utils import logger
from build.utils import read_json_from_file
from build.utils import save_as_json


@analyze_time
@analyze_memory
def main():
    # Log status
    logger.info("Loading local data files")
    test_results = read_json_from_file(TEST_RESULTS_PATH)
    hospitalization = read_json_from_file(HOSPITALIZATION_PATH)
    vaccination = read_json_from_file(VACCINATIONS_PATH)
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
    case_dates = pd.date_range(start=DATE_SETTINGS["firstCaseDate"], end=YESTERDAY_YMD)

    # Set recovered, deceased, hospitalized and ICU time-series
    hospital = get_hospital_data(hospitalization, DATE_SETTINGS["firstCaseDate"])
    recovered = hospital["discharged"]
    manual_data["deceased"].update(deaths)
    deceased = list(manual_data["deceased"].values())
    hospitalized = hospital["activeHospitalizations"]
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
    tests_per_day_chart_data = get_tests_per_day_chart_data(test_results, case_dates)
    cumulative_cases_chart_data = get_cumulative_cases_chart_data(
        test_results,
        recovered,
        deceased,
        hospitalized,
        intensive,
        on_ventilation,
        case_dates,
        test_per_day_chart_data=tests_per_day_chart_data,
    )
    new_cases_per_day_chart_data = get_new_cases_per_day_chart_data(
        cumulative_cases_chart_data
    )
    cumulative_tests_chart_data = get_cumulative_tests_chart_data(
        test_results, case_dates
    )

    n_active_cases = cumulative_cases_chart_data["active"][-1]
    n_active_cases_change = (
        cumulative_cases_chart_data["active"][-1]
        - cumulative_cases_chart_data["active"][-2]
    )

    # Calculate vaccination data
    logger.info("Calculating vaccination data")
    last_day_vaccination_data = [
        x for x in vaccination if x["MeasurementType"] == "Vaccinated"
    ][-1]
    last_day_completed_vaccination_data = [
        x for x in vaccination if x["MeasurementType"] == "FullyVaccinated"
    ][-1]
    # TODO: Doses administered
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
    raw_active_100k = (
        cumulative_cases_chart_data["active"][-1]
        - cumulative_cases_chart_data["active"][-2]
    )
    raw_confirmed_changed = new_cases_per_day_chart_data["confirmedCases"][-1]
    raw_per_hundred_changed = (
        cumulative_cases_chart_data["active100k"][-1]
        - cumulative_cases_chart_data["active100k"][-2]
    )
    confirmed_changed = new_cases_per_day_chart_data["confirmedCases"][-1]
    tests_changed = (
        cumulative_tests_chart_data["testsAdministered"][-1]
        - cumulative_tests_chart_data["testsAdministered"][-2]
    )

    partially_immunized_total = all_vaccination_number_total + n_confirmed_cases
    partially_immunized_pct = round(
        (float(partially_immunized_total) / float(POPULATION) * 100), 2
    )

    # Create dictionary for final JSON
    logger.info("Compiling final JSON")
    final_json = {
        "updatedOn": TODAY_DMYHM,
        "activeCasesNumber": str(n_active_cases),
        "activeChanged": str(n_active_cases_change),
        "allVaccinationFromPopulationPercentage": last_day_vaccination_data[
            "PopulationCoverage"
        ],
        "allVaccinationNumberLastDay": all_vaccination_number_last_day,
        "allVaccinationNumberTotal": all_vaccination_number_total,
        "completedVaccinationNumberLastDay": completed_vaccination_number_last_day,
        "completedVaccinationNumberTotal": completed_vaccination_number_total,
        "completelyVaccinatedFromTotalVaccinatedPercentage": fully_vaccinated_from_total_vaccinated_percentage,
        "confirmedCasesNumber": str(n_confirmed_cases),
        "confirmedChanged": confirmed_changed,
        "deceasedChanged": str(n_deaths_change),
        "deceasedNumber": str(n_deaths),
        "hospitalizedChanged": str(
            hospital["activeHospitalizations"][-1]
            - hospital["activeHospitalizations"][-2]
        ),
        "hospitalizedNumber": hospital["activeHospitalizations"][-1],
        "partiallyImmunized": partially_immunized_total,
        "partiallyImmunizedPercentage": partially_immunized_pct,
        "perHundred": cumulative_cases_chart_data["active100k"][-1],
        "positiveTestAverage14Percent": tests_per_day_chart_data[
            "positiveTestAverage14Percent"
        ],
        "rawActiveChanged": raw_active_100k,
        "rawConfirmedChanged": raw_confirmed_changed,
        "rawPerHundredChanged": raw_per_hundred_changed,
        "recoveredChanged": str(
            hospital["discharged"][-1] - hospital["discharged"][-2]
        ),
        "recoveredNumber": hospital["discharged"][-1],
        "testsAdministeredNumber": str(n_tests_administered),
        "testsChanged": tests_changed,
        "vaccinationNumberLastDay": vaccination_number_last_day,
        "vaccinationNumberTotal": vaccination_number_total,
    }

    # Dump JSON output
    save_as_json(STATS_BAR_PATH, final_json)

    # Log finish time
    logger.info("Finished update process")


if __name__ == "__main__":
    main()
