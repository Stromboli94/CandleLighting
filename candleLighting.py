import hdate, datetime
from ics import Calendar, Event
from location import latitude, longitude, timezone, altitude, diaspora, hebrew

c = hdate.Location(name = "home", latitude = latitude, longitude = longitude, timezone = timezone, altitude = altitude, diaspora = diaspora)
tod = datetime.date.today()
h = hdate.HDate(tod, diaspora= diaspora, hebrew=hebrew)
cal = Calendar()
years = 3
for i in range(years):
    hols = h.get_holidays_for_year(types=[hdate.HolidayTypes.EREV_YOM_TOV, hdate.HolidayTypes.YOM_TOV])
    rh = hols[1][1]
    currentShabbos = rh.upcoming_shabbat
    if i < 1:
        erh = (hdate.htables.HOLIDAYS[1], rh.previous_day)
        hols.append(erh)
    weeks = h.year_size() // 7

    # Add holidays to calendar
    for hol in hols:
        day = hol[1].gdate
        z = hdate.Zmanim(date = day, location = c, candle_lighting_offset = 18, havdalah_offset = 50, hebrew = hebrew)
        e = Event()
        e.name = hol[0].description[1]
        cl = z.candle_lighting
        if not cl:
            cl = z.havdalah
            e.name = e.name + " - havdalah"
        elif day.weekday() == 4:
            cl = z.zmanim['sunset'] - datetime.timedelta(minutes = z.candle_lighting_offset)
            e.name = e.name + " - candle lighting"
        else:
            e.name = e.name + " - candle lighting"
        e.begin = cl
        e.end = cl
        e.transparent = True
        e.description = "Generated by https://github.com/Stromboli94/CandleLighting"
        e.heb = hdate.HDate(z.date, diaspora=diaspora, hebrew=hebrew)
        cal.events.add(e)

    # Add Shabbosim to calendar
    for i in range(weeks + 1):
        if not currentShabbos.holiday_type in [hdate.HolidayTypes.EREV_YOM_TOV, hdate.HolidayTypes.YOM_TOV]:
            day = currentShabbos.gdate
            z = hdate.Zmanim(date = day, location = c, candle_lighting_offset = 18, havdalah_offset = 50, hebrew = hebrew)
            e = Event()
            e.name = f'Parshat {currentShabbos.parasha} - havdalah' if currentShabbos.parasha != "none" else "Shabbos Hol HaMoed - havdalah"
            cl = z.havdalah
            e.begin = cl
            e.end = cl
            e.transparent = True
            e.description = "Generated by https://github.com/Stromboli94/CandleLighting"
            e.heb = hdate.HDate(z.date, diaspora=diaspora, hebrew=hebrew)
            cal.events.add(e)
        friday = currentShabbos.previous_day
        if not friday.holiday_type in [hdate.HolidayTypes.EREV_YOM_TOV, hdate.HolidayTypes.YOM_TOV]:
            day = friday.gdate
            z = hdate.Zmanim(date = day, location = c, candle_lighting_offset = 18, havdalah_offset = 50, hebrew = hebrew)
            e = Event()
            e.name = f'Parshat {currentShabbos.parasha} - candle lighting'
            cl = z.candle_lighting
            e.begin = cl
            e.end = cl
            e.transparent = True
            e.description = "Generated by https://github.com/Stromboli94/CandleLighting"
            e.heb = hdate.HDate(z.date, diaspora=diaspora, hebrew=hebrew)
            cal.events.add(e)
        currentShabbos = currentShabbos.next_day.upcoming_shabbat
    h.hdate.year += 1

with open("CandleLighting.ics", 'w') as f:
    f.writelines(cal.serialize_iter())

events = sorted(cal.events, key=lambda x: x.begin)
with open('CandleLighting.txt', 'w') as f:
    for e in events:
        f.write(f'{e.name} - {e.begin.strftime("%D - %#I:%M %p")}\n')
        print(f'{e.name} - {e.begin.strftime("%D - %#I:%M %p")}')

