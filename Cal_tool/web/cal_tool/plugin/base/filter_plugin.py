class FilterAlias:
    def __init__(self,p_attribute=None, p_alias=None,p_filter_options= [ ]):
        self.__m_attribute = p_attribute #the filter attribute that is going to be used in the filtering algorithm
        self.__m_alias = p_alias #the name that is going to be displayed on the frontend
        self.__m_filter_options = p_filter_options #possible to give a list of options to choose from, not necessary

    def getAlias(self):
        return self.__m_alias

    def addFilterOption(self,p_filter_option):
        self.__m_filter_options.extend(p_filter_option)


class FilterOption:
    def __init__(self, p_display_field=None, p_query_field=None):
        """
        :param p_display_field: displayed name for in the frontend
        :param p_query_field: queried string that is going to be used to queried
        """
        self.__m_display_field = p_display_field
        self.__m_query_field = p_query_field

    def giveQueryField(self):
        return self.__m_query_field

    def giverDisplayField(self):
        return self.__m_display_field