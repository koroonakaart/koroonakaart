import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date
from collections import defaultdict
import pprint


def getHospitalData(json_hospital, startDate):
    hospitalizations = []
    activehospitalizations = []
    intensive = []
    discharged = []
    startDate = datetime.strptime(startDate, '%Y-%m-%d')
    for result in json_hospital:
        statisticsDate = datetime.strptime(result["StatisticsDate"].split('T')[0], '%Y-%m-%d')
        if statisticsDate >= startDate:
            hospitalizations += [int(result["Hospitalised"])]
            activehospitalizations += [int(result["ActivelyHospitalised"])]
            if result["IsInIntensive"] != None:
                intensive += [int(result["IsInIntensive"])]
            else:
                intensive += [result["IsInIntensive"]]
            discharged += [int(result["TotalCasesDischarged"])]
    hospital_results = {
    "hospitalizations": hospitalizations,
    "activehospitalizations": activehospitalizations,
    "intensive": intensive,
    "discharged": discharged
    }
    return hospital_results


def getMunicipalityData(json_municipalities, county_mapping):
    municipalities_array = []
    yesterday = datetime.strftime(datetime.today() - timedelta(1), '%Y-%m-%d')
    communes_that_are_summed = ['Tallinn', 'Pärnu linn', 'Saaremaa vald']
    communes_that_are_summed_data = {}
    for result in json_municipalities:
        if result["StatisticsDate"] == yesterday and result["ResultValue"] == "P":
            if result["Commune"] in communes_that_are_summed:
                if result["Commune"] in communes_that_are_summed_data:
                    communes_that_are_summed_data[result["Commune"]]["range_start"] += result["TotalCasesFrom"]
                    communes_that_are_summed_data[result["Commune"]]["range_end"] += result["TotalCasesTo"]
                else:
                    communes_that_are_summed_data[result["Commune"]] = {
                        "range_start": result["TotalCasesFrom"],
                        "range_end": result["TotalCasesTo"],
                        "County": county_mapping[result["County"]],
                        "Commune": result["Commune"],
                        "ResultValue": result["ResultValue"]
                    }
            else:
                county = county_mapping[result["County"]]
                municipalities_array.append([county, result["Commune"], result["Village"], result["ResultValue"],result["TotalCasesFrom"], result["TotalCasesTo"]])

    for commune_index in communes_that_are_summed_data:
        commune = communes_that_are_summed_data[commune_index]
        if (commune["range_end"] > 0):
                municipalities_array.append([commune["County"], commune["Commune"], "", commune["ResultValue"], commune["range_start"], commune["range_end"]])

    municipalities_json = {
        "municipalitiesData": municipalities_array
    }
    return municipalities_json


def getCountInfectionsByCounty(json, county_mapping) -> list:
    # Ordering of counties for chart
    map_counties = ["Harjumaa", "Hiiumaa", "Ida-Virumaa", "Jõgevamaa", "Järvamaa", "Läänemaa",
                    "Lääne-Virumaa", "Põlvamaa", "Pärnumaa", "Raplamaa", "Saaremaa", "Tartumaa",
                    "Valgamaa", "Viljandimaa", "Võrumaa"]

    # For performance, hashing
    set_map_counties = set(map_counties)

    counts = defaultdict(int)

    for res in json:
        # Check if test positive
        if res["ResultValue"] == "P":
            # Get county and map it, exclude unknown ones
            county = county_mapping[res["County"]]
            if county in set_map_counties:
                counts[county] += 1

    # Create list of lists as in current json
    result_array = [[county, counts[county], county] for county in map_counties]

    return result_array


def getDataInfectionsByCount10000(infectionsByCounty, county_sizes):
    return [[county, round(value / county_sizes[county] * 10000, 2), county] for county, value, county in infectionsByCounty]


def getDataTestsPopRatio(dataInfectionsByCounty10000):
    # Just extract pop ratios
    return [v for k, v, k in dataInfectionsByCounty10000]


def getCountyByDay(json, dates, county_mapping, county_sizes):
    chart_counties = ["Harjumaa", "Hiiumaa", "Ida-Virumaa", "Jõgevamaa", "Järvamaa", "Läänemaa",
                      "Lääne-Virumaa", "Põlvamaa", "Pärnumaa", "Raplamaa", "Saaremaa", "Tartumaa",
                      "Valgamaa", "Viljandimaa", "Võrumaa"]

    county_date_counts = defaultdict(int)

    for res in json:
        if res["ResultValue"] == "P":
            date = pd.to_datetime(res["StatisticsDate"]).date()
            county = county_mapping[res["County"]]
            if county in chart_counties:
                county_date_counts[(county, str(date))] += 1

    countyByDay = {}
    mapPlayback = []
    mapPlayback10k = []
    for county in chart_counties:
        per_day_county = []
        per_day_county_10k = []
        for date in dates:
            val = county_date_counts[(county, str(date.date()))]
            per_day_county.append(val)
            per_day_county_10k.append((val/county_sizes[county] * 10000))

        mapPlayback.append({"MNIMI": county, "sequence": list(np.cumsum(per_day_county)), "drilldown": county})
        mapPlayback10k.append({"MNIMI": county, "sequence": list(np.round(np.cumsum(per_day_county_10k),2)), "drilldown": county})
        # Calculate cumulative
        countyByDay[county] = list(np.cumsum(per_day_county))

    countyByDayNew = [countyByDay[county][-1] - countyByDay[county][-2] for county in chart_counties]

    countyList = {
        "countyByDay": countyByDay,
        "countyByDayNew": countyByDayNew,
        "mapPlayback": mapPlayback
        ,
        "mapPlayback10k": mapPlayback10k
        }

    return countyList


def getdataCountyDailyActive(json, dates, county_mapping,county_sizes):
    chart_counties = ["Harjumaa", "Hiiumaa", "Ida-Virumaa", "Jõgevamaa", "Järvamaa", "Läänemaa",
                      "Lääne-Virumaa", "Põlvamaa", "Pärnumaa", "Raplamaa", "Saaremaa", "Tartumaa",
                      "Valgamaa", "Viljandimaa", "Võrumaa"]

    county_date_counts = defaultdict(int)

    for res in json:
        if res["ResultValue"] == "P":
            date = pd.to_datetime(res["StatisticsDate"]).date()
            county = county_mapping[res["County"]]
            if county in chart_counties:
                county_date_counts[(county, str(date))] += 1

    countyByDay = {}
    activeMap100kPlayback = []
    countyByDayActivePercentage = {}
    mapCountyByDayActivePercentage = []

    for county in chart_counties:
        per_day_county = []
        active_per_day_county_100k = []
        per_day_county_active_percent = []
        for date in dates:
            val = county_date_counts[(county, str(date.date()))]
            per_day_county.append(val)
            active_per_day_county_100k.append((val/county_sizes[county] * 100000))
            per_day_county_active_percent.append((val * 100 / county_sizes[county]))

        # Calculate cumulative
        countyByDay[county] = list(map(int, pd.Series(per_day_county).rolling(14, min_periods=0).sum()))
        activeMap100kPlayback.append({"MNIMI": county, "sequence": list(round(pd.Series(active_per_day_county_100k).rolling(14, min_periods=0).sum(),2)), "drilldown": county})
        countyByDayActivePercentage[county] = list(round(pd.Series(per_day_county_active_percent).rolling(14, min_periods=0).sum(),2))
        mapCountyByDayActivePercentage.append({"MNIMI": county, "sequence": list(round(pd.Series(per_day_county_active_percent).rolling(14, min_periods=0).sum(),2)), "drilldown": county})
        activeList ={
        "countyByDayActive": countyByDay
        ,
        "activeMap100kPlayback": activeMap100kPlayback,
        "countyByDayActivePercentage": countyByDayActivePercentage,
        "mapCountyByDayActivePercentage": mapCountyByDayActivePercentage
        }

    return activeList


def getDataConfirmedCasesByCounties(json, county_mapping):
    chart_counties = ["Harjumaa", "Hiiumaa", "Ida-Virumaa", "Jõgevamaa", "Järvamaa", "Läänemaa",
                      "Lääne-Virumaa", "Põlvamaa", "Pärnumaa", "Raplamaa", "Saaremaa", "Tartumaa",
                      "Valgamaa", "Viljandimaa", "Võrumaa", "Info puudulik"]

    # Count totals for every county
    counts = defaultdict(int)

    for res in json:
        if res["ResultValue"] == "P":
            county = county_mapping[res["County"]]
            counts[county] += 1

    return [counts[county] for county in chart_counties]


def getDataNewCasesPerDayChart(data):
    cases = np.diff(data["cases"], prepend=0)
    recovered = np.diff(data["recovered"], prepend=0)
    deceased = np.diff(data["deceased"], prepend=0)

    dataNewCasesPerDayChart = {
        "confirmedCases": list(cases),
        "recovered": list(recovered),
        "deceased": list(deceased)
    }

    return dataNewCasesPerDayChart


def getDataCumulativeTestsChart(json, dates):
    # Count totals for every day
    date_counts = defaultdict(int)

    dates_within_range = set([str(date.date()) for date in list(dates)])

    date_start = str(dates[0].date())

    count_before_date_range = 0

    for res in json:
        date = str(pd.to_datetime(res["StatisticsDate"]).date())
        if date in dates_within_range:
            date_counts[date] += 1
        elif date < date_start:
            # Hack to count dates before our range
            count_before_date_range += 1

    tests = []
    for date in dates:
        tests.append(date_counts[str(date.date())])

    # Add everything before first date to first date
    tests[0] += count_before_date_range

    return_json = {
        "testsAdminstered": list(np.cumsum(tests))
    }

    return return_json


def getDataTestsPerDayChart(json, dates):
    # Count totals for every day
    date_counts = defaultdict(int)
    date_positive = defaultdict(int)

    dates_within_range = set([str(date.date()) for date in list(dates)])

    date_start = str(dates[0].date())

    count_before_date_range = 0
    count_positive_before_date_range = 0

    for res in json:
        date = str(pd.to_datetime(res["StatisticsDate"]).date())
        if date in dates_within_range:
            date_counts[date] += 1
            if res["ResultValue"] == "P":
                date_positive[date] += 1
        elif date < date_start:
            # Hack to count dates before our range
            count_before_date_range += 1
            if res["ResultValue"] == "P":
                count_positive_before_date_range += 1

    tests = []
    positive_tests = []
    for date in dates:
        tests.append(date_counts[str(date.date())])
        positive_tests.append(date_positive[str(date.date())])


    # Add everything before first date to first date
    tests[0] += count_before_date_range
    positive_tests[0] += count_positive_before_date_range
    positive_test_percentage = list(np.round(np.array(positive_tests) / np.array(tests) * 100, 2)),
    return_json = {
        "positiveTestsPerDay": positive_tests,
        "negativeTestsPerDay": list(np.array(tests) - np.array(positive_tests)),
        "positiveTestsPercentage": positive_test_percentage[0],
        "positiveTestAverage14Percent": np.round(np.average(positive_test_percentage[0][-14:]),2)

        }

    return return_json


def getDataCumulativeCasesChart(json, recovered_list, deceased_list, hospitalised, intensive, onventilation, dates):
    date_counts = defaultdict(int)
    andmed = getDataTestsPerDayChart(json,dates)
    for res in json:
        if res["ResultValue"] == "P":
            date = pd.to_datetime(res["StatisticsDate"]).date()
            date_counts[str(date)] += 1

    confirmed_cases = []

    for date in dates:
        confirmed_cases.append(date_counts[str(date.date())])

    cases = np.cumsum(confirmed_cases)
    recovered = recovered_list
    deceased = deceased_list
    intensive = intensive
    hospitalised = hospitalised
    onventilation = onventilation


    new_cases_14 = [andmed["positiveTestsPerDay"][0]]
    for i in range(1,14):
        new_cases_14.append(new_cases_14[i-1] + andmed["positiveTestsPerDay"][i])

    for i in range(14, len(andmed["positiveTestsPerDay"])):
        new_cases_14.append(new_cases_14[i-1] - andmed["positiveTestsPerDay"][i-14]  + andmed["positiveTestsPerDay"][i])

    estonian_population = 1_328_976 # from https://www.stat.ee/en/find-statistics/statistics-theme/population/population-figure
    per_100_k_multiplier = 100_000 / estonian_population
    new_cases_14_per_100_k = [round(active_cases * per_100_k_multiplier, 2) for active_cases in new_cases_14]

    dataCumulativeCasesChart = {
        "cases": list(cases),
        "recovered": recovered_list,
        "active": new_cases_14,
        "active100k": new_cases_14_per_100_k,
        "deceased": deceased_list,
        "haiglas": hospitalised,
        "intensive": intensive,
        "onventilation": onventilation
    }

    return dataCumulativeCasesChart


def getDataPositiveTestsByAgeChart(json):
    results = [d["ResultValue"] for d in json]
    genders = [d["Gender"] for d in json]
    age_groups = [d["AgeGroup"] for d in json]

    df = pd.DataFrame({
        "Gender": genders,
        "AgeGroup": age_groups,
        "ResultValue": results
    })

    pos_results = df[df.ResultValue == "P"].groupby(["Gender", "AgeGroup"]).count()
    neg_results = df[df.ResultValue == "N"].groupby(["Gender", "AgeGroup"]).count()

    pos_results.rename(columns={
        "ResultValue": "Positive"
    }, inplace=True)

    neg_results.rename(columns={
        "ResultValue": "Negative"
    }, inplace=True)

    end_df = pos_results.join(neg_results, how="outer")
    end_df.fillna(0, inplace=True)
    end_df["Positive"] = end_df[["Positive"]].astype('int')

    male_order = [
        ('M', '0-4'),
        ('M', '5-9'),
        ('M', '10-14'),
        ('M', '15-19'),
        ('M', '20-24'),
        ('M', '25-29'),
        ('M', '30-34'),
        ('M', '35-39'),
        ('M', '40-44'),
        ('M', '45-49'),
        ('M', '50-54'),
        ('M', '55-59'),
        ('M', '60-64'),
        ('M', '65-69'),
        ('M', '70-74'),
        ('M', '75-79'),
        ('M', '80-84'),
        ('M', 'üle 85')
    ]

    female_order = [
        ('N', '0-4'),
        ('N', '5-9'),
        ('N', '10-14'),
        ('N', '15-19'),
        ('N', '20-24'),
        ('N', '25-29'),
        ('N', '30-34'),
        ('N', '35-39'),
        ('N', '40-44'),
        ('N', '45-49'),
        ('N', '50-54'),
        ('N', '55-59'),
        ('N', '60-64'),
        ('N', '65-69'),
        ('N', '70-74'),
        ('N', '75-79'),
        ('N', '80-84'),
        ('N', 'üle 85')
    ]

    # Create male positive and negative lists
    malePositive = []
    maleNegative = []
    femalePositive = []
    femaleNegative = []
    for i in range(len(male_order)):
        malePositive.append(end_df.loc[male_order[i], "Positive"])
        maleNegative.append(end_df.loc[male_order[i], "Negative"])
        femalePositive.append(end_df.loc[female_order[i], "Positive"])
        femaleNegative.append(end_df.loc[female_order[i], "Negative"])
    femaleTotal = sum(femalePositive) + sum(femaleNegative)
    maleTotal = sum(malePositive) + sum(maleNegative)
    malePositiveTotal = sum(malePositive)
    femalePositiveTotal = sum(femalePositive)
    maleNegativeTotal = sum(maleNegative)
    femaleNegativeTotal = sum(femaleNegative)

    end_result = {
        "malePositive": malePositive,
        "maleNegative": maleNegative,
        "maleTotal": maleTotal,
        "malePositiveTotal": malePositiveTotal,
        "maleNegativeTotal": maleNegativeTotal,
        "femalePositive": femalePositive,
        "femaleNegative": femaleNegative,
        "femaleTotal": femaleTotal,
        "femalePositiveTotal": femalePositiveTotal,
        "femaleNegativeTotal": femaleNegativeTotal
    }

    return end_result


def getDataPositiveNegativeChart(json, mapping):
    """
    Compile data for the "Positive and negative tests by county" chart.
    """

    # Define counties (in order)
    chart_counties = ["Info puudulik", "Harjumaa", "Hiiumaa", "Ida-Virumaa", "Jõgevamaa", "Järvamaa", "Läänemaa",
                      "Lääne-Virumaa", "Põlvamaa", "Pärnumaa", "Raplamaa", "Saaremaa", "Tartumaa",
                      "Valgamaa", "Viljandimaa", "Võrumaa"]

    results = [d["ResultValue"] for d in json]
    county = [mapping[d["County"]] for d in json]

    df = pd.DataFrame({
        "County": county,
        "ResultValue": results
    })

    pos_results = df[df.ResultValue == "P"].groupby("County").count()
    neg_results = df[df.ResultValue == "N"].groupby("County").count()

    pos_results.rename(columns={
        "ResultValue": "Positive"
    }, inplace=True)

    neg_results.rename(columns={
        "ResultValue": "Negative"
    }, inplace=True)

    end_df = pos_results.join(neg_results, how="outer")
    end_df.fillna(0, inplace=True)
    end_df["Positive"] = end_df[["Positive"]].astype('int')

    county_positive = []
    county_negative = []
    for order in chart_counties:
        county_positive.append(end_df.loc[order, "Positive"])
        county_negative.append(end_df.loc[order, "Negative"])

    end_output = {
        "negative": county_negative,
        "positive": county_positive
    }

    return end_output

def getDataVaccinatedPeopleChart(json, dates):
    date_counts_progress = defaultdict(int)
    date_counts_completed = defaultdict(int)
    date_counts = defaultdict(int)

    dates_within_range = set([str(date.date()) for date in list(dates)])
    date_start = str(dates[0].date())

    json_progress = [x for x in json if x['VaccinationStatus'] == 'InProgress']
    json_completed = [x for x in json if x['VaccinationStatus'] == 'Completed']

    for res in json:
        date = str(pd.to_datetime(res["StatisticsDate"]).date())
        if date in dates_within_range:
            if res['VaccinationStatus'] == 'Completed':
                date_counts_progress[date] -= res["DailyCount"]
            elif res['VaccinationStatus'] == 'InProgress':
                date_counts_progress[date] += res["DailyCount"]
    for res in json_completed:
        date = str(pd.to_datetime(res["StatisticsDate"]).date())
        if date in dates_within_range:
            date_counts_completed[date] += res["DailyCount"]
    for res in json_progress:
        date = str(pd.to_datetime(res["StatisticsDate"]).date())
        if date in dates_within_range:
            date_counts[date] += res["DailyCount"]

    vacc_progress = []
    vacc_completed = []
    vacc = []

    for date in dates:
        vacc_progress.append(date_counts_progress[str(date.date())])
        vacc_completed.append(date_counts_completed[str(date.date())])
        vacc.append(date_counts[str(date.date())])

    return_json = {
        "vaccinesProgress": list(np.cumsum(vacc_progress)),
        "vaccinesCompleted": list(np.cumsum(vacc_completed)),
        "vaccinesAll": list(np.cumsum(vacc))
    }

    return return_json

def getInIntensiveData(json, manualData):
    if (type(json) is not list or type(manualData) is not dict):
        return False

    data = getDictWithDatesAndKey(json, 'IsInIntensive')

    output = manualData

    for day in data:
        if isinstance(data[day], str):
            output[day] = int(data[day])
    return output

def getOnVentilationData(json):
    if type(json) is not list:
        return False

    output = {}

    data = getDictWithDatesAndKey(json, 'IsOnVentilation')

    for day in data:
        if data[day] is None:
            data[day] = "0"
        if isinstance(data[day], str):
            output[day] = int(data[day])
    return output

def getDictWithDatesAndKey(json, key):
    days = {}

    for day in json:
        date = day['StatisticsDate'].split('T')[0]
        data = day[key]
        days[date] = data

    return days

def mergeDateDictionaries(dict1, dict2):
    output = dict1
    for index in dict2:
        output[index] = dict2[index]
    return output