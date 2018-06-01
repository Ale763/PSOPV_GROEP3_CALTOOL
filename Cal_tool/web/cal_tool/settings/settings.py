import json


class SettingsManager:
    def __init__(self):
        # Internal strategies

        # Event change strategies
        self.__event_change_strategy = None
        self.__event_change_strategies = EventChangeStrategies.get_all()

        # # Event matching strategies
        # self.__event_matching_strategy = None
        # self.__event_matching_strategies = EventMatchingStrategies.get_all()

        # Merge strategies
        self.__merge_strategy = None
        self.__merge_strategies = MergeStrategies.get_all()

        # String matching strategies
        self.__string_matching_strategy = None
        self.__string_matching_strategies = StringMatchingStrategies.get_all()
        self.__fuzzy_string_word_treshold = None
        self.__fuzzy_string_string_treshold = None

        # Sort strategies
        self.__sort_strategy = None
        self.__sort_strategies = SortStrategies.get_all()

        self.__short_term_update_frequency = None
        self.__long_term_update_hour = None
        self.__long_term_update_minutes = None

        self.parse_settings()


    def parse_settings(self):
        with open(SETTINGS_STORE, 'r') as fp:
            data = json.load(fp)
            self.set_settings(data)
        # return data

    def save_settings(self):
        data = self.to_json()
        with open(SETTINGS_STORE, 'w') as fp:
            json.dump(data, fp)

    def to_dict(self):
        dict = {
            "event_change_strategy": self.__event_change_strategy,
            "event_change_strategies": self.__event_change_strategies,
            # "event_matching_strategy": self.__event_matching_strategy,
            # "event_matching_strategies": self.__event_matching_strategies,
            "merge_strategy": self.__merge_strategy,
            "merge_strategies": self.__merge_strategies,
            "string_matching_strategy": self.__string_matching_strategy,
            "string_matching_strategies": self.__string_matching_strategies,
            "fuzzy_string_word_treshold": self.__fuzzy_string_word_treshold,
            "fuzzy_string_string_treshold": self.__fuzzy_string_string_treshold,
            "sort_strategy": self.__sort_strategy,
            "sort_strategies": self.__sort_strategies,
            "short_term_update_frequency": self.__short_term_update_frequency,
            "long_term_update_hour": self.__long_term_update_hour,
            "long_term_update_minutes": self.__long_term_update_minutes
        }
        return dict

    def to_json(self):
        json = {
            "event_change_strategy": self.__event_change_strategy.name,
            # "event_matching_strategy": self.__event_matching_strategy.name,
            "merge_strategy": self.__merge_strategy.name,
            "string_matching_strategy": self.__string_matching_strategy.name,
            "fuzzy_string_word_treshold": self.__fuzzy_string_word_treshold,
            "fuzzy_string_string_treshold": self.__fuzzy_string_string_treshold,
            "sort_strategy": self.__sort_strategy.name,
            "short_term_update_frequency": self.__short_term_update_frequency,
            "long_term_update_hour": self.__long_term_update_hour,
            "long_term_update_minutes": self.__long_term_update_minutes
        }
        return json

    def set_settings(self, p_settings):
        """
        This functions is used from the view to map the strings given by the admin input
        to the Enums from the objects.
        :param p_settings:  Dictionary with all the settings
        :return             Returns True if all given settings were ok,
                            Returns False otherwise
        """
        # Very lazing testing on correct input from admin
        try:
            # Event change strategies
            p_event_change_strategy = EventChangeStrategies.get_strategy(p_settings["event_change_strategy"])

            # Event matching strategies
            # p_event_matching_strategy = EventMatchingStrategies.get_strategy(p_settings["event_matching_strategy"])

            # Merge strategies
            p_merge_strategy = MergeStrategies.get_strategy(p_settings["merge_strategy"])

            # String matching strategies
            p_string_matching_strategy= StringMatchingStrategies.get_strategy(p_settings["string_matching_strategy"])
            p_word_treshold= p_settings["fuzzy_string_word_treshold"]
            p_string_treshold = p_settings["fuzzy_string_string_treshold"]

            # Sort strategies
            p_sort_strategy = SortStrategies.get_strategy(p_settings["sort_strategy"])

            # Update scheduling
            p_short_term_update_frequency = p_settings["short_term_update_frequency"]
            p_long_term_update_hour = p_settings["long_term_update_hour"]
            p_long_term_update_minutes = p_settings["long_term_update_minutes"]

            self.__set_settings(p_event_change_strategy,
                                # p_event_matching_strategy,
                                p_merge_strategy,
                                p_string_matching_strategy,
                                p_word_treshold,
                                p_string_treshold,
                                p_sort_strategy,
                                p_short_term_update_frequency,
                                p_long_term_update_hour,
                                p_long_term_update_minutes)
            return True
        except Exception as e:
            print(e)
            return False


    def __set_settings(self,
                       p_event_change_strategy,
                       # p_event_matching_strategy,
                       p_merge_strategy,
                       p_string_matching_strategy,
                       p_word_treshold,
                       p_string_treshold,
                       p_sort_strategy,
                       p_short_term_update_frequency,
                       p_long_term_update_hour,
                       p_long_term_update_minutes):
        # Event change strategies
        self.__event_change_strategy = p_event_change_strategy

        # Event matching strategies
        # self.__event_matching_strategy = p_event_matching_strategy

        # Merge strategies
        self.__merge_strategy = p_merge_strategy

        # String matching strategies
        self.__string_matching_strategy = p_string_matching_strategy
        self.__fuzzy_string_word_treshold = p_word_treshold
        self.__fuzzy_string_string_treshold = p_string_treshold

        # Sort strategies
        self.__sort_strategy = p_sort_strategy

        # Update scheduling
        do_cron_add = False
        if self.__short_term_update_frequency is None or self.__long_term_update_hour is None or self.__long_term_update_minutes is None:
            do_cron_add = True
        elif self.__short_term_update_frequency != p_short_term_update_frequency or self.__long_term_update_hour != p_long_term_update_hour or self.__long_term_update_minutes != p_long_term_update_minutes:
            do_cron_add = True
        self.__short_term_update_frequency = p_short_term_update_frequency
        self.__long_term_update_hour = p_long_term_update_hour
        self.__long_term_update_minutes = p_long_term_update_minutes

        self.save_settings()
        if do_cron_add:
            cron_add()
        # update_variables()
        # globals()


    # ------------------------------------------------------------------------------------------------------------------
    # Plugins:


    # ------------------------------------------------------------------------------------------------------------------
    # Internal strategies
    # Strategy handling

    # Event change strategy
    def get_active_event_change_strategy(self):
        return self.__event_change_strategy

    def set_active_event_change_strategy(self, p_event_change_strategy):
        self.__event_change_strategy = p_event_change_strategy

    def get_event_change_strategies(self):
        return self.__event_change_strategies

    # Event matching strategy
    # def get_active_event_matching_strategy(self):
    #     return self.__event_change_strategy
    #
    # def set_active_event_matching_strategy(self, p_event_matching_strategy):
    #     self.__event_matching_strategy = p_event_matching_strategy
    #
    # def get_event_matching_strategies(self):
    #     return self.__event_matching_strategies

    # Merge strategy
    def get_active_merge_strategy(self):
        return self.__merge_strategy

    def set_active_merge_strategy(self, p_merge_strategy):
        self.__merge_strategy = p_merge_strategy

    def get_merge_strategies(self):
        return self.__merge_strategies

    # Sorting strategy
    def get_active_sorting_strategy(self):
        return self.__sort_strategy

    def set_active_sorting_strategy(self, p_sorting_strategy):
        self.__sort_strategy = p_sorting_strategy

    def get_sorting_strategies(self):
        return self.__sort_strategies

    # Fuzzy string matching
    def get_word_treshold(self):
        return self.__fuzzy_string_word_treshold

    def get_string_treshold(self):
        return self.__fuzzy_string_string_treshold

    def set_word_treshold(self, p_treshold):
        self.__fuzzy_string_word_treshold = p_treshold
        cron_add()
        self.save_settings()

    def set_string_treshold(self, p_treshold):
        self.__fuzzy_string_string_treshold = p_treshold
        cron_add()
        self.save_settings()

    # ------------------------------------------------------------------------------------------------------------------
    # Plugins:



    # ------------------------------------------------------------------------------------------------------------------
    # Registration

    # def get_registration_settings(self):
    #     return self.__registration_settings

from Project.settings import globals, SETTINGS_STORE, update_variables, cron_add

# Strategies
from cal_tool.event_updates.event_change_strategy import EventChangeStrategies
from cal_tool.event_updates.event_compare import EventCompareStrategies
from cal_tool.event_updates.event_matching import EventMatchingStrategies
from cal_tool.utilities.sorting import SortStrategies
from cal_tool.utilities.fuzzy_string_matching import StringMatchingStrategies
from cal_tool.event_updates.merge_strategy import MergeStrategies