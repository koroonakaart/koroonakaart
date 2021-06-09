from build.chart_data_functions import get_positive_negative_chart_data
from build.constants import COUNTY_MAPPING
from build.constants import POSITIVE_NEGATIVE_PATH
from build.constants import TEST_RESULTS_PATH
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

    # Log status
    logger.info("Calculating data for charts")

    positive_negative_chart_data = get_positive_negative_chart_data(
        test_results, COUNTY_MAPPING
    )

    # Create dictionary for final JSON
    logger.info("Compiling final JSON")
    final_json = {
        "updatedOn": TODAY_DMYHM,
        "dataPositiveNegativeChart": positive_negative_chart_data,
    }

    # Dump JSON output
    save_as_json(POSITIVE_NEGATIVE_PATH, final_json)

    # Log finish time
    logger.info("Finished update process")


if __name__ == "__main__":
    main()
