from cal_tool.calendar.calendar_io import calendar_io_factory
import datetime, pytz

io = calendar_io_factory.get_strategy()

a = io.parse_file("./test_calendars/event_change_v1.ics")
b = io.parse_file("./test_calendars/event_change_v2.ics")

# a.remove_duplicates()
# print("stuff")

t = datetime.datetime(2003, 8, 4, 12, 30, 45)
print(t)





