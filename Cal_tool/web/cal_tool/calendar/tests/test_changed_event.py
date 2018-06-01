from cal_tool.calendar.calendar_io import *
from cal_tool.event_updates.changed_event import changed_event
io = default_calendar_io()
a = io.parse_file("/data/web/cal_tool/calendar/tests/test_calendars/changed_event.ics")
event_list = a.get_event_list()
p_event1 = event_list[0]
p_event2 = event_list[1]

test = changed_event(p_event1, p_event2)
result = test.parse_changes()

for key, val in result.items():
    print(key, val)
print("DONE")