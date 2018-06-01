from enum import Enum, auto

class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
         return name

class AttributeType(AutoName):
    LOCATION = auto()
    SUMMARY = auto()
    DESCRIPTION = auto()
    DTSTART = auto()
    DTEND = auto()
    STATUS = auto()
    CLASS = auto()
    PRIORITY = auto()
    ORGANIZER = auto()
    PROF = auto()
    COURSE = auto()
    COURSENUMBER = auto()
    ROOM = auto()
    TYPE = auto()
    GROUP = auto()

class FilterMode(AutoName):
    CONTAINS = auto()
    EQUAL = auto()

class FilterUHasseltAttribute:
    #p_attributeType is a string
    def __init__(self, p_attribute_type=None, p_mode=None, p_not=None, p_value=None):
        if p_attribute_type != None:
            self.__m_type=AttributeType[p_attribute_type.upper()]
            self.__m_mode = FilterMode[p_mode.upper()]
            self.__m_not=p_not
            self.__m_value=p_value

    def get_type_in_string(self):
        return self.__m_type.value

    def get_mode_in_string(self):
        return self.__m_mode.value

    def get_value(self):
        return self.__m_value

    def get_not(self):
        return self.__m_not

    def set_type(self, p_attribute):
        self.__m_type = AttributeType[p_attribute]

    def load_from_database(self, data):
        self.__m_type = AttributeType[data["type"].split(".")[1]]
        self.__m_mode = FilterMode[data["mode"].split(".")[1]]
        self.__m_not = data["not_value"]
        self.__m_value = data["value"]

    def save_to_database(self, p_filter_db):
        """
        Saving NEW object to database, ONLY FOR NEW OBJECTS
        For existing objects use .save()
        """
        db_filterattribute = FilterAttributes(filter_id = p_filter_db,
                            type = self.__m_type,
                            value = self.__m_value,
                            mode = self.__m_mode,
                            not_value = self.__m_not)

        db_filterattribute.save()

from cal_tool.models import FilterAttributes