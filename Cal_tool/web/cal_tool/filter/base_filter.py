class base_filter:
    def filter_calendar_source(self, p_calendar):
        pass

    def save_to_database(self, p_cal_source_id):
        pass

    def load_from_database(self, p_filter_id):
        pass

    def load_base_filter(self, p_filter_id):
        db_filter = Filters.objects.filter(filter_id=int(p_filter_id))[0]
        attributes = FilterAttributes.objects.filter(filter_id=db_filter)
        for attribute in attributes:
            if self.__check_UHasselt(attribute.type):
                return False

        return True

    def __check_UHasselt(self, p_attribute):
        if p_attribute == "AttributeType.PROF":
            return True
        elif p_attribute == "AttributeType.COURSE":
            return True
        elif p_attribute == "AttributeType.COURSENUMBER":
            return True
        elif p_attribute == "AttributeType.ROOM":
            return True
        elif p_attribute == "AttributeType.TYPE":
            return True
        elif p_attribute == "AttributeType.GROUP":
            return True
        else:
            return False

from cal_tool.models import Filters, FilterAttributes