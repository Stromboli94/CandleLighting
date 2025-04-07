import hdate, datetime
from location import latitude, longitude, timezone, altitude, diaspora, language

def get_plag_times(tod, c):
    #get date of previous Sunday. Returns today if it is Sunday
    tod = tod - datetime.timedelta(days = (tod.weekday() + 1) % 7)
    times = []
    for i in range(5):
        day = tod + datetime.timedelta(days = i)
        z = hdate.Zmanim(date = day, location = c, language = language, candle_lighting_offset = 18, havdalah_offset = 50).plag_hamincha.local.time()
        times.append(z)
        print(f'{day}, {day.strftime('%A')}, {z}')
    return times

def get_mincha_time(t):
    t = datetime.datetime.combine(t['day'], t['time'])
    delta = t.minute % 5
    t = t.replace(second = 0) - datetime.timedelta(minutes = 10 + delta)
    return t

c = hdate.Location(name = "home", latitude = latitude, longitude = longitude, timezone = timezone, altitude = altitude, diaspora = diaspora)
tod = datetime.date.today()
#tod = datetime.date(year=2025, month= 2, day= 9)
get_plag_times(tod, c)
