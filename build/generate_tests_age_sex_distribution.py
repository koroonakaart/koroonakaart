from build.chart_data_functions import get_positive_tests_by_age_chart_data
from build.constants import TEST_RESULTS_PATH
from build.constants import TESTS_AGE_SEX_DISTRIBUTION_PATH
from build.constants import TODAY_DMYHM
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

    logger.info("Calculating data for charts")
    positive_test_by_age_chart_data = get_positive_tests_by_age_chart_data(test_results)

    # Create dictionary for final JSON
    logger.info("Compiling final JSON")
    final_json = {
        "updatedOn": TODAY_DMYHM,
        "dataPositiveTestsByAgeChart": positive_test_by_age_chart_data,
    }

    # Dump JSON output
    save_as_json(TESTS_AGE_SEX_DISTRIBUTION_PATH, final_json)

    # Log finish time
    logger.info("Finished update process")


if __name__ == "__main__":
    main()
