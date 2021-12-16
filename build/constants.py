# Source files
MANUAL_DATA_PATH = "../data/manual_data.json"
DEATHS_PATH = "../data/deaths.json"
TEST_RESULTS_PATH = "../data/test_results.json"
TEST_LOCATIONS_PATH = "../data/test_locations.json"
HOSPITALIZATION_PATH = "../data/hospitalization.json"
VACCINATIONS_PATH = "../data/vaccinations.json"

# Output files
OUTPUT_FILE_LOCATION = "../data/data.json"


county_mapping = {
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

counties = [
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
    "Info puudulik",
]

# 2020 population from https://www.stat.ee/et/avasta-statistikat/piirkonnad
county_sizes = {
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

age_groups = [
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
