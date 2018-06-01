# from cal_tool.event_updates.event_compare import event_compare_factory
# from cal_tool.utilities.sorting import sort_factory
from cal_tool.event_updates.event_matching import EventMatchingStrategies
from enum import Enum


class MergeStrategies(Enum):
    DEFAULT_MERGE = 0

    @staticmethod
    def get_all():
        result = {}
        for strategy in MergeStrategies:
            result[strategy.name] = strategy
        return result

    @staticmethod
    def get_strategy(p_strategy_name):
        for strategy in MergeStrategies:
            if p_strategy_name == strategy.name:
                return strategy
        return None

    @staticmethod
    def get_default():
        return MergeStrategies.DEFAULT_MERGE


class merge_factory:
    @staticmethod
    def get_strategy(p_event_matching=EventMatchingStrategies.FUZZY_EVENT_MATCHING,
                     p_merge_strategy=MergeStrategies.DEFAULT_MERGE):
        """
        Get strategy for merging
        :param p_event_matching:
        :param p_merge_strategy:            Strategy-string (has to be one of the possible strategies)
                                            Possible strategies:
                                                1. DEFAULT_MERGE
        :return                             If strategy exists: Strategy instance,else: None
        """
        # event_matching_factory = event_compare_factory.get_strategy(p_event_compare_strategy)
        if p_merge_strategy == MergeStrategies.DEFAULT_MERGE:
            return default_merge_strategy(p_event_matching)
        else:
            return None


class base_merge_strategy:
    # Override this method
    def merge(self, p_calendars):
        """
        Merges the calendars to be one calendar_source object
        :param      p_calendars: List of calendars to merge
        :return:    Returns the merged calendars as a calendar_source object
        """
        pass


class default_merge_strategy(base_merge_strategy):
    def __init__(self, p_event_match=EventMatchingStrategies.STRICT_EVENT_MATCHING):
        # if p_event_match is None:
        #     p_event_cmp = event_matching_factory.get_strategy()
        self.__event_cmp = event_matching_factory.get_strategy(p_event_match)
        #self.__sort_strategy = cal_tool.utilities.sorting.sort_factory.get_strategy()


    def merge(self, p_calendars):
        """
        Merges the calendars to be one calendar_source object
        :param      p_calendars: List of calendars to merge
        :return:    Returns the merged calendars as a calendar_source object
        """
        merged_cal = calendar_source()
        # For every calendar from p_calendars
        for calendar in p_calendars:
            calendar.apply_filters()                    # Apply filter to limit amount of calculations later
            merged_cal.add_multiple_events(calendar)    # Add events
        merged_cal.sort()


        # TODO:: Make sure that UID of Event is unique
        for i in range(merged_cal.get_size()-1):
            current = merged_cal.get_event(i)
            next = merged_cal.get_event(i+1)
            if next is None or current is None:
                continue
            if self.__event_cmp.match(current, next):
                merged_cal.remove(i+1)
        merged_cal.construct_default_calendar_attributes()
        return merged_cal


from cal_tool.event_updates.event_matching import event_matching_factory, EventMatchingStrategies
from cal_tool.event_updates.event_compare import event_compare_factory, EventCompareStrategies
from cal_tool.calendar.calendar_source import calendar_source