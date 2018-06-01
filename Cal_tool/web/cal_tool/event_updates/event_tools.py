class InvalidEvent(Exception):
    def __init__(self, p_value):
        self.__value = p_value

    def __str__(self):
        return repr(self.__value)


class event_tools:
    @staticmethod
    def test_valid_event(p_event):
        """
        Test if p_event is valid
        :param p_event: Event to check validity of
        :return:        If valid: returns True, else: False
        """
        # If p_event has no start, but it has an end; then it is INVALID
        if event_tools.get_event_start(p_event) is not None and event_tools.get_event_end(p_event) is None:
            return False
        return True


    @staticmethod
    def get_event_start(p_event):
        """
        Returns start of event
        :param p_event: Event to search start from
        :return:    Returns start of the event
                    If the event is recurring, the next occurrence date will be returned
        """
        rrule = p_event.get("RRULE")
        dtstart = p_event.get('DTSTART')
        # TODO: Method to handle recurring events (search first occurrence of next event to occur)
        if dtstart is not None:
            return dtstart
        elif rrule:
            pass
        else:
            raise InvalidEvent("This event has an invalid format")



    @staticmethod
    def get_event_end(p_event):
        dtend = p_event.get('DTEND')        # Get dtend
        if dtend is not None :
            return dtend
        duration = p_event.get('DURATION')  # If dtend is not defined, get duration
        return duration

    @staticmethod
    def get_attribute_list(p_event):
        for attribute, value in p_event.items():
            print(attribute, value)


#from cal_tool.utilities.fuzzy_string_matching import string_matching_factory
#from icalendar import Event



