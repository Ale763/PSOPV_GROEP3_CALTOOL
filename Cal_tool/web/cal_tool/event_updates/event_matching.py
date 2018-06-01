from cal_tool.utilities.fuzzy_string_matching import string_matching_factory, StringMatchingStrategies
from enum import Enum


class EventMatchingStrategies(Enum):
    STRICT_EVENT_MATCHING = 0
    FUZZY_EVENT_MATCHING = 1
    WEIGHTED_SUM_EVENT_MATCHING = 2

    @staticmethod
    def get_all():
        result = {}
        for strategy in EventMatchingStrategies:
            result[strategy.name] = strategy
        return result

    @staticmethod
    def get_strategy(p_strategy_name):
        for strategy in EventMatchingStrategies:
            if p_strategy_name == strategy.name:
                return strategy
        return None

    @staticmethod
    def get_default():
        return EventMatchingStrategies.FUZZY_EVENT_MATCHING


class event_matching_factory:
    @staticmethod
    def get_strategy(p_event_matching_strategy=EventMatchingStrategies.FUZZY_EVENT_MATCHING,
                     p_string_matching_strategy=StringMatchingStrategies.MODIFIED_DAMERAU_LEVENSHTEIN):
        """
        Get strategy for event matching
        :param p_event_matching_strategy:   Strategy-string (has to be one of the possible strategies)
                                            Possible strategies:
                                                1. STRICT_EVENT_MATCHING
                                                2. FUZZY_EVENT_MATCHING + string_matching_strategy
                                                3. WEIGHTED_SUM_EVENT_MATCHING
        :return                             If strategy exists: Strategy instance,else: None
        """
        if p_event_matching_strategy == EventMatchingStrategies.STRICT_EVENT_MATCHING:
            return strict_attribute_event_matching()
        elif p_event_matching_strategy == EventMatchingStrategies.FUZZY_EVENT_MATCHING: # Default
            return fuzzy_attribute_event_matching(p_string_matching_strategy)
        elif p_event_matching_strategy == EventMatchingStrategies.WEIGHTED_SUM_EVENT_MATCHING:
            return weighted_sum_event_matching()
        else:
            return None


class base_event_matching:
    """
    Base of event-matching strategy
    """
    def match(self, p_event1, p_event2):
        """
        Interface method for event-matching-strategies
        :param p_event1:    Event1 to match against event2
        :param p_event2:    Event2 to match against event1
        """
        pass


    def get_all_attribute_keys(self, p_event):
        attribute_list = []
        for key in p_event:
            attribute_list.append(key)
        return attribute_list


class strict_attribute_event_matching(base_event_matching):
    """
    Strict event-matching based on all attributes
    """
    def match(self, p_event1, p_event2):
        # Get attribute keys of events
        event1_keys = self.get_all_attribute_keys(p_event1)
        event2_keys = self.get_all_attribute_keys(p_event2)

        len_event1_keys = len(event1_keys)
        len_event2_keys = len(event2_keys)

        # If amount of attributes is not the same, the events are not the same
        if len_event1_keys == len_event2_keys:
            for key in event1_keys:
                # Check that both items have a value for a shared key
                if p_event2.get(key) is not None:
                    # The value for the given shared key has to be the same
                    a = p_event1.decoded(key)
                    b = p_event2.decoded(key)
                    if p_event1.decoded(key) != p_event2.decoded(key):
                        return False
                    # Remove key from both attribute list
                    #event1_keys.remove(key)
                    event2_keys.remove(key)
                else:
                    # If the value for a given shared key is not the same, the items are not equal
                    return False
            # After checking all the keys of event1_keys, event2_keys has to be empty as well
            if event2_keys != []:
                return False
            return True
        else:
            # If amount of attributes is not the same, the events are clearly not equal
            return False


class fuzzy_attribute_event_matching(base_event_matching):
    """
    Fuzzy event-matching on certain attributes (SUMMARY, DESCRIPTION, DTSTART, DTEND, DURATION)
    all other attributes will be matched in a strict way
    """
    def __init__(self, p_string_matching_strategy=StringMatchingStrategies.MODIFIED_DAMERAU_LEVENSHTEIN):
        self.string_matching_strategy = string_matching_factory.get_strategy(p_string_matching_strategy)


    def match(self, p_event1, p_event2):
        # Get attribute keys of events
        event1_keys = self.get_all_attribute_keys(p_event1)
        event2_keys = self.get_all_attribute_keys(p_event2)

        len_event1_keys = len(event1_keys)
        len_event2_keys = len(event2_keys)

        # fuzzy_matching = string_matching_factory.get_strategy(StringMatchingStrategies.MODIFIED_DAMERAU_LEVENSHTEIN)

        event1_matching_counter = event2_matching_counter = 0
        # If amount of attributes is not the same, the events are not the same
        if len_event1_keys == len_event2_keys:
            for key in event1_keys:
                # Check that both items have a value for a shared key
                if p_event2.get(key) is not None:
                    # Only certain fields are filled by the user and are frequently used
                    if self.__test_attribute_available_for_fuzzy_matching(key):
                        # The value for the given shared key has to be the same
                        event1_attribute = self.__attribute_to_string(key, p_event1)
                        event2_attribute = self.__attribute_to_string(key, p_event2)
                        if self.string_matching_strategy.match(event1_attribute, event2_attribute) is False:
                            return False
                    else:
                        # The value for the given shared key has to be the same
                        if p_event1.decoded(key) != p_event2.decoded(key) and key != "DTSTAMP":
                            return False
                else:
                    # If the value for a given shared key is not the same, the items are not equal
                    return False
            # After checking all the keys of event1_keys, event2_keys has to be empty as well
            return True
        else:
            # If amount of attributes is not the same, the events are clearly not equal
            return False


    def __attribute_to_string(self, key, event):
        if key == "DTSTART" or key == "DTEND" or key == "DTSTART":
            return str(event.decoded(key))
        else:
            return str(event.decoded(key))


    def __test_attribute_available_for_fuzzy_matching(self, attribute):
        if attribute == "SUMMARY":
            return True
        if attribute == "DESCRIPTION":
            return True
        return False


class weighted_sum_event_matching(base_event_matching):
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

    def match(self, p_event1, p_event2):
        """
        Compares p_event1 and p_event2 based on uid, summary, created and description
        with every characteristic having a specific weight resp 0.35, .30, 0.20, 0.15
        BOTH events cant be None for a given key
        :param p_event1:
        :param p_event2:
        :return:        Returns an integer based on the equivalentness of the 2 events
                        (None != None)
                        -
        """
        self.__match_ratio = 0
        if self.__test_events_on_key(p_event1, p_event2, "UID"):
            self.__match_ratio += 0.35
        if self.__test_events_on_key(p_event1, p_event2, "SUMMARY"):
            self.__match_ratio += 0.3
        if self.__test_events_on_key(p_event1, p_event2, "CREATED"):
            self.__match_ratio += 0.2
        if self.__test_events_on_key(p_event1, p_event2, "DESCRIPTION"):
            self.__match_ratio += 0.15

        return self.__match_ratio >= self.__match_treshold


    def __test_events_both_not_none(self, p_event1, p_event2, key):
        if p_event1.get(key) is not None and p_event2.get(key) is not None:
            return True
        return False


    def __test_events_on_key(self, p_event1, p_event2, key):
        if self.__test_events_both_not_none(p_event1, p_event2, key):
            if p_event1.get(key) == p_event2.get(key):
                return True
        return False







#from icalendar import Event
