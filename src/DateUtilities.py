from datetime import datetime
import os, csv

monthDayMap = {
    1: 31,
    2: 28,
    3:31,
    4:30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}

def nextMonthGen():
    now = str(datetime.date(datetime.now()))
    year, month, _ = now.split('-')
    year = int(year)
    month = int(month)
    while True:
        if month >= 12:
            month = 1
            year += 1
            yield month, year
        else:
            month += 1
            yield month, year
