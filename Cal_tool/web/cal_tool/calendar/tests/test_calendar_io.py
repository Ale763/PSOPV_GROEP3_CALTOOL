from cal_tool.calendar.calendar_io import default_calendar_io


def test1():
    d = default_calendar_io()

    a = d.parse_file("res/1.ics")
    b = d.parse_file("res/b.ics")
    c = d.parse_file("res/3-B-R.ics")
    print()


    # timeit(a)
    d.parse_file("/data/web/cal_tool/calendar/tests/res/1.ics")
    print(d.parse_file("https://alessiotona.duckdns.org/"))
    print(d.test("https://uhcal-api.brentchesny.com/calendars/914103e0-2add-11e8-9ccb-e7919f03e688.ics", 'rb').read())
    open("https://uhcal-api.brentchesny.com/calendars/914103e0-2add-11e8-9ccb-e7919f03e688.ics")


def test2():
    d = default_calendar_io()
    a = d.parse_file("/data/web/cal_tool/calendar/tests/res/1.ics")
    d.write_to_file(a,"/data/web/cal_tool/calendar/tests/res/test")