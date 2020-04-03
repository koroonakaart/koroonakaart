import json
import requests
from constants import county_mapping, county_sizes
from chart_data_functions import *
from helpers import NpEncoder


######## CONFIGURE MANUAL DATA ########
MANUAL_DATA = {
    "updatedOn": "02/04/2020, 12:30",
    "hospitalisedNumber": 85,
    "deceasedNumber": 11,
    "recoveredNumber": 45,
    "datesEnd": "2020-04-02",
    "dates1Start": "2020-03-16",
    "dates2Start": "2020-02-26",
    "recovered": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 4, 7, 8, 8, 11, 11, 20, 20,
                  20,
                  26, 33, 45],
    "deceased": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 3, 3,
                 4, 5,
                 11],
    "hospitalised": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 3, 3, 3, 8, 10, 14, 15, 17, 28, 29, 34,
                     40, 48,
                     56, 79, 91, 95, 85],
    "intensive": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 6, 7, 7, 7, 7, 10, 10,
                  13,
                  13, 15, 16]
}

######## CONFIGURE IO LOCATIONS ########
API_ENDPONT = "https://opendata.digilugu.ee/opendata_covid19_test_results.json"
OUTPUT_FILE_LOCATION = "../data_new.json"

def get_json_data(url) -> any:
    # Open data endpoint
    r = requests.get(url=url)
    return r.json()

if __name__ == "__main__":
    # Get data
    json_data = get_json_data(API_ENDPONT)

    # Date of update
    updatedOn = MANUAL_DATA["updatedOn"]

    # Statsbar
    hospitalisedNumber = MANUAL_DATA["hospitalisedNumber"]
    deceasedNumber = MANUAL_DATA["deceasedNumber"]
    recoveredNumber = MANUAL_DATA["recoveredNumber"]

    # Find count of confirmed cases
    confirmedCasesNumber = np.sum([res["ResultValue"] == "P" for res in json_data])

    # Find total number of tests
    testsAdministeredNumber = len(json_data)

    # Calculate active number of cases
    activeCasesNumber = confirmedCasesNumber - (deceasedNumber + recoveredNumber)

    # Set date ranges
    dates_range_end = MANUAL_DATA["datesEnd"]

    dates1_range_start = MANUAL_DATA["dates1Start"]
    dates1_range_end = dates_range_end
    # dates1_range_end = "2020-04-02"

    dates2_range_start = MANUAL_DATA["dates2Start"]
    dates2_range_end = dates_range_end
    # dates2_range_end = "2020-04-02"

    # Set recovered, deceased, hospitalised and ICU time-series
    recovered = MANUAL_DATA["recovered"]
    deceased = MANUAL_DATA["deceased"]
    hospitalised =  MANUAL_DATA["hospitalised"]
    intensive = MANUAL_DATA["intensive"]

    # Create date ranges for charts
    dates1 = pd.date_range(start=dates1_range_start, end=dates1_range_end)
    dates2 = pd.date_range(start=dates2_range_start, end=dates2_range_end)

    # create copy
    json_copy = json_data


    # Get data for each chart
    dataInfectionsByCounty = getCountInfectionsByCounty(json_copy, county_mapping)
    dataInfectionsByCounty10000 = getDataInfectionsByCount10000(dataInfectionsByCounty, county_sizes)
    dataTestsPopRatio = getDataTestsPopRatio(dataInfectionsByCounty10000)
    countyByDay = getCountyByDay(json_copy, dates2, county_mapping)
    dataConfirmedCasesByCounties = getDataConfirmedCasesByCounties(json_copy, county_mapping)
    dataCumulativeCasesChart = getDataCumulativeCasesChart(json_copy, recovered, deceased, hospitalised, intensive,
                                                           dates2)
    dataNewCasesPerDayChart = getDataNewCasesPerDayChart(dataCumulativeCasesChart)
    dataCumulativeTestsChart = getDataCumulativeTestsChart(json_copy, dates2)
    dataTestsPerDayChart = getDataTestsPerDayChart(json_copy, dates2)
    dataPositiveTestsByAgeChart = getDataPositiveTestsByAgeChart(json_copy)
    dataPositiveNegativeChart = getDataPositiveNegativeChart(json_copy, county_mapping)

    # Create dictionary for final json
    finalJson = {
        "updatedOn": updatedOn,
        "confirmedCasesNumber": str(confirmedCasesNumber),
        "activeCasesNumber": str(activeCasesNumber),
        "hospitalisedNumber": str(hospitalisedNumber),
        "deceasedNumber": str(deceasedNumber),
        "recoveredNumber": str(recoveredNumber),
        "testsAdministeredNumber": str(testsAdministeredNumber),
        "dates1": list(map(lambda x: str(x.date()), dates1)),
        "dates2": list(map(lambda x: str(x.date()), dates2)),
        "dataInfectionsByCounty": dataInfectionsByCounty,
        "dataInfectionsByCounty10000": dataInfectionsByCounty10000,
        "dataTestsPopRatio": dataTestsPopRatio,
        "countyByDay": countyByDay,
        "dataConfirmedCasesByCounties": dataConfirmedCasesByCounties,
        "dataCumulativeCasesChart": dataCumulativeCasesChart,
        "dataNewCasesPerDayChart": dataNewCasesPerDayChart,
        "dataCumulativeTestsChart": dataCumulativeTestsChart,
        "dataTestsPerDayChart": dataTestsPerDayChart,
        "dataPositiveTestsByAgeChart": dataPositiveTestsByAgeChart,
        "dataPositiveNegativeChart": dataPositiveNegativeChart
    }

    # dump json output
    with open(OUTPUT_FILE_LOCATION, "w", encoding="utf-8") as f:
        json.dump(finalJson, f, cls=NpEncoder, ensure_ascii=False)
