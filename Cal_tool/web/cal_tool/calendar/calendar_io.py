class io_factory:
    DEFAULT = 0
    @staticmethod
    def get_strategy(p_strategy):
        """
        Get strategy for merging
        :param p_event_compare_strategy:
        :param p_merge_strategy:    Strategy-string (has to be one of the possible strategies)
                                    Possible strategies:
                                        1. default_merge_strategy
        :return                     If strategy exists: Strategy instance,else: None
        """
        if p_strategy == io_factory.DEFAULT:
            return default_calendar_io()
        else:
            return None


class CalscaleNotSupported(Exception):
    def __init__(self, p_value):
        self.__value = p_value

    def __str__(self):
        return repr(self.__value)


class CalendarOpeningException(Exception):
    def __init__(self, p_value):
        self.__value = p_value

    def __str__(self):
        return repr(self.__value)


class calendar_io_factory:
    @staticmethod
    def get_strategy(p_strategy="default_calendar_io"):
        """
        Get strategy for calendar_io
        :param strategy:    Strategy-string (has to be one of the possible strategies)
        :return             If strategy exists: Strategy instance,else: None
        """
        if p_strategy == "default_calendar_io":
            return default_calendar_io()
        else:
            return None


class base_calendar_io:
    def parse_file(self, p_source):
        """
        Parse source into a calendar object
        :param p_source:    Source file to retrieve ics information
        :return:            None
        """
        pass


class default_calendar_io(base_calendar_io):
    def parse_file(self, p_path):
        """
        Parse source into a calendar_source object with only event_list, source_location and calendar attributes filled
        :exception:         Throws CalscaleNotSupported if non-supported CALSCALE is used in calendar
        :param p_path:      Source file to retrieve ics file (from local file or url)
        :return:            If source exists and is valid: parsed calendar object, else: None
        """
        try:

            file = self.open_source(p_path, 'rb')
            cal = Calendar.from_ical(file.read())
        except AttributeError:
            raise CalendarOpeningException("The given calendar could not be opened.")

        cal_source = calendar_source()
        for component in cal.walk():
            if component.name == "VEVENT":
                cal_source.add_event(component)
            elif component.name == "VCALENDAR":
                if self.__test_valid_calscale(component.get('CALSCALE')):
                    cal_source.set_cal_attributes(component)
                else:
                    raise CalscaleNotSupported("Only gregorian calendars are supported for now.")
        file.close()
        cal_source.set_source_location(p_path)
        return cal_source

    def write_to_file(self, p_cal, p_path):
        """
        :param p_path:
        :return:
        """
        cal = Calendar()

        # Add Calendar-attributes
        attribute_list = p_cal.get_cal_attribute_list()
        for attribute in attribute_list:
            if attribute == "BEGIN":
                continue
            cal.add(attribute, attribute_list[attribute])

        # Add Events
        for event in p_cal.get_event_list():
            cal.add_component(event)

        # Write to file
        file = self.open_source(p_path, 'wb')
        t = cal.to_ical()
        file.write(t)
        file.close()

    @staticmethod
    def __test_valid_calscale(p_calscale):
        """
        Test if p_calscale is valid (GREGORIAN)
        :param p_calscale:  Calscale to test against
        :return:            True: if valid, else: False
        """
        if p_calscale == "GREGORIAN" or p_calscale is None:
            return True
        return False


    def open_source(self, p_path, p_mode):
        """
        Try to open source file
        :param p_path:      Source file to retrieve ics information
        :return:            If source exists and is valid: opened file, else: None
        """
        try:
            file = open(p_path, p_mode)                 # Try to open local ics-file
        except FileNotFoundError:
            file = self.__open_url(p_path, p_mode)      # Try to open ics-url
        except Exception as e:
            raise e
        return file


    def __open_url(self, p_path, p_mode):
        """
        Try to open remote source file
        :param p_path:    Source file to retrieve ics information
        :return:            If source exists and is valid: opened file, else: None
        """
        try:
            request = urllib.request.Request(p_path)
            response = urllib.request.urlopen(request)
            file = response
            return file
        except Exception as e:
            print(e)
            return None


    def test(self, p1, p2):
        # return self.__open_url(p1, p2)
        pass


import urllib
from urllib.request import urlopen
from icalendar import Calendar, Event
from cal_tool.calendar.calendar_source import calendar_source
