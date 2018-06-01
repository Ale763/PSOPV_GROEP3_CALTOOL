from cal_tool.event_updates.merge_strategy import merge_factory
from cal_tool.calendar.calendar_io import calendar_io_factory
from cal_tool.event_updates.event_matching import event_matching_factory
from cal_tool.utilities.fuzzy_string_matching import string_matching_factory
import os

dirname = os.path.dirname(__file__)

io = calendar_io_factory.get_strategy()

cals = []
filename = os.path.join(dirname, 'test_calendars/merge1.ics')
a = io.parse_file(filename)
cals.append(a)
filename = os.path.join(dirname, 'test_calendars/merge2.ics')
b = io.parse_file(filename)
cals.append(b)

default_event_matching = event_matching_factory.get_strategy()
string_matching = string_matching_factory.get_strategy(string_matching_factory.MODIFIED_DAMERAU_LEVENSHTEIN)
fuzzy_attribute_event_matching = event_matching_factory.get_strategy(event_matching_factory.FUZZY_EVENT_MATCHING, string_matching)
merge_strategy = merge_factory.get_strategy(default_event_matching)


result = merge_strategy.merge(cals)
print(result)

