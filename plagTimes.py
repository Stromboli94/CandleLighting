import hdate, datetime
from location import latitude, longitude, timezone, altitude, diaspora, hebrew

def get_plag_times(tod, c):
    #get date of previous Sunday. Returns today if it is Sunday
    tod = tod - datetime.timedelta(days = (tod.weekday() + 1) % 7)
    times = []
    for i in range(5):
        day = tod + datetime.timedelta(days = i)
        z = hdate.Zmanim(date = day, location = c, hebrew = False).zmanim["plag_mincha"].time()
        times.append(z)
        print(f'{day}: {z}')
    return times

def get_mincha_time(t):
    t = datetime.datetime.combine(t['day'], t['time'])
    delta = t.minute % 5
    t = t.replace(second = 0) - datetime.timedelta(minutes = 10 + delta)
    return t

c = hdate.Location(name = "home", latitude = latitude, longitude = longitude, timezone = timezone, altitude = altitude, diaspora = diaspora)
tod = datetime.date.today()
get_plag_times(tod, c)
