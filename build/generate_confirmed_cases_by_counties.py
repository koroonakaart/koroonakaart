from build.chart_data_functions import get_confirmed_cases_by_county
from build.chart_data_functions import get_county_by_day
from build.constants import CONFIRMED_CASES_BY_COUNTIES_PATH
from build.constants import COUNTY_MAPPING
from build.constants import COUNTY_POPULATION
from build.constants import DATE_SETTINGS
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

    # Log status
    logger.info("Calculating main statistics")

    # Create date ranges for charts
    dates2 = pd.date_range(start=DATE_SETTINGS["dates2_start"], end=YESTERDAY_YMD)

    # Get data for each chart
    logger.info("Calculating data for charts")
    county_by_day = get_county_by_day(
        test_results, dates2, COUNTY_MAPPING, COUNTY_POPULATION
    )
    confirmed_cases_by_county = get_confirmed_cases_by_county(
        test_results, COUNTY_MAPPING
    )

    del county_by_day["mapPlayback"]
    del county_by_day["mapPlayback10k"]

    # Create dictionary for final JSON
    logger.info("Compiling final JSON")
    final_json = {
        "updatedOn": TODAY_DMYHM,
        "dataConfirmedCasesByCounties": confirmed_cases_by_county,
        "countyByDay": county_by_day,
    }

    # Dump JSON output
    save_as_json(CONFIRMED_CASES_BY_COUNTIES_PATH, final_json)

    # Log finish time
    logger.info("Finished update process")


if __name__ == "__main__":
    main()
