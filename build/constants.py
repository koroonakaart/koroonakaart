from datetime import datetime
from datetime import timedelta

import pytz

ESTONIA_TZ = pytz.timezone("Europe/Helsinki")
TODAY_DMYHM = datetime.today().astimezone(ESTONIA_TZ).strftime("%d/%m/%Y, %H:%M")
YESTERDAY_YMD = datetime.strftime(datetime.today() - timedelta(1), "%Y-%m-%d")

DATE_SETTINGS = {
    "dates2_start": "2020-02-26",  # The date of the first Covid-19 case in Estonia. Most charts start from this date.
    "dates3_start": "2020-12-26",  # Vaccination started in Estonia on 27 December 2020. Time series charts related
    # to vaccination start one day earlier.
}

# Relative to repo root

# Source files
MANUAL_DATA_PATH = "data/manual_data.json"
DEATHS_PATH = "data/deaths.json"
TEST_RESULTS_PATH = "data/test_results.json"
TEST_LOCATIONS_PATH = "data/test_locations.json"
HOSPITALIZATION_PATH = "data/hospitalization.json"
VACCINATIONS_PATH = "data/vaccinations.json"

# Result files
OUTPUT_PATH = "koroonakaart/src/data/data.json"
CONFIRMED_CASES_BY_COUNTIES_PATH = "koroonakaart/src/data/ConfirmedCasesByCounties.json"
CUMULATIVE_CASES_PATH = "koroonakaart/src/data/CumulativeCases.json"
CUMULATIVE_CASES_PER_100K_PATH = "koroonakaart/src/data/CumulativeCasesPer100k.json"
CUMULATIVE_TESTS_PATH = "koroonakaart/src/data/CumulativeTests.json"
DAILY_COUNTY_CASES_PATH = "koroonakaart/src/data/DailyCountyCases.json"
DAILY_COUNTY_NEW_CASES_PATH = "koroonakaart/src/data/DailyCountyNewCases.json"
GENDER_PATH = "koroonakaart/src/data/Gender.json"
NEW_CASES_PER_DAY_PATH = "koroonakaart/src/data/NewCasesPerDay.json"
POSITIVE_NEGATIVE_PATH = "koroonakaart/src/data/PositiveNegative.json"
POSITIVE_TESTS_AGE_DISTRIBUTION_PATH = (
    "koroonakaart/src/data/PositiveTestsAgeDistribution.json"
)
TESTS_AGE_SEX_DISTRIBUTION_PATH = "koroonakaart/src/data/TestsAgeSexDistribution.json"
TESTS_PER_DAY_PATH = "koroonakaart/src/data/TestsPerDay.json"
TESTS_POP_RATIO_PATH = "koroonakaart/src/data/TestsPopRatio.json"
VACCINATED_PEOPLE_PATH = "koroonakaart/src/data/VaccinatedPeople.json"

COUNTY_MAPPING = {
    "Harju maakond": "Harjumaa",
    "Hiiu maakond": "Hiiumaa",
    "Ida-Viru maakond": "Ida-Virumaa",
    "Järva maakond": "Järvamaa",
    "Jõgeva maakond": "Jõgevamaa",
    "Lääne maakond": "Läänemaa",
    "Lääne-Viru maakond": "Lääne-Virumaa",
    "": "Info puudulik",
    "Pärnu maakond": "Pärnumaa",
    "Põlva maakond": "Põlvamaa",
    "Rapla maakond": "Raplamaa",
    "Saare maakond": "Saaremaa",
    "Tartu maakond": "Tartumaa",
    "Valga maakond": "Valgamaa",
    "Viljandi maakond": "Viljandimaa",
    "Võru maakond": "Võrumaa",
    "Eesti": "Info puudulik",
}

COUNTIES = [
    "Harjumaa",
    "Hiiumaa",
    "Ida-Virumaa",
    "Jõgevamaa",
    "Järvamaa",
    "Läänemaa",
    "Lääne-Virumaa",
    "Põlvamaa",
    "Pärnumaa",
    "Raplamaa",
    "Saaremaa",
    "Tartumaa",
    "Valgamaa",
    "Viljandimaa",
    "Võrumaa",
]

COUNTIES_INCL_UNKNOWN = COUNTIES.copy() + [
    "Info puudulik",
]

COUNTIES_INCL_UNKNOWN_FIRST = ["Info puudulik"] + COUNTIES.copy()

# 2020 population from https://www.stat.ee/et/avasta-statistikat/piirkonnad
COUNTY_POPULATION = {
    "Harjumaa": 605029,
    "Hiiumaa": 9315,
    "Ida-Virumaa": 134259,
    "Jõgevamaa": 28442,
    "Järvamaa": 30174,
    "Lääne-Virumaa": 58862,
    "Läänemaa": 20444,
    "Põlvamaa": 24647,
    "Pärnumaa": 86185,
    "Raplamaa": 33282,
    "Saaremaa": 33083,
    "Tartumaa": 153317,
    "Valgamaa": 28204,
    "Viljandimaa": 46161,
    "Võrumaa": 35415,
}

AGE_GROUPS = [
    "0-4",
    "5-9",
    "10-14",
    "15-19",
    "20-24",
    "25-29",
    "30-34",
    "35-39",
    "40-44",
    "45-49",
    "50-54",
    "55-59",
    "60-64",
    "65-69",
    "70-74",
    "75-79",
    "80-84",
    "üle 85",
]
