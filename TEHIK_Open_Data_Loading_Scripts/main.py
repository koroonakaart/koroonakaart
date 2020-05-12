import json
import requests
from constants import county_mapping, county_sizes, counties, age_groups
from chart_data_functions import *
from helpers import NpEncoder


######## CONFIGURE MANUAL DATA ########
MANUAL_DATA = {
    "updatedOn": "12/05/2020, 11:00",
    "hospitalisedNumber": 48,
    "deceasedNumber": 61,
    "recoveredNumber": 289,
    "datesEnd": "2020-05-11 ",
    "dates1Start": "2020-03-15",
    "dates2Start": "2020-02-25",
    "recovered": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                 1, 1, 1, 1, 1, 2, 2, 4, 7, 8, 8, 11, 11, 20, 20,
                 20, 26, 33, 45, 48,59, 62, 62, 69, 72, 83, 93, 93,98,
                 102, 115,117,133,145,162,164,165,169,184,192,206,228,233,
                 233,240, 236, 249, 253, 256, 259,259,261,264,273, 277,285,285, 287,289],
    "deceased": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 1, 1, 1, 1, 3, 3, 4, 5, 11, 12,13, 15, 19,
                 21, 24, 24,24, 24,25, 27,31,35,36,38,38,40,40,43,44,45,46,
                 47,50,52,52, 52, 54, 54,55, 57,57,57,57,59, 59,60, 60,61, 61],
    "hospitalised": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 0, 2, 3, 3, 3, 8, 10, 14, 15, 17, 28, 29, 34,
                     40, 48, 56, 79, 91, 95, 85, 90,113, 130, 129,
                     130, 139, 134,138, 146,153, 157, 146,147,137,129,
                     122,125,128,124, 114,109,103,99,94,95,91, 89, 75,
                     72,74, 75,77, 70,67,61, 58,49, 51,48, 48],
    "intensive": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 2, 4, 6, 7, 7, 7, 7, 10, 10,
                  13, 13, 15, 16, 16,20, 17, 14, 12, 11, 9, 9, 11,11,
                  9, 11,10,10,11,11,10,9,9, 7,7,6,6,6,7,9, 10, 9, 7,7,
                   7,6, 6,4,4, 5,5, 5, 5, 5]
}

######## CONFIGURE IO LOCATIONS ########
API_ENDPONT = "https://opendata.digilugu.ee/opendata_covid19_test_results.json"
OUTPUT_FILE_LOCATION = "../koroonakaart/src/data.json"

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
    hospitalChanged = MANUAL_DATA["hospitalised"][-1] - MANUAL_DATA["hospitalised"][-2]
    deceasedChanged  = MANUAL_DATA["deceased"][-1] - MANUAL_DATA["deceased"][-2]
    recoveredChanged = MANUAL_DATA["recovered"][-1] - MANUAL_DATA["recovered"][-2]

    # Find count of confirmed cases
    confirmedCasesNumber = np.sum([res["ResultValue"] == "P" for res in json_data])

    # Find total number of tests
    testsAdministeredNumber = len(json_data)

    # Calculate active number of cases

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
    dataCountyDailyActive = getdataCountyDailyActive(json_copy,dates2,county_mapping)
    activeCasesNumber = dataCumulativeCasesChart["active"][-1]
    activeChanged = dataCumulativeCasesChart["active"][-1] - dataCumulativeCasesChart["active"][-2]
    dataActiveInfectionsByCounty = [[k, v[-1]] for k,v in dataCountyDailyActive.items()]


    # Create dictionary for final json
    finalJson = {
        "updatedOn": updatedOn,
        "confirmedCasesNumber": str(confirmedCasesNumber),
        "activeCasesNumber": str(activeCasesNumber),
        "hospitalisedNumber": str(hospitalisedNumber),
        "deceasedNumber": str(deceasedNumber),
        "recoveredNumber": str(recoveredNumber),
        "testsAdministeredNumber": str(testsAdministeredNumber),
        "hospitalChanged": str(hospitalChanged),
        "deceasedChanged": str(deceasedChanged),
        "recoveredChanged": str(recoveredChanged),
        "activeChanged": str(activeChanged),
        "dates1": list(map(lambda x: str(x.date()), dates1)),
        "dates2": list(map(lambda x: str(x.date()), dates2)),
        "counties": counties,
        "age_groups": age_groups,
        "dataInfectionsByCounty": dataInfectionsByCounty,
        "dataInfectionsByCounty10000": dataInfectionsByCounty10000,
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
        "dataPositiveNegativeChart": dataPositiveNegativeChart
    }

    # dump json output
    with open(OUTPUT_FILE_LOCATION, "w", encoding="utf-8") as f:
        json.dump(finalJson, f, cls=NpEncoder, ensure_ascii=False)
