from build.chart_data_functions import get_vaccinated_people_chart_data
from build.constants import DATE_SETTINGS
from build.constants import TODAY_DMYHM
from build.constants import VACCINATED_PEOPLE_PATH
from build.constants import VACCINATIONS_PATH
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
    vaccination = read_json_from_file(VACCINATIONS_PATH)

    logger.info("Calculating main statistics")
    vaccination_dates = pd.date_range(
        start=DATE_SETTINGS["vaccinationStartDate"], end=YESTERDAY_YMD
    )

    logger.info("Calculating data for charts")
    vaccinated_people_chart_data = get_vaccinated_people_chart_data(
        vaccination, vaccination_dates
    )

    # Create dictionary for final JSON
    logger.info("Compiling final JSON")
    final_json = {
        "updatedOn": TODAY_DMYHM,
        "vaccinationDates": [str(x.date()) for x in vaccination_dates],
        "dataVaccinatedPeopleChart": vaccinated_people_chart_data,
    }

    # Dump JSON output
    save_as_json(VACCINATED_PEOPLE_PATH, final_json)

    # Log finish time
    logger.info("Finished update process")


if __name__ == "__main__":
    main()
