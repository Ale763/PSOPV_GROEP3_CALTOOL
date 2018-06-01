from enum import Enum

class EventChangeStrategies(Enum):
    DEFAULT_EVENT_CHANGE = 0

    @staticmethod
    def get_all():
        result = {}
        for strategy in EventChangeStrategies:
            result[strategy.name] = strategy
        return result

    @staticmethod
    def get_strategy(p_strategy_name):
        for strategy in EventChangeStrategies:
            if p_strategy_name == strategy.name:
                return strategy
        return None

    @staticmethod
    def get_default():
        return EventChangeStrategies.DEFAULT_EVENT_CHANGE

class event_change_factory:
    @staticmethod
    def get_strategy(p_event_change_strategy=EventChangeStrategies.DEFAULT_EVENT_CHANGE):
        """
        Get strategy for event-change algorithm
        :param p_event_change_strategy: Strategy-string (has to be one of the possible strategies)
                                        Possible strategies:
                                            1. DEFAULT_EVENT_CHANGE
        :return                         If strategy exists: Strategy instance,else: None
        """
        if p_event_change_strategy == EventChangeStrategies.DEFAULT_EVENT_CHANGE:
            return default_event_change_strategy()
        return None


# ----------------------------------------------------------------------------------------------------------------------

class base_event_change_strategy:
    # Override this method
    def check_for_events(self, p_old_source, p_new_source):
        """

        :param p_old_source:    calendar_source of old event
        :param p_new_source:    calendar_source of new event
        :return:                Returns a tuple of lists of deleted, changed and added events
        """
        pass


# ----------------------------------------------------------------------------------------------------------------------

class default_event_change_strategy(base_event_change_strategy):
    def __init__(self):
        self.__attribute_em = event_matching_factory.get_strategy(EventMatchingStrategies.FUZZY_EVENT_MATCHING)
        self.__weighted_sum_em = event_matching_factory.get_strategy(EventMatchingStrategies.WEIGHTED_SUM_EVENT_MATCHING)

    # ------------------------------------------------------------------------------------------------------------------
    # Getters & Setters

    def get_attribute_event_matching(self):
        return self.__attribute_em


    def get_weighted_sum_event_matching(self):
        return self.__weighted_sum_em


    def set_attribute_event_matching(self, attribute_em):
        self.__attribute_em = attribute_em


    def set_weighted_sum_event_matching(self, weighted_sum_em):
        self.__weighted_sum_em = weighted_sum_em


    # ------------------------------------------------------------------------------------------------------------------

    def check_for_events(self, p_old_source, p_new_source):
        """

        :param p_old_source:    calendar_source of old event
        :param p_new_source:    calendar_source of new event
        :return:                Returns a tuple of lists of deleted, changed and added events
        """
        # Remove duplicates
        p_old_source.remove_duplicates()
        p_new_source.remove_duplicates()

        # First search for unmodified events
        temp_old_source, temp_new_source = self.__search_for_unmodified_events(p_old_source, p_new_source)

        # Search for modified events
        temp_old_source, temp_new_source, changed_events = self.__search_for_modified_events(temp_old_source, temp_new_source)

        # Remaining events in old calendar source, are the deleted events
        deleted_events = temp_old_source.get_event_list()

        # Remaining events in new calendar source, are the added events
        added_events = temp_new_source.get_event_list()
        return deleted_events, changed_events, added_events


    def __search_for_unmodified_events(self, p_old_src, p_new_src):
        """
        Searches both calendar_source objects for strictly the same events
        :param p_old_src:   Old version of the calendar_source object
        :param p_new_src:   Newest version of the calendar_source object
        :return:            Returns a tuple of the the old and new version of the calendar_source objects
                            without the events that havent changed
        """

        # Make a deep copy of the old and new version of the calendar_source objects
        temp_old_source = copy.deepcopy(p_old_src)
        temp_new_source = copy.deepcopy(p_new_src)

        # Get the list of events from the old calendar_source
        old_src_events = p_old_src.get_event_list()
        for event in list(old_src_events):
            # Search for event from old_source in new_source with an attribute_matching_strategy
            old_src_event_index = temp_old_source.search(event, self.__attribute_em.match)
            new_src_event_index = temp_new_source.search(event, self.__attribute_em.match)
            # If unmodified event from old version of the source is found in new version of the source
            if new_src_event_index is not None:
                temp_old_source.remove(old_src_event_index)     # Remove even from old source
                temp_new_source.remove(new_src_event_index)     # Remove even from new source

        # Return old and new version without the unmodified events
        return temp_old_source, temp_new_source


    def __search_for_modified_events(self, p_old_src, p_new_src):
        """
        Searches both calendar_source objects for events that have changed
        :param p_old_src:   Old version of the calendar_source object
        :param p_new_src:   Newest version of the calendar_source object
        :return:            Returns a tuple of the the old and new version of the calendar_source objects
                            without the events that have changed and a list with the events that have changed
        """

        # Make a deep copy of the old and new version of the calendar_source objects
        temp_old_source = copy.deepcopy(p_old_src)
        temp_new_source = copy.deepcopy(p_new_src)

        # Get the list of events from the old calendar_source
        old_src_events = p_old_src.get_event_list()
        changed_events = []
        for event in list(old_src_events):
            # Search for event from old_source in new_source with weighted_sum matching
            old_src_event_index = temp_old_source.search(event, self.__weighted_sum_em.match)
            new_src_event_index = temp_new_source.search(event, self.__weighted_sum_em.match)
            # If modified event from old version of the source is found in new version of the source
            if new_src_event_index is not None:
                # modified_event = temp_new_source.get_event(new_src_event_index)
                old_event = temp_old_source.get_event(old_src_event_index)
                new_event = temp_new_source.get_event(new_src_event_index)
                change = changed_event(old_event, new_event)

                changed_events.append(change)                                   # Save modified event to changed_events
                #changed_events.append(change)
                temp_old_source.remove(old_src_event_index)                     # Remove event from old source
                temp_new_source.remove(new_src_event_index)                     # Remove even from new source
        return temp_old_source, temp_new_source, changed_events




import copy
from cal_tool.event_updates.event_matching import event_matching_factory, EventMatchingStrategies
from cal_tool.event_updates.changed_event import changed_event