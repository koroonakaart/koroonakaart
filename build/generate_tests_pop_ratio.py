from build.chart_data_functions import get_infection_count_by_county
from build.chart_data_functions import get_infections_data_by_count_10000
from build.chart_data_functions import get_test_data_pop_ratio
from build.constants import COUNTY_MAPPING
from build.constants import COUNTY_POPULATION
from build.constants import TEST_RESULTS_PATH
from build.constants import TESTS_POP_RATIO_PATH
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

    # Get data for each chart
    logger.info("Calculating data for charts")
    infections_by_county = get_infection_count_by_county(test_results, COUNTY_MAPPING)
    infections_by_county_10000 = get_infections_data_by_count_10000(
        infections_by_county, COUNTY_POPULATION
    )
    tests_pop_ratio = get_test_data_pop_ratio(infections_by_county_10000)

    # Create dictionary for final JSON
    logger.info("Compiling final JSON")
    final_json = {
        "updatedOn": TODAY_DMYHM,
        "dataTestsPopRatio": tests_pop_ratio,
    }

    # Dump JSON output
    save_as_json(TESTS_POP_RATIO_PATH, final_json)

    # Log finish time
    logger.info("Finished update process")


if __name__ == "__main__":
    main()
