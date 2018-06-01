from enum import Enum

class SortStrategies(Enum):
    DEFAULT_SORT = 0

    @staticmethod
    def get_all():
        result = {}
        for strategy in SortStrategies:
            result[strategy.name] = strategy
        return result

    @staticmethod
    def get_strategy(p_strategy_name):
        for strategy in SortStrategies:
            if p_strategy_name == strategy.name:
                return strategy
        return None

    @staticmethod
    def get_default():
        return SortStrategies.DEFAULT_SORT

class sort_factory:
    @staticmethod
    def get_strategy(p_sort_strategy=SortStrategies.DEFAULT_SORT):
        """
        Get strategy for merging
        :param strategy:    Strategy-string (has to be one of the possible strategies)
        :return             If strategy exists: Strategy instance,else: None
        """
        if p_sort_strategy == SortStrategies.DEFAULT_SORT: # Default sort is quick-sort
            return quick_sort_strategy()
        else:
            return None


class base_sort_strategy:
    """
    Matches 2 strings on 2 levels: whole string matching + individual word matching (split on " ")
    :param p_stra:
    :param p_strb:
    :param p_word_treshold:     Treshold for individual words (percentage)
    :param p_string_treshold:   Treshold for whole string (percentage)
    :return:                    If the match value is strictly higher than both tresholds: Returns True
                                Otherwise: Returns False
    """
    def sort(self, arr, cmp):
        """
        Interface method for sorting-strategies
        :param arr: Array to sort
        :param cmp: Compare function to sort array-items
                    REQUIREMENT: Must return -1, 0, 1 for comparison method
        :return:    Returns sorted arr
        """
        pass


class quick_sort_strategy(base_sort_strategy):
    """
    General-purpose sorting strategy based on the quicksort-algorithm
    """
    def __quick_sort(self,arr, cmp):
        """
        Sorting function based on quicksort with availability for custom cmp-function
        :param arr: Array to sort
        :param cmp: Compare function to sort array-items
                    REQUIREMENT: Must return -1, 0, 1 for comparison method
        :return:    Returns sorted arr
        """
        less = []
        pivotList = []
        more = []
        if len(arr) <= 1:
            return arr
        else:
            # arr_len = len(arr)
            # pivot_nr = random.randrange(0,arr_len)
            # pivot = arr[pivot_nr]
            pivot = arr[0]
            for i in arr:
                if cmp(i, pivot) < 0:
                    less.append(i)
                elif cmp(i, pivot) > 0:
                    more.append(i)
                else:
                    pivotList.append(i)
            less = self.__quick_sort(less, cmp)
            more = self.__quick_sort(more, cmp)
            return less + pivotList + more


    def sort(self, arr, cmp):
        """
        Interface method for sorting-strategies (Quicksort variant)
        :param arr: Array to sort
        :param cmp: Compare function to sort array-items
                    REQUIREMENT: Must return -1, 0, 1 for comparison method
        :return:    Returns sorted arr
        """
        return self.__quick_sort(arr, cmp)

