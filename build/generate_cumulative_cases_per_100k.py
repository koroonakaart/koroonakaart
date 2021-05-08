from build.chart_data_functions import get_cumulative_cases_chart_data
from build.chart_data_functions import get_hospital_data
from build.chart_data_functions import get_in_intensive_data
from build.chart_data_functions import get_on_ventilation_data
from build.constants import CUMULATIVE_CASES_PER_100K_PATH
from build.constants import DATE_SETTINGS
from build.constants import DEATHS_PATH
from build.constants import HOSPITALIZATION_PATH
from build.constants import MANUAL_DATA_PATH
from build.constants import TEST_RESULTS_PATH
from build.constants import TODAY_DMYHM
from build.constants import YESTERDAY_YMD
from build.utils import analyze_memory
from build.utils import analyze_time
from build.utils import logger
from build.utils import read_json_from_file
from build.utils import save_as_json
import pandas as pd


@analyze_time
@analyze_memory
def main():
    # Log status
    logger.info("Loading local data files")
    test_results = read_json_from_file(TEST_RESULTS_PATH)
    hospitalization = read_json_from_file(HOSPITALIZATION_PATH)
    deaths = read_json_from_file(DEATHS_PATH)
    manual_data = read_json_from_file(MANUAL_DATA_PATH)

    # Log status
    logger.info("Calculating main statistics")

    # Create date ranges for charts
    dates2 = pd.date_range(start=DATE_SETTINGS["dates2_start"], end=YESTERDAY_YMD)

    # Set recovered, deceased, hospitalized and ICU time-series
    hospital = get_hospital_data(hospitalization, DATE_SETTINGS["dates2_start"])
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

    # Get data for each chart
    logger.info("Calculating data for charts")
    cumulative_cases_chart_data = get_cumulative_cases_chart_data(
        test_results,
        recovered,
        deceased,
        hospitalized,
        intensive,
        on_ventilation,
        dates2,
    )

    # Create dictionary for final JSON
    logger.info("Compiling final JSON")
    final_json = {
        "updatedOn": TODAY_DMYHM,
        "dates2": [str(x.date()) for x in dates2],
        "active100k": cumulative_cases_chart_data["active100k"],
    }

    # Dump JSON output
    save_as_json(CUMULATIVE_CASES_PER_100K_PATH, final_json)

    # Log finish time
    logger.info("Finished update process")


if __name__ == "__main__":
    main()
