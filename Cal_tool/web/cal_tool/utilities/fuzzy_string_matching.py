from enum import Enum


class StringMatchingStrategies(Enum):
    STRICT = 0
    MODIFIED_DAMERAU_LEVENSHTEIN = 1

    @staticmethod
    def get_all():
        result = {}
        for strategy in StringMatchingStrategies:
            result[strategy.name] = strategy
        return result

    @staticmethod
    def get_strategy(p_strategy_name):
        for strategy in StringMatchingStrategies:
            if p_strategy_name == strategy.name:
                return strategy
        return None

    @staticmethod
    def get_default():
        return StringMatchingStrategies.MODIFIED_DAMERAU_LEVENSHTEIN

class string_matching_factory:
    @staticmethod
    def get_strategy(p_strategy=StringMatchingStrategies.STRICT):
        """
        Get strategy for merging
        :param strategy:    Strategy-string (has to be one of the possible strategies)
        :return             If strategy exists: Strategy instance,else: None
        """
        if p_strategy == StringMatchingStrategies.STRICT:
            return strict_string_matching_strategy()
        elif p_strategy == StringMatchingStrategies.MODIFIED_DAMERAU_LEVENSHTEIN:    # Default
            return modified_damerau_levenshtein_strategy()
        else:
            return None


class base_matching_strategy:
    """
    Matches 2 strings on 2 levels: whole string matching + individual word matching (split on " ")
    :param p_stra:
    :param p_strb:
    :param p_word_treshold:     Treshold for individual words (percentage)
    :param p_string_treshold:   Treshold for whole string (percentage)
    :return:                    If the match value is strictly higher than both tresholds: Returns True
                                Otherwise: Returns False
    """
    def match(self, p_stra, p_strb):
        pass


class strict_string_matching_strategy(base_matching_strategy):
    """
    Default matching strategy: Classic strict matching between 2 strings
    """
    def match(self, p_stra, p_strb):
        """
        Classic strict matching between 2 strings
        :param p_stra:
        :param p_strb:
        :return:        Returns True if strings are equal, Returns False otherwise
        """
        if p_stra == p_strb:
            return True
        return False



class modified_damerau_levenshtein_strategy(base_matching_strategy):
    """
    Matching strategy based on Damerau-Levenshtein with whole string + individual word checking
    """
    def __init__(self, p_word_treshold=None, p_string_treshold=None):
        if p_word_treshold is None:
            p_word_treshold = MODIFIED_DAMERAU_LEVENSHTEIN_WORD_TRESHOLD
        if p_string_treshold is None:
            p_string_treshold = MODIFIED_DAMERAU_LEVENSHTEIN_STRING_TRESHOLD
        self.word_treshold = p_word_treshold
        self.string_treshold = p_string_treshold


    @staticmethod
    def __damerau_levenshtein(p_stra, p_strb):
        """
        Sligthly modified fuzzy-string-matching algorithm of Damerau-Levenshtein
        This algorithm identifies deletions, insertions, substitutions and transpositions
        :return:    Proportional match between the 2 strings
        """
        d = {}
        lenstr1 = len(p_stra)
        lenstr2 = len(p_strb)

        if lenstr1 == 0 and lenstr2 == 0:
            return 1
        elif (lenstr1 == 0 and lenstr2 != 0) or (lenstr1 == 0 and lenstr2 != 0):
            return 0

        # Initialize first column
        for i in range(-1, lenstr1 + 1):
            d[(i, -1)] = i + 1

        # Initialize first row
        for j in range(-1, lenstr2 + 1):
            d[(-1, j)] = j + 1

        # Calculate matrix of transformation costs
        for i in range(lenstr1):
            for j in range(lenstr2):
                if p_stra[i] == p_strb[j]:
                    cost = 0
                else:
                    cost = 1
                d[(i, j)] = min(
                    d[(i - 1, j)] + 1,                                      # deletion
                    d[(i, j - 1)] + 1,                                      # insertion
                    d[(i - 1, j - 1)] + cost,                               # substitution
                )
                if i and j and p_stra[i] == p_strb[j - 1] and p_stra[i - 1] == p_strb[j]:
                    d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)      # transposition

        # Calculate proportion of matching between the 2 strings
        MAX = max([lenstr1, lenstr2])
        return ((MAX - d[lenstr1 - 1, lenstr2 - 1]) / MAX) * 100


    def __match_word(self, p_stra, p_strb):
        """
        Matches the 2 words and verifies if the match is strictly higher than the given treshold
        :param p_stra:
        :param p_strb:
        :param p_treshold:
        :return:            If the match is strictly higher thant the treshold: Returns the proportional word match
                            Otherwise: Returns 0
        """
        word_match = modified_damerau_levenshtein_strategy.__damerau_levenshtein(p_stra, p_strb)
        if word_match <= self.word_treshold:
            return 0
        return word_match


    def __match_each_word(self, p_phrase1, p_phrase2):
        """
        Matches the individual words (split on " ") against the given treshold

        :param p_phrase1:   String 1 to match against string 2
        :param p_phrase2:   String 2 to match against string 1
        :param treshold:    Words have to match strictly above this treshold
        :return:            Returns the sum of the proportional match if all the words match higher
                            than the given treshold
                            Otherwise returns 0
        """

        # Split strings in word lists
        phrase1_list = p_phrase1.split(" ")
        phrase2_list = p_phrase2.split(" ")

        # Calculate length of each word list
        len_phrase1_list = len(phrase1_list)
        len_phrase2_list = len(phrase2_list)

        # Calculate min and max length for fault tolerance (if the lengths of word lists are not equal)
        min_len = min(len_phrase1_list, len_phrase2_list)
        # max_len = max(len_phrase1_list, len_phrase2_list)

        # Initialize match_weight at 0, initially
        match_weight = 0

        # Test if both strings have the same amount of words
        matching = modified_damerau_levenshtein_strategy()
        for i in range(min_len):
            word_match = modified_damerau_levenshtein_strategy.__damerau_levenshtein(phrase1_list[i], phrase2_list[i])
            if word_match <= self.word_treshold:
                return 0
            match_weight += word_match
        return match_weight / min_len


    def match(self, p_stra, p_strb):
        """
        Matches 2 strings on 2 levels: whole string matching + individual word matching (split on " ")
        :param p_stra:
        :param p_strb:
        :param p_word_treshold:     Treshold for individual words (percentage)
        :param p_string_treshold:   Treshold for whole string (percentage)
        :return:                    If the match value is strictly higher than both tresholds: Returns True
                                    Otherwise: Returns False
        """

        # Test if both strings are strictly the same
        strict_string_matching = strict_string_matching_strategy()
        if strict_string_matching.match(p_stra, p_strb):
            return True

        # Initialize succes on true
        match_success = True

        # Match individual words
        words_match = modified_damerau_levenshtein_strategy.__match_each_word(self, p_stra, p_strb)
        if words_match <= self.word_treshold:  # Match has to be strictly higher than the given treshold
            return False

        # Match whole string
        phrase_match = modified_damerau_levenshtein_strategy.__damerau_levenshtein(p_stra, p_strb)
        if phrase_match <= self.string_treshold:
            match_success = False

        return match_success

from Project.settings import FUZZY_STRING_MATCHING_STRING_TRESHOLD, FUZZY_STRING_MATCHING_WORD_TRESHOLD
from cal_tool.singletons.settings_manager_starter import settings_manager
MODIFIED_DAMERAU_LEVENSHTEIN_WORD_TRESHOLD = settings_manager.get_word_treshold()
MODIFIED_DAMERAU_LEVENSHTEIN_STRING_TRESHOLD = settings_manager.get_string_treshold()