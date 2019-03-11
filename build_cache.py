from fetch import Reading
from datetime import date, timedelta

i = 0

while(i < 1000):
    reading = Reading(date=date.today() + timedelta(days=i))
    try:
        if not reading.has_file():
            reading.fetch()
            reading.save()
    except Exception:
        print(reading.url)
    i = i + 1
