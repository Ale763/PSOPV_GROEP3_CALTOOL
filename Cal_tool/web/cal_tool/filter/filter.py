from .base_filter import base_filter


class Filter(base_filter):
    def __init__(self, p_id=None, p_name=None):
        self.__m_id=p_id
        self.__m_name=p_name
        self.__m_filter_attributes = []
        self.__m_valid_events = []
        self.__m_time_valid_events = 0.0

    def get_id(self):
        return self.__m_id

    def set_name(self):
        return self.__m_name

    def set_name(self, p_newName):
        self.__m_name= p_newName

    def add_attribute(self, p_attribute_type, p_mode, p_not, p_value):
        new_filter_attribute=FilterAttribute(p_attribute_type, p_mode, p_not, p_value)
        self.__m_filter_attributes.append(new_filter_attribute)

    """def add_attribute(self, p_attribute):
        self.__m_filterAttributes.append(p_attribute)"""

    def delete_attribute(self, p_filter_attribute):
        self.__m_filter_attributes.remove(p_filter_attribute)

    def __filter_event(self, p_event):
        for filter_attribute in self.__m_filter_attributes:
            not_boolean=filter_attribute.get_not()
            type=filter_attribute.get_type_in_string().upper()
            value=filter_attribute.get_value()
            mode = filter_attribute.get_mode_in_string()

            if type not in p_event:
                if not not_boolean:
                    return False
                else:
                    continue

            if self.__check_attribute(type, mode, value, p_event, not_boolean):
                continue
            else:
                return False

        return True


    def __check_attribute(self, p_type, p_mode, p_value, p_event, p_not_boolean):
        try:
            if p_type=='DTSTART' or p_type=='DTEND':
                return self.__check_date(p_value, p_type, p_event, p_not_boolean)
            elif (p_event[p_type] == p_value and p_mode is 'EQUAL') or (vText.from_ical(p_event[p_type]) == p_value and p_mode is 'EQUAL'):
                return True and (not p_not_boolean)
            elif (p_value in p_event[p_type] and p_mode is 'CONTAINS') or (vText.from_ical(p_event[p_type]) == p_value and p_mode is 'CONTAINS'):
                return True and (not p_not_boolean)
            else:
                return False or p_not_boolean
        except KeyError:
            return False or p_not_boolean

    def __check_date(self, p_value, p_type, p_event, p_not_boolean):
        event_value = p_event[p_type].dt
        if p_value.date() == event_value.date():
            return True and (not p_not_boolean)
        else:
            return False and (not p_not_boolean)

    def filter_calendar_source(self, p_calendar):
        self.__m_valid_events = []
        for event_index in range(0, p_calendar.get_size()):
            event = p_calendar.get_event(event_index)
            if self.__filter_event(event):
                self.__add_event_to_valid_events(event)

        self.__calc_time_valid_events()

        return self.__m_valid_events

    def __add_event_to_valid_events(self, p_event):
        if not self.__check_for_duplicates(p_event):
            self.__m_valid_events.append(p_event)

    def __check_for_duplicates(self, p_event):
        for event in self.__m_valid_events:
            if event == p_event:
                return True

        return False

    def string_to_datetime(self, p_type, p_value):
        if p_type == "DTSTART" or p_type == "DTEND":
            return datetime.strptime(p_value, '%d %b, %Y')

        else:
            return p_value

    def get_time_valid_events(self):
        return self.__m_time_valid_events

    def __calc_time_valid_events(self):
        for event in self.__m_valid_events:
            if 'DTSTART' not in event or 'DTEND' not in event:
                continue

            start=event['DTSTART'].dt
            end = event['DTEND'].dt
            duration = end-start
            self.__m_time_valid_events += divmod(duration.days * 86400 + duration.seconds, 60)[0]/60

    def load_from_database(self, p_filter_id):
        db_filter = Filters.objects.filter(filter_id=int(p_filter_id)).values()[0]
        self.__m_id = int(p_filter_id)
        self.__m_name = db_filter["name"]

        db_filter = Filters.objects.filter(filter_id=int(p_filter_id))[0]
        attributes = FilterAttributes.objects.filter(filter_id=db_filter).values()
        for attribute in attributes:
            atr = FilterAttribute()
            atr.load_from_database(attribute)
            self.__m_filter_attributes.append(atr)


    def save_to_database(self, p_cal_source_id):
        """
        Saving NEW object to database, ONLY FOR NEW OBJECTS
        For existing objects use .save()
        """
        db_cal_source = CalendarSources.objects.filter(cal_source_id=int(p_cal_source_id))[0]
        db_filter = Filters(filter_id = self.__m_id,
                            name = self.__m_name,
                            cal_source_id = db_cal_source,
                            last_modified = datetime.now())
        db_filter.save()
        for attribute in self.__m_filter_attributes:
            attribute.save_to_database(db_filter)

from .FilterAttribute import FilterAttribute
from datetime import *
from cal_tool.models import Filters, CalendarSources, FilterAttributes
from icalendar import vText