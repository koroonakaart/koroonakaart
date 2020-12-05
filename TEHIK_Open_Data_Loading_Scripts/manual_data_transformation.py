import json
import requests
from datetime import datetime, timedelta, date
import pandas as pd
from helpers import NpEncoder


MANUAL_DATA = {
    'datesStart': "2020-02-26",
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

def create_json_from_manual_data(data):
    today = datetime.today().strftime('%d/%m/%Y, %H:%M'),
    yesterday = datetime.strftime(datetime.today() - timedelta(1), '%Y-%m-%d')

    dates_range_start = data["datesStart"]
    dates_range_end = yesterday

    dates = pd.date_range(start=dates_range_start, end=dates_range_end)

    transformedData = {
        'intensive': {},
        'deceased': {}
    }
    i = 0
    arrayLength = len(data['intensive'])
    array2Length = len(data['deceased'])
    for date in dates:
        if (i >= arrayLength or i >= array2Length):
            break
        transformedData['intensive'][str(date.date())] = data['intensive'][i]
        transformedData['deceased'][str(date.date())] = data['deceased'][i]
        i += 1
    return transformedData

def printToJson(fileLocation, dataDict):
    with open(fileLocation, "w", encoding="utf-8") as f:
        json.dump(dataDict, f, cls=NpEncoder, ensure_ascii=False)

printToJson('manual_data.json', create_json_from_manual_data(MANUAL_DATA))