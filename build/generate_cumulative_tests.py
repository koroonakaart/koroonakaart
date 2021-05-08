from build.chart_data_functions import get_cumulative_tests_chart_data
from build.constants import CUMULATIVE_TESTS_PATH
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

    # Set recovered, deceased, hospitalized and ICU time-series
    cumulative_tests_chart_data = get_cumulative_tests_chart_data(test_results, dates2)

    # Create dictionary for final JSON
    logger.info("Compiling final JSON")
    final_json = {
        "updatedOn": TODAY_DMYHM,
        "dates2": [str(x.date()) for x in dates2],
        "testsAdministered": cumulative_tests_chart_data["testsAdministered"],
    }

    # Dump JSON output
    save_as_json(CUMULATIVE_TESTS_PATH, final_json)

    # Log finish time
    logger.info("Finished update process")


if __name__ == "__main__":
    main()
