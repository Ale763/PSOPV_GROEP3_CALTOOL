from cal_tool.calendar.calendar_io import calendar_io_factory
from cal_tool.event_updates.event_change_strategy import event_change_factory

io = calendar_io_factory.get_strategy()

a = io.parse_file("./test_calendars/event_change_v1.ics")
b = io.parse_file("./test_calendars/event_change_v2.ics")

evc = event_change_factory.get_strategy()
del_ev, mod_ev, add_ev = evc.check_for_events(a,b)
print("SUCCESFULL")
