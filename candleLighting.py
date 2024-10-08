import hdate, datetime
from ics import Calendar, Event

c = hdate.Location(name = "home", latitude = 40.6933884, longitude = -73.6580434, timezone = "America/New_York", altitude = 13, diaspora = True)
tod = datetime.date.today()
h = hdate.HDate(tod, diaspora= True, hebrew=False)
hols = h.get_holidays_for_year(types=[hdate.HolidayTypes.EREV_YOM_TOV, hdate.HolidayTypes.YOM_TOV])
rh = hols[1][1]
currentShabbos = rh.upcoming_shabbat
weeks = h.year_size() // 7
cal = Calendar()

# Add holidays to calendar
for hol in hols:
    day = hol[1].gdate
    z = hdate.Zmanim(date = day, location = c, candle_lighting_offset = 18, havdalah_offset = 50, hebrew = False)
    e = Event()
    e.name = hol[0].description[1]
    cl = z.candle_lighting
    if not cl:
        cl = z.havdalah
    elif day.weekday() == 4:
        cl = z.zmanim['sunset'] - datetime.timedelta(minutes = z.candle_lighting_offset)
    e.begin = cl
    e.end = cl
    e.transparent = True
    e.heb = hdate.HDate(z.date, diaspora=True, hebrew=False)
    cal.events.add(e)

# Add Shabbosim to calendar
for i in range(weeks + 1):
    if not currentShabbos.holiday_type in [hdate.HolidayTypes.EREV_YOM_TOV, hdate.HolidayTypes.YOM_TOV]:
        day = currentShabbos.gdate
        z = hdate.Zmanim(date = day, location = c, candle_lighting_offset = 18, havdalah_offset = 50, hebrew = False)
        e = Event()
        e.name = f'Parshat {currentShabbos.parasha}' if currentShabbos.parasha != "none" else "Shabbos Hol HaMoed"
        cl = z.havdalah
        e.begin = cl
        e.end = cl
        e.transparent = True
        e.heb = hdate.HDate(z.date, diaspora=True, hebrew=False)
        cal.events.add(e)
    friday = currentShabbos.previous_day
    if not friday.holiday_type in [hdate.HolidayTypes.EREV_YOM_TOV, hdate.HolidayTypes.YOM_TOV]:
        day = friday.gdate
        z = hdate.Zmanim(date = day, location = c, candle_lighting_offset = 18, havdalah_offset = 50, hebrew = False)
        e = Event()
        e.name = f'Parshat {currentShabbos.parasha}'
        cl = z.candle_lighting
        e.begin = cl
        e.end = cl
        e.transparent = True
        e.heb = hdate.HDate(z.date, diaspora=True, hebrew=False)
        cal.events.add(e)
    currentShabbos = currentShabbos.next_day.upcoming_shabbat

with open("CandleLighting.ics", 'w') as f:
    f.writelines(cal.serialize_iter())

events = sorted(cal.events, key=lambda x: x.begin)
with open('CandleLighting.txt', 'w') as f:
    for e in events:
        f.write(f'{e.name} - {e.begin.strftime("%D - %#I:%M %p")}\n')
        print(f'{e.name} - {e.begin.strftime("%D - %#I:%M %p")}')

