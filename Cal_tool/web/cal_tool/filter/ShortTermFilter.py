from .base_filter import base_filter
from datetime import *

class ShortTermFilter(base_filter):


    def __init__(self, p_days_to_add):
        self.__m_days=p_days_to_add
        self.__m_valid_events=[]

    def __filter_event(self, p_event):
        return self.__check_date(p_event["DTSTART"].dt) or self.__check_date(p_event["DTEND"].dt)

    def __check_date(self, p_date):
        d = datetime.today() + timedelta(days=self.__m_days)

        # Add timezone support
        today = datetime.today()
        # brussels_tz = pytz.timezone('Europe/Brussels')
        utc = pytz.utc
        if isinstance(p_date, datetime):
            new_datetime = p_date
        else:
            new_datetime = datetime.combine(p_date, datetime.min.time())

        new_datetime = new_datetime.replace(tzinfo=utc)
        today = today.replace(tzinfo=utc)

        return (new_datetime > today and p_date < d)

    def filter_calendar_source(self, p_calendar):
        for event_index in range(0, p_calendar.get_size()):
            event = p_calendar.get_event(event_index)
            if self.__filter_event(event):
                self.__add_event_to_valid_events(event)

        return self.__m_valid_events

    def __add_event_to_valid_events(self, p_event):
        if not self.__check_for_duplicates(p_event):
            self.__m_valid_events.append(p_event)

    def __check_for_duplicates(self, p_event):
        for event in self.__m_valid_events:
            if event == p_event:
                return True

        return False

from datetime import datetime, timedelta
import pytz