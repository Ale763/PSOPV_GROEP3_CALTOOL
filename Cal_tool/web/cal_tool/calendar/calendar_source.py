# from enum import Enum
import shutil
from cal_tool.utilities.sorting import sort_factory
from cal_tool.models import CalendarSources, Filters


class calendar_source:
    def __init__(self,
                 p_events=None,
                 p_source_type = CalendarSources.FILE):

        # Settings
        self.__sort_strategy = sort_factory.get_strategy(SORTING_STRATEGY)

        # Event-change-matching strategies
        self.__attribute_em = EventMatchingStrategies.STRICT_EVENT_MATCHING
        self.__weighted_sum_em = event_matching_factory.get_strategy()

        # Event datetime-compare strategy
        self.__datetime_compare_strategy = event_compare_factory.get_strategy(EventCompareStrategies.DATETIME_EVENT_COMPARE)

        # Characteristics
        self.__event_list = p_events
        self.__src_id = None
        if p_events is None:
            p_events = []
        self.__event_list = p_events
        self.__cal_attributes = {}
        self.construct_default_calendar_attributes()
        self.__filter_list = []
        self.__cal_source_id = None

        self.__source_type = p_source_type
        self.__source_location = None
        self.__filtered_source_location = None

        self.__source_url = None
        self.__temp_source_file_location=None

        self.__source_name = ""

    # ------------------------------------------------------------------------------------------------------------------
    # Database

    def save_to_database(self, p_cal_id):
        """
        Saving NEW object to database, ONLY FOR NEW OBJECTS
        For existing objects use .save()
        """
        temp_len = len(ICS_TMP_STORE)
        a = self.__source_location[:temp_len]
        if self.__source_location[:len(ICS_SAVED_STORE)] == ICS_SAVED_STORE:
            temp_len = len(ICS_SAVED_STORE)

        # Save unfiltered source
        filename = self.__source_location[temp_len:]
        shutil.move(self.__source_location, ICS_SAVED_STORE + filename)
        self.__source_location = ICS_SAVED_STORE + filename

        # Save filtered source
        self.apply_filters()
        io = default_calendar_io()
        self.__filtered_source_location = CalendarSources.generate_new_file_name(ICS_SAVED_STORE)
        io.write_to_file(self, self.__filtered_source_location)

        # Translate type
        if self.__source_type == CalendarSources.FILE:
            type = "File"
        else:
            type = "URL"

        if self.__src_id is None:
            self.__src_id = CalendarSources.generate_new_id()

        db_cal_source = CalendarSources(cal_source_id=self.__src_id,
                                        cal_id = p_cal_id,
                                        cal_source_alias = self.__source_name,
                                        source_location = self.__source_location,
                                        filtered_source_location = self.__filtered_source_location,
                                        type = type,
                                        url=self.__source_url)
        db_cal_source.save()

        for filter in self.__filter_list:
            filter.save_to_database(self.__src_id)

    def load_from_database(self, p_cal_source_id, p_refilter=False):
        db_cal = CalendarSources.objects.get(cal_source_id=p_cal_source_id)
        self.__src_id = p_cal_source_id
        self.__cal_source_id = db_cal.cal_source_id
        self.__source_name = db_cal.cal_source_alias
        if db_cal.type == CalendarSources.FILE:
            self.__source_type = CalendarSources.FILE
        else:
            self.__source_type = CalendarSources.URL
        self.__source_location = db_cal.source_location
        self.__filtered_source_location = db_cal.filtered_source_location
        self.__source_url = db_cal.url

        io = default_calendar_io()
        # If calendar has to be refilterd, new filters will be applied, else take filtered location
        if p_refilter:
            temp_cal_src = io.parse_file(self.__source_location)
            temp_cal_src.set_filter_list(self.__filter_list)
            temp_cal_src.apply_filters()
        else:
            temp_cal_src = io.parse_file(self.__filtered_source_location)
        self.__cal_attributes = temp_cal_src.__cal_attributes
        self.__event_list = temp_cal_src.__event_list

        db_filters = Filters.get_filters(db_cal.cal_source_id)

        basefilter = base_filter()

        for db_filter in db_filters:
            id = db_filter.filter_id
            if basefilter.load_base_filter(id):
                filter = Filter()
            else:
                filter = FilterUHasselt()
            filter.load_from_database(db_filter.filter_id)
            self.__filter_list.append(filter)


    # ------------------------------------------------------------------------------------------------------------------
    # Getters & Setters
    def get_id(self):
        return self.__source_url

    def set_filter_list(self, p_filter_list):
        self.__filter_list = p_filter_list

    def get_filter_list(self):
        return self.__filter_list

    def set_source_id(self, p_id):
        self.__src_id = p_id

    def get_source_id(self):
        return self.__src_id

    def get_filtered_source_location(self):
        return self.__filtered_source_location

    def get_filters(self):
        return self.__filter_list

    def set_source_url(self, p_url):
        self.__source_url = p_url

    def get_source_url(self):
        return self.__source_url

    def set_source_name(self, p_source_name):
        self.__source_name = p_source_name

    def get_source_name(self):
        return self.__source_name

    def get_source_type(self):
        return self.__source_type

    def set_source_type(self, p_source_type):
        self.__source_type = p_source_type

    def get_filtered_source_location(self):
        return self.__filtered_source_location

    def set_filtered_source_location(self,p_filtered_source_location):
        self.__filtered_source_location = p_filtered_source_location

    def get_source_location(self):
        return self.__source_location

    def set_source_location(self, p_source_location):
        self.__source_location = p_source_location

    def get_size(self):
        return len(self.__event_list)

    def remove(self, p_index):
        obj = self.__event_list[p_index]
        self.__event_list.remove(obj)

    def add_event(self, p_event):
        """
        Adds p_event to __event_list ONLY IF it is valid
        :param p_event: Event to add to __event_list
        """
        if event_tools.test_valid_event(p_event):
            self.__event_list.append(p_event)

    def add_event_list(self, p_event_list):
        for event in p_event_list:
            if event_tools.test_valid_event(event):
                self.__event_list.append(event)

    def add_multiple_events(self, p_calendar):
        """
        Adds multiple events from p_event_list but ONLY IF the are valid
        :param p_event_list: Events to add to __event_list
        """
        for event in p_calendar.get_event_list():
            self.add_event(event)

    def set_cal_attributes(self, p_attributes):
        """
        Retrieves info from Calendar-object and stores it in __cal_attributes in dictionary format
        :param p_attributes:    Calendar-object containing information about calendar that we need
        """
        temp = {}
        try:
            p_attributes.subcomponents = None
        except AttributeError:
            pass
        for attr in p_attributes:
            temp[attr] = p_attributes.get(attr)
            self.__cal_attributes[attr] = p_attributes.get(attr)

    def get_event(self, p_index):
        """
        :param index:   Index of event to retrieve
        :return:        Requested event at given index, None if index is bigger than list length
        """
        if p_index >= len(self.__event_list):
            return None
        return self.__event_list[p_index]


    def get_event_list(self):
        return self.__event_list

    def set_event_list(self, p_event_list):
        """
        Sets p_event_list as the self.__event_list and checks that every event is valid
        :param p_event_list:
        """
        self.__event_list = []
        for event in p_event_list:
            if event_tools.test_valid_event(event):
                self.__event_list.append(event)


    def add_multiple_filters(self, p_filter_list):
        if p_filter_list is not None:
            for filter in p_filter_list:
                self.__filter_list.append(filter)

    def __set_event_list(self, p_event_list):
        """
        Sets p_event_list as the self.__event_list and does NOT check that every event is valid
        :param p_event_list:
        """
        self.__event_list = p_event_list

    def get_cal_attribute_list(self):
        return self.__cal_attributes


    def get_datetime_compare_strategy(self):
        return self.datetime_compare_strategy


    def set_datetime_compare_strategy(self, p_datetime_compare_strategy):
        """
        Sets datetime_compare_strategy
        :param p_datetime_compare_strategy:    datetime_compare_strategy to set, can't be None
        """
        if p_datetime_compare_strategy is not None:
            self.datetime_compare_strategy = p_datetime_compare_strategy
        else:
            raise AttributeError("""The parameter "p_datetime_compare_strategy" can't be None""")


    # ------------------------------------------------------------------------------------------------------------------

    def copy_calendar_source(self, p_calendar_source):
        self.__cal_source_id = p_calendar_source.get_id()
        self.__source_name = p_calendar_source.get_source_name()
        self.__source_type = p_calendar_source.get_source_type()
        self.__source_location = p_calendar_source.get_source_location()
        self.__filtered_source_location = p_calendar_source.get_filtered_source_location()
        self.__source_url = p_calendar_source.get_source_url()
        #self.add_multiple_filters(p_calendar_source.get_filters())
        self.__cal_attributes = p_calendar_source.get_cal_attribute_list()
        self.__event_list = p_calendar_source.get_event_list()

    def event_list_to_string(self):
        stringlist = []

        for event in self.__event_list:
            event = self.event_to_string(event)
            if event["summary"] is not None:
                stringlist.append(event)

        return stringlist

    def event_to_string(self, p_event):
        try:
            event = {}
            event["start"] = p_event["DTSTART"].dt.strftime("%Y-%m-%d %H:%M:%S")
            event["end"] = p_event["DTEND"].dt.strftime("%Y-%m-%d %H:%M:%S")
            event["summary"] = str(p_event["SUMMARY"].to_ical().decode("unicode-escape")).replace("\\\\", "\\").replace("\;", "").replace("\,", ", ")
            return event
        except KeyError:
            return None


    def sort(self):
        self.__event_list = self.__sort_strategy.sort(self.__event_list, self.__datetime_compare_strategy.compare)


    def apply_filters(self):
        if self.__filter_list == []:
            return
        newCalendar = calendar_source()
        newCalendar.set_event_list(self.__event_list)
        # for event in self.__event_list:
        #     newCalendar.add_event(event)
        self.__event_list = []

        for filter in self.__filter_list:
            valid_events = filter.filter_calendar_source(newCalendar)
            for event in valid_events:
                if event not in self.__event_list:
                    self.add_event(event)

    def apply_time_filter(self, p_filter):
        newCalendar = calendar_source()
        for event in self.__event_list:
            newCalendar.add_event(event)

        p_filter.filter_calendar_source(newCalendar)

        return p_filter.get_time_valid_events()

    def remove_duplicates(self):
            self.sort()
            amount_of_events = self.get_size()
            em = event_matching_factory.get_strategy()
            # Seen that the list is sorted, all the events that are equal will be grouped
            # this way events that are the same will folow eachother, that's why we only have
            # to test for subsequent events
            for i in range(amount_of_events-1):
                current_event = self.__event_list[i]
                next_event = self.__event_list[i+1]
                if em.match(current_event, next_event):
                    self.remove(i+1)
                    i += 1
            self.apply_filters()

    def special_search(self, p_event):
        """
        Searches for index of p_event
        :param p_event: Event to search in self.__event_list
        :return:        If p_event is found, returns index of p_event
                        Else return None
        """
        # Initiate max_match_ratio and index
        max_match_ratio = 0
        index = 0

        # Search every event in self.__event_list for p_event
        for event in self.__event_list:
            # Check first if there is a strict match
            if self.__attribute_em.match(event, p_event):
                return True
            else:
            # If there is no strict match, match based on weighted sum (for changed events)
            # internally the matcher will verify that the match is at least as big as the treshold
                if self.__weighted_sum_em.match(event, p_event):
                    current_match_ratio = self.__weighted_sum_em.get_match_ratio()
                    # If current match is greater than the match found so far, update max_match_ratio
                    if current_match_ratio > max_match_ratio:
                        max_match_ratio = current_match_ratio
            # Update index
            index += 1

        # Verify that max_match_ratio is greater than the treshold
        if max_match_ratio >= self.__weighted_sum_em.get_match_treshold():
            return index
        return None


    def search(self, p_event, p_match):
        """
        Searches for index of p_event
        :param p_match: Matching function to match events
        :param p_event: Event to search in self.__event_list
        :return:        If p_event is found, returns index of p_event
                        Else return None
        """
        index = 0

        # Search every event in self.__event_list for p_event
        for event in self.__event_list:
            if p_match(event, p_event):
                return index
            index += 1
        return None


    def construct_default_calendar_attributes(self):
        """
        Constructs default calendar attributes and adds them to the calendar
        """
        self.__cal_attributes = {"BEGIN": "VCALENDAR",
                                 "VERSION": "2.0",
                                 "PRODID": "Icaller ©2018",
                                 "CALSCALE": "GREGORIAN",
                                 "METHOD": "PUBLISH"}

    def check_for_updates(self):
        pass


from cal_tool.event_updates.event_tools import event_tools
from cal_tool.event_updates.event_compare import event_compare_factory, EventCompareStrategies
from cal_tool.event_updates.event_matching import event_matching_factory, EventMatchingStrategies
from cal_tool.calendar.calendar_io import default_calendar_io
from Project.settings import ICS_TMP_STORE, ICS_SAVED_STORE
from cal_tool.filter.filter import Filter, base_filter
from cal_tool.filter.FilterUHasselt import FilterUHasselt
# from datetime import datetime
# from icalendar import Event
from cal_tool.utilities.sorting import SortStrategies
from cal_tool.event_updates.merge_strategy import MergeStrategies

from Project.settings import FUZZY_STRING_MATCHING_WORD_TRESHOLD, FUZZY_STRING_MATCHING_STRING_TRESHOLD

SORTING_STRATEGY = SortStrategies.DEFAULT_SORT
MERGE_STRATEGY = MergeStrategies.DEFAULT_MERGE
# EVENT_MATCHING_STRATEGY = settings_manager.get_active_event_matching_strategy()
# EVENT_COMPARE_STRATEGY = settings_manager.get_active_event_compare_strategy()