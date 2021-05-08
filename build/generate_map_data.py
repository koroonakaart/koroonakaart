import pandas as pd

from build.chart_data_functions import get_county_by_day
from build.chart_data_functions import get_county_daily_active
from build.chart_data_functions import get_infection_count_by_county
from build.chart_data_functions import get_infections_data_by_count_10000
from build.chart_data_functions import get_municipality_data
from build.constants import COUNTY_MAPPING, MAP_PATH
from build.constants import COUNTY_POPULATION
from build.constants import DATE_SETTINGS
from build.constants import TEST_LOCATIONS_PATH
from build.constants import TEST_RESULTS_PATH
from build.constants import TODAY_DMYHM
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
    test_locations = read_json_from_file(TEST_LOCATIONS_PATH)

    # Log status
    logger.info("Calculating main statistics")
    dates2 = pd.date_range(start=DATE_SETTINGS["dates2_start"], end=YESTERDAY_YMD)

    # Get data for each chart
    logger.info("Calculating data for charts")
    infections_by_county = get_infection_count_by_county(test_results, COUNTY_MAPPING)
    infections_by_county_10000 = get_infections_data_by_count_10000(
        infections_by_county, COUNTY_POPULATION
    )
    county_by_day = get_county_by_day(
        test_results, dates2, COUNTY_MAPPING, COUNTY_POPULATION
    )
    county_daily_active = get_county_daily_active(
        test_results, dates2, COUNTY_MAPPING, COUNTY_POPULATION
    )
    active_infections_by_county = [
        {"MNIMI": k, "sequence": v, "drilldown": k}
        for k, v in county_daily_active["countyByDayActive"].items()
    ]
    municipalities_data = get_municipality_data(test_locations, COUNTY_MAPPING)

    # Create dictionary for final JSON
    logger.info("Compiling final JSON")
    final_json = {
        "updatedOn": TODAY_DMYHM,
        "dates2": [str(x.date()) for x in dates2],
        "dataMunicipalities": municipalities_data,
        "mapPlayback": county_by_day["mapPlayback"],
        "mapPlayback10k": county_by_day["mapPlayback10k"],
        "dataActiveInfectionsByCounty": active_infections_by_county,
        "dataCountyDailyActive": county_daily_active,
        "dataInfectionsByCounty": infections_by_county,
        "dataInfectionsByCounty10000": infections_by_county_10000,
    }

    # Dump JSON output
    save_as_json(MAP_PATH, final_json)

    # Log finish time
    logger.info("Finished update process")


if __name__ == "__main__":
    main()
