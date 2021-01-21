import json
import requests
import pytz
import sys
from datetime import datetime, timedelta, date, timezone
from constants import county_mapping, county_sizes, counties, age_groups
from chart_data_functions import *
from helpers import NpEncoder
from dateutil.parser import parse as parsedate

estonian_timezone = pytz.timezone('Europe/Helsinki')
today = datetime.today().astimezone(estonian_timezone).strftime('%d/%m/%Y, %H:%M')
yesterday = datetime.strftime(datetime.today() - timedelta(1), '%Y-%m-%d')


######## CONFIGURE MANUAL DATA ########

MANUAL_DATA = {
    "updatedOn": today,
    "deceasedNumber": 125,
    "datesEnd": yesterday,
    "dates1Start": "2020-03-15",
    "dates2Start": "2020-02-26",
    "dates3Start": "2020-12-26",
}


######## CONFIGURE IO LOCATIONS ########

API_ENDPOINT = "https://opendata.digilugu.ee/opendata_covid19_test_results.json"
MUNICIPALITIES_ENDPOINT = "https://opendata.digilugu.ee/opendata_covid19_test_location.json"
HOSPITAL_ENDPOINT = "https://opendata.digilugu.ee/opendata_covid19_hospitalization_timeline.json"
VACCINE_ENDPOINT = "https://opendata.digilugu.ee/opendata_covid19_vaccination_total.json"
MANUAL_DATA_FILE_LOCATION = "../data/manual_data.json"
DEATHS_FILE_LOCATION = "../data/deaths.json"
OUTPUT_FILE_LOCATION = "../data/data.json"


def get_json_data(url) -> any:
    # Open data endpoint
    r = requests.get(url=url)
    return r.json()

def read_json_from_file(path) -> any:
    with open(path) as f:
        data = json.load(f)
    return data

def is_up_to_date(dictionary, key):
    yesterday = datetime.today() - timedelta(1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    file_date_time = datetime.strptime(dictionary[0][key].split('T')[0], '%Y-%m-%d')
    if file_date_time >= yesterday:
        return True
    return False

def is_header_last_modified_up_to_date(url):
    url_date = parsedate(requests.head(url).headers['Last-Modified'])
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
    if url_date > today:
        return True
    return False

if __name__ == "__main__":
    # Get data
    json_data = get_json_data(API_ENDPOINT)
    municipalities = get_json_data(MUNICIPALITIES_ENDPOINT)
    json_hospital = get_json_data(HOSPITAL_ENDPOINT)
    json_vaccine = get_json_data(VACCINE_ENDPOINT)
    json_deaths = read_json_from_file(DEATHS_FILE_LOCATION)
    json_manual = read_json_from_file(MANUAL_DATA_FILE_LOCATION)

    if (not is_up_to_date(municipalities, 'LastStatisticsDate') or
        not is_up_to_date(json_hospital, 'LastLoadStatisticsDate') or
        not is_header_last_modified_up_to_date(MUNICIPALITIES_ENDPOINT)):
        print("One of the TEHIK API has not been updated\n", file=sys.stderr)
        exit()

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

    dates3_range_start = MANUAL_DATA["dates3Start"]
    dates3_range_end = dates_range_end

    # Create date ranges for charts
    dates1 = pd.date_range(start=dates1_range_start, end=dates1_range_end)
    dates2 = pd.date_range(start=dates2_range_start, end=dates2_range_end)
    dates3 = pd.date_range(start=dates3_range_start, end=dates3_range_end)

    # Create copy
    json_copy = json_data
    municipalities_copy = municipalities
    hospital_copy = json_hospital
    hospital = getHospitalData(hospital_copy, dates2_range_start)

    # Set recovered, deceased, hospitalised and ICU time-series
    recovered = hospital["discharged"]
    deceased = list(mergeDateDictionaries(json_manual["deceased"], json_deaths).values())
    hospitalised =  hospital["hospitalizations"]
    intensive = list(getOnVentilationData(json_hospital, json_manual['intensive']).values())
    deceasedNumber = deceased[-1]
    deceasedChanged = int(deceased[-1]) - int(deceased[-2])

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
    dataVaccinatedPeopleChart = getDataVaccinatedPeopleChart(json_vaccine, dates3)
    dataCountyDailyActive = getdataCountyDailyActive(json_copy,dates2,county_mapping,county_sizes)
    activeCasesNumber = dataCumulativeCasesChart["active"][-1]
    activeChanged = dataCumulativeCasesChart["active"][-1] - dataCumulativeCasesChart["active"][-2]
    dataActiveInfectionsByCounty = [{"MNIMI": k, "sequence": v, "drilldown": k} for k,v in dataCountyDailyActive["countyByDayActive"].items()]
    dataActiveInfectionsByCounty100k = [[k, round(v[-1] / county_sizes[k] * 100000, 2)] for k,v in dataCountyDailyActive["countyByDayActive"].items()]
    dataMunicipalities = getMunicipalityData(municipalities_copy, county_mapping)
    perHundred = dataCumulativeCasesChart["active100k"][-1]

    #vaccination data calculation
    lastDayVaccinationData = [x for x in json_vaccine if x['VaccinationStatus'] == 'InProgress'][-1]
    lastDayCompletedVaccinationData = [x for x in json_vaccine if x['VaccinationStatus'] == 'Completed'][-1]
    vaccinationNumberTotal = lastDayVaccinationData["TotalCount"]
    completedVaccinationNumberTotal = lastDayCompletedVaccinationData["TotalCount"]
    completelyVaccinatedFromTotalVaccinatedPercentage = round(completedVaccinationNumberTotal * 100 / (vaccinationNumberTotal + completedVaccinationNumberTotal),2)

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
        "dates3": list(map(lambda x: str(x.date()), dates3)),
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
        "dataVaccinatedPeopleChart": dataVaccinatedPeopleChart,
        "dataMunicipalities": dataMunicipalities,
        "hospital": hospital,
        "vaccinationNumberTotal": vaccinationNumberTotal,
        "vaccinationNumberLastDay": lastDayVaccinationData["DailyCount"],
        "vaccinationPercentage": lastDayVaccinationData["PopulationCoverage"],
        "completedVaccinationNumberTotal": completedVaccinationNumberTotal,
        "completedVaccinationNumberLastDay": lastDayCompletedVaccinationData["DailyCount"],
        "completedVaccinationPercentage": lastDayCompletedVaccinationData["PopulationCoverage"],
        "completelyVaccinatedFromTotalVaccinatedPercentage": completelyVaccinatedFromTotalVaccinatedPercentage
    }

    # Dump json output
    with open(OUTPUT_FILE_LOCATION, "w", encoding="utf-8") as f:
        json.dump(finalJson, f, cls=NpEncoder, ensure_ascii=False)

