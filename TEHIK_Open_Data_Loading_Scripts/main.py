import json
import requests
from datetime import datetime, timedelta, date
from constants import county_mapping, county_sizes, counties, age_groups
from chart_data_functions import *
from helpers import NpEncoder


today = datetime.today().strftime('%d/%m/%Y, %H:%M'),
yesterday = datetime.strftime(datetime.today() - timedelta(1), '%Y-%m-%d')


######## CONFIGURE MANUAL DATA ########

MANUAL_DATA = {
    "updatedOn": today[0],
    "deceasedNumber": 125,
    "datesEnd": yesterday,
    "dates1Start": "2020-03-15",
    "dates2Start": "2020-02-26",
    "intensive": [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 6, 7, 7,
        7, 7, 10, 10, 13, 13, 15, 16, 16, 20, 17, 14, 12, 11,
        9, 9, 11, 11, 9, 11, 10, 10, 11, 11, 10, 9, 8, 7,
        7, 6, 6, 6, 7, 8, 10, 9, 7, 7, 7, 6, 6, 4,
        4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 3, 2,
        2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 1, 1, 1, 1, 1, 2, 3, 3, 2, 3, 3, 3, 2,
        2, 1, 0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 4, 3,
        2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1,
        1, 1, 3, 3, 4, 3, 1, 1, 3, 2, 2, 2, 2, 2,
        4, 4, 4, 4, 4, 5, 6, 6, 5, 5, 5, 7, 6, 6,
        7, 10, 8, 7, 8, 8, 7, 7, 6, 6, 7, 11, 12, 11,
        12, 11
    ],
    "deceased": [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 1, 1, 3, 3, 4, 5, 11, 12, 13, 15, 19, 21, 24,
        24, 24, 24, 25, 27, 31, 35, 36, 38, 38, 40, 40, 43, 44,
        45, 46, 47, 50, 52, 52, 52, 54, 54, 55, 57, 57, 57, 57,
        59, 59, 60, 60, 61, 61, 61, 62, 63, 63, 63, 64, 64, 64,
        64, 64, 64, 64, 65, 65, 66, 66, 67, 67, 68, 68, 68, 69,
        69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69,
        69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69,
        69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69,
        69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69,
        69, 69, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63,
        63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 64, 64, 64,
        64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
        64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
        64, 64, 64, 64, 64, 64, 64, 65, 66, 67, 67, 67, 67, 67,
        67, 68, 68, 68, 68, 68, 68, 68, 68, 68, 68, 68, 71, 71,
        71, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73,
        73, 73, 73, 75, 76, 76, 76, 76, 80, 80, 81, 81, 84, 85,
        86, 87, 87, 88, 92, 94, 97, 99, 104, 109, 112, 118, 121, 122,
        123, 125
    ]
}


######## CONFIGURE IO LOCATIONS ########

API_ENDPOINT = "https://opendata.digilugu.ee/opendata_covid19_test_results.json"
MUNICIPALITIES_ENDPOINT = "https://opendata.digilugu.ee/opendata_covid19_test_location.json"
HOSPITAL_ENDPOINT = "https://opendata.digilugu.ee/opendata_covid19_hospitalization_timeline.json"
MANUAL_DATA_FILE_LOCATION = "manualData.json"
DEATHS_FILE_LOCATION = "deaths.json"
OUTPUT_FILE_LOCATION = "../koroonakaart/src/data.json"


def get_json_data(url) -> any:
    # Open data endpoint
    r = requests.get(url=url)
    return r.json()

def read_json_from_file(path) -> any:
    with open(path) as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    # Get data

    json_manual = read_json_from_file(MANUAL_DATA_FILE_LOCATION)
    json_data = get_json_data(API_ENDPOINT)
    municipalities = get_json_data(MUNICIPALITIES_ENDPOINT)
    json_hospital = get_json_data(HOSPITAL_ENDPOINT)
    json_deaths = read_json_from_file(DEATHS_FILE_LOCATION)

    # Date of update
    updatedOn = MANUAL_DATA["updatedOn"]

    # Statsbar
    # Find count of confirmed cases
    confirmedCasesNumber = np.sum([res["ResultValue"] == "P" for res in json_data])

    # Find total number of tests
    testsAdministeredNumber = len(json_data)

    # Calculate active number of cases

    # Set date ranges
    dates_range_end = MANUAL_DATA["datesEnd"]

    dates1_range_start = MANUAL_DATA["dates1Start"]
    dates1_range_end = dates_range_end

    dates2_range_start = MANUAL_DATA["dates2Start"]
    dates2_range_end = dates_range_end


    # Create date ranges for charts
    dates1 = pd.date_range(start=dates1_range_start, end=dates1_range_end)
    dates2 = pd.date_range(start=dates2_range_start, end=dates2_range_end)

    # Create copy
    json_copy = json_data
    municipalities_copy = municipalities
    hospital_copy = json_hospital
    hospital = getHospitalData(hospital_copy)

    # Set recovered, deceased, hospitalised and ICU time-series
    recovered = hospital["discharged"]
    deceased = list(mergeDateDictionaries(json_deaths, json_manual["deceased"]))
    hospitalised =  hospital["hospitalizations"]
    intensive = list(getOnVentilationData(json_hospital, json_manual['intensive']).values())

    deceasedNumber = deceased[-1]
    deceasedChanged = deceased[-1] - deceased[-2]

    # Get data for each chart
    dataInfectionsByCounty = getCountInfectionsByCounty(json_copy, county_mapping)
    dataInfectionsByCounty10000 = getDataInfectionsByCount10000(dataInfectionsByCounty, county_sizes)
    dataTestsPopRatio = getDataTestsPopRatio(dataInfectionsByCounty10000)
    countyByDay = getCountyByDay(json_copy, dates2, county_mapping,county_sizes)
    dataConfirmedCasesByCounties = getDataConfirmedCasesByCounties(json_copy, county_mapping)
    dataCumulativeCasesChart = getDataCumulativeCasesChart(json_copy, recovered, deceased, hospitalised, intensive,
                                                           dates2)
    dataNewCasesPerDayChart = getDataNewCasesPerDayChart(dataCumulativeCasesChart)
    dataCumulativeTestsChart = getDataCumulativeTestsChart(json_copy, dates2)
    dataTestsPerDayChart = getDataTestsPerDayChart(json_copy, dates2)
    dataPositiveTestsByAgeChart = getDataPositiveTestsByAgeChart(json_copy)
    dataPositiveNegativeChart = getDataPositiveNegativeChart(json_copy, county_mapping)
    dataCountyDailyActive = getdataCountyDailyActive(json_copy,dates2,county_mapping,county_sizes)
    activeCasesNumber = dataCumulativeCasesChart["active"][-1]
    activeChanged = dataCumulativeCasesChart["active"][-1] - dataCumulativeCasesChart["active"][-2]
    dataActiveInfectionsByCounty = [{"MNIMI": k, "sequence": v, "drilldown": k} for k,v in dataCountyDailyActive["countyByDayActive"].items()]
    dataActiveInfectionsByCounty100k = [[k, round(v[-1] / county_sizes[k] * 100000, 2)] for k,v in dataCountyDailyActive["countyByDayActive"].items()]
    dataMunicipalities = getMunicipalityData(municipalities_copy, county_mapping)
    perHundred = dataCumulativeCasesChart["active100k"][-1]


    # Create dictionary for final json
    finalJson = {
        "updatedOn": updatedOn,
        "confirmedCasesNumber": str(confirmedCasesNumber),
        "activeCasesNumber": str(activeCasesNumber),
        "perHundred": str(perHundred),
        "hospitalisedNumber": str(hospital["activehospitalizations"][-1]),
        "deceasedNumber": str(deceasedNumber),
        "recoveredNumber": str(hospital["discharged"][-1]),
        "testsAdministeredNumber": str(testsAdministeredNumber),
        "hospitalChanged": str(hospital["activehospitalizations"][-1] - hospital["activehospitalizations"][-2]),
        "deceasedChanged": str(deceasedChanged),
        "recoveredChanged": str(hospital["discharged"][-1] - hospital["discharged"][-2]),
        "activeChanged": str(activeChanged),
        "dates1": list(map(lambda x: str(x.date()), dates1)),
        "dates2": list(map(lambda x: str(x.date()), dates2)),
        "counties": counties,
        "age_groups": age_groups,
        "dataInfectionsByCounty": dataInfectionsByCounty,
        "dataInfectionsByCounty10000": dataInfectionsByCounty10000,
        "dataActiveInfectionsByCounty100k": dataActiveInfectionsByCounty100k,
        "dataActiveInfectionsByCounty": dataActiveInfectionsByCounty,
        "dataTestsPopRatio": dataTestsPopRatio,
        "countyByDay": countyByDay,
        "dataCountyDailyActive": dataCountyDailyActive,
        "dataConfirmedCasesByCounties": dataConfirmedCasesByCounties,
        "dataCumulativeCasesChart": dataCumulativeCasesChart,
        "dataNewCasesPerDayChart": dataNewCasesPerDayChart,
        "dataCumulativeTestsChart": dataCumulativeTestsChart,
        "dataTestsPerDayChart": dataTestsPerDayChart,
        "dataPositiveTestsByAgeChart": dataPositiveTestsByAgeChart,
        "dataPositiveNegativeChart": dataPositiveNegativeChart,
        "dataMunicipalities": dataMunicipalities,
        "hospital": hospital
    }

    # Dump json output
    with open(OUTPUT_FILE_LOCATION, "w", encoding="utf-8") as f:
        json.dump(finalJson, f, cls=NpEncoder, ensure_ascii=False)

