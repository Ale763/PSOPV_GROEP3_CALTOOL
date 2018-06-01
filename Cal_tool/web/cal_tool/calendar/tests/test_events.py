from cal_tool.calendar.calendar_io import default_calendar_io
from cal_tool.event_updates.event_matching import event_matching_factory
from cal_tool.utilities.fuzzy_string_matching import string_matching_factory

d = default_calendar_io()
# cal = d.parse_file("test_calendars/reverse_order.ics")
cal = d.parse_file("test_calendars/duplicates.ics")

e1 = cal.get_event(0)
e2 = cal.get_event(1)
strict_string_matching = event_matching_factory.get_strategy(event_matching_factory.FUZZY_EVENT_MATCHING)
fuzzy_matching = event_matching_factory.get_strategy(event_matching_factory.FUZZY_EVENT_MATCHING, string_matching_factory.MODIFIED_DAMERAU_LEVENSHTEIN)
r = fuzzy_matching.match(e1, e2)
print(r)
# b = d.parse_file("res/b.ics")
# c = d.parse_file("res/3-B-R.ics")
# e = Event()
# e.add('uid', 1)
# e.add('dtstart', datetime(2005,4,4,8,0,0,tzinfo=UTC))
# d = e.items()
#
# for i in e:
#     print("{0}: {1}".format(i, e[i]))
# print()