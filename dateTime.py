#! /usr/bin/python3
from datetime import datetime, timedelta
from pytz import timezone
import pytz
from datetime import date
import calendar

def getTime():
    now = datetime.now(pytz.timezone("Europe/Berlin"))
    #now = datetime.utcnow()
    myTimeZone = " MEST"
    mm = str(now.month)
    dd = str(now.day)
    yyyy = str(now.year)
    hour = str(now.hour)
    minute = str(now.minute)
    if now.minute < 10:
        minute = '0' + str(now.minute)
    second = str(now.second)
    mydate = date.today()
    #if now.hour >= 12:
    #    ampm = ' PM'
    #else:
    #    ampm = ' AM'
    #if now.hour > 12:
    #    hour = str(now.hour - 12)
    weekday = calendar.day_name[mydate.weekday()]
    return "It is " + hour + ":" + minute

def getDate():
    now = datetime.now(pytz.timezone("Europe/Berlin"))
    mm = now.month
    dd = now.day
    yyyy = str(now.year)
    hour = str(now.hour)
    minute = str(now.minute)
    second = str(now.second)
    weekday = now.weekday()
    week = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    year = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    day = str(dd);
    if dd == 1:
        day += 'st'
    elif dd == 2:
        day += 'nd'
    else:
        day += 'th'
    weekdayName = week[weekday]
    return "Today is " + weekdayName + ", " + year[mm] + " " + day + ", " + yyyy

##print("Hello there!") Obi Wan Kenobi referenz ;)
print("Hallo!")
print(getTime())
print(getDate())
