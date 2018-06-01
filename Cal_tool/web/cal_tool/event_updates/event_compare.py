from enum import Enum


class EventCompareStrategies(Enum):
    DATETIME_EVENT_COMPARE = 0

    @staticmethod
    def get_all():
        result = {}
        for strategy in EventCompareStrategies:
            result[strategy.name] = strategy
        return result

    @staticmethod
    def get_default():
        return EventCompareStrategies.DATETIME_EVENT_COMPARE


class event_compare_factory:
    @staticmethod
    def get_strategy(p_event_compare_strategy=EventCompareStrategies.DATETIME_EVENT_COMPARE):
        """
        Get strategy for event comparing
        :param p_event_compare_strategy:    Strategy-string (has to be one of the possible strategies)
                                            Possible strategies:
                                                1. DATETIME_EVENT_COMPARE
        :return:                            If strategy exists: Strategy instance, else None
        """
        if p_event_compare_strategy == EventCompareStrategies.DATETIME_EVENT_COMPARE:
            return datatime_event_compare()
        else:
            return None


class base_event_compare:
    def compare(self, p_event1, p_event2):
        """
        Compares event1 and event2, based on their start and end date-time
        :param p_event1:
        :param p_event2:
        :return:        Returns an integer based on the equivalentness of the 2 events
                            - If p_event1 starts before p_event2 or if they start on the same moment
                              , but p_event1 finishes before p_event2
                              Return -1
                            - If both events start and stop at the same moment
                              Return 0
                            - Else
                              Return 1
        """
        pass


class datatime_event_compare(base_event_compare):
    """
    Event-matching based on datetime
    """
    def compare(self, p_event1, p_event2):
        """
        Compares event1 and event2, based on their start and end date-time
        :param p_event1:
        :param p_event2:
        :return:        Returns an integer based on the equivalentness of the 2 events
                            - If p_event1 starts before p_event2 or if they start on the same moment
                              , but p_event1 finishes before p_event2
                              Return -1
                            - If both events start and stop at the same moment
                              Return 0
                            - Else
                              Return 1
        """
        # print(p_event1.get("SUMMARY"))
        # print(p_event2.get("SUMMARY"))
        # p1 = p_event1.get("SUMMARY") == 'Verblijf in Van der Valk Hotel Eindhoven'
        # p2 = p_event2.get("SUMMARY") == '[PSOPV] - Analyseverslag bespreken met begeleider'
        # if p1 and p2:
        #     print("booboo")
        ev1_start = event_tools.get_event_start(p_event1).dt
        ev1_end = event_tools.get_event_end(p_event1).dt
        ev2_start = event_tools.get_event_start(p_event2).dt
        ev2_end = event_tools.get_event_end(p_event2).dt
        all_datetime = isinstance(ev1_start, datetime) and isinstance(ev1_end, datetime) and isinstance(ev2_start, datetime) and isinstance(ev2_end, datetime)
        all_not_datetime = not isinstance(ev1_start, datetime) and not isinstance(ev1_end, datetime) and not isinstance(ev2_start, datetime) and not isinstance(ev2_end, datetime)
        if all_datetime or all_not_datetime:
            pass
        else:
            if isinstance(ev1_start, datetime):
                ev1_start = ev1_start.date()
            if isinstance(ev1_end, datetime):
                ev1_end = ev1_end.date()
            if isinstance(ev2_start, datetime):
                ev2_start = ev2_start.date()
            if isinstance(ev2_end, datetime):
                ev2_end = ev2_end.date()

        # TODO:: Modify algorithm to handle datetime and date
        if self.__check_equal(ev1_start, ev1_end, ev2_start, ev2_end):
            return 0
        elif self.__check_smaller(ev1_start, ev1_end, ev2_start, ev2_end):
            return -1
        else:  # In all the other cases: event1 comes after event2
            return 1

    @staticmethod
    def __check_equal(ev1_start, ev1_end, ev2_start, ev2_end):
        if ev1_start == ev2_start and ev1_end == ev2_end:  # If events have the same start and end date-time
            return True
        return False

    @staticmethod
    def __check_smaller(ev1_start, ev1_end, ev2_start, ev2_end):
        if ev1_start < ev2_start or (
                ev1_start == ev2_start and ev1_end < ev2_end):  # If event1 starts before or at the same time, than event 2
            return True
        return False


class weighted_sum_compare(base_event_compare):
    """
    Weighted sum event-matching
    """
    def __init__(self, p_match_treshold=0.50):
        self.__match_treshold = p_match_treshold
        self.__match_ratio = None


    # ------------------------------------------------------------------------------------------------------------------
    # Getters & setters
    def get_match_ratio(self):
        return self.__match_ratio


    def get_match_treshold(self):
        return self.__match_treshold


    def set_match_treshold(self, p_match_ratio):
        self.__match_ratio = p_match_ratio


    # ------------------------------------------------------------------------------------------------------------------

    def compare(self, p_event1, p_event2):
        """
        Compares p_event1 and p_event2 based on uid, summary, created and description
        with every characteristic having a specific weight resp 0.35, .30, 0.20, 0.15
        :param p_event1:
        :param p_event2:
        :return:        Returns an integer based on the equivalentness of the 2 events
                        -
        """
        self.__match_ratio = 0
        if p_event1.get('uid') == p_event2.get("uid"):
            self.__match_ratio += 0.35
        if p_event1.get("summary") == p_event2.get("summary"):
            self.__match_ratio += 0.3
        if p_event1.get("created") == p_event2.get("created"):
            self.__match_ratio += 0.2
        if p_event1.get("description") == p_event2.get("description"):
            self.__match_ratio += 0.15


        # Translate match_ratio - self.__match_treshold relation to integers
        if self.__match_ratio < self.__match_treshold:
            return -1
        elif self.__match_ratio == self.__match_treshold:
            return 0
        else:
            return 1


from .event_tools import event_tools
from datetime import datetime, date