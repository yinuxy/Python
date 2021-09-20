import datetime

from borax.calendars.lunardate import LunarDate



today = datetime.date.today()
print(type(today.year), type(today.month), type(today.day))
thisday = LunarDate(today.year,today.month,today.day)
print(thisday, type(thisday))
solardate = thisday.to_solar_date()
print(solardate, type(solardate))


thisbirth = LunarDate(today.year,today.month,today.day)
ssolardate = thisbirth.to_solar_date()
print(ssolardate, type(ssolardate))
