from icalendar import Calendar, Event
from cal_tool.plugin.base.filter_attributes import filter_attributes
class Plugin:
    """
    This class has all the subplugins and will use the default subplugin if there isn a subplugin inheritted for a specific pluign
    This class controls all the subplugins and has the grouped up together
    """

    def __init__(self, p_name="Standaard",
                 p_source_plugin=None,
                 p_logo=None,
                 p_view_plugin=None):
        """
        :param p_name: name of the plugin
        :param p_source_plugin: sourceplugin if available, else default will be used
        :param p_logo: path to the logo
        :param p_view_plugin: view plugin that makes the redirections for if they wish to redirect in a different way then the default would
        :param p_filter_attributes: are the filter attributes you want to filter on
        """
        if p_source_plugin is None:
            p_source_plugin = SourcePlugin()

        if p_view_plugin is None:
            p_view_plugin = ViewPlugin()


        self.__m_name = p_name
        self.__m_source_plugin = p_source_plugin
        self.__m_logo = p_logo
        self.__m_view_plugin = p_view_plugin
        self.__m_filter_attributes = filter_attributes

    def setSourcePlugin(self,p_source_plugin):
        self.__m_source_plugin = p_source_plugin

    def getSourcePlugin(self):
        return self.__m_source_plugin

    def getViewPlugin(self):
        return self.__m_view_plugin

    def getLogo(self):
        return self.__m_logo

    def getName(self):
        return self.__m_name

    @staticmethod
    def getRegistrationParser():
        return BaseRegistrationInputParser()
    def getFilterAttributes(self):
        return self.__m_filter_attributes

    def setFilterAttributes(self, p_filter_attributes):
        self.__m_filter_attributes = p_filter_attributes

from cal_tool.plugin.base.views import ViewPlugin
from cal_tool.plugin.base.source_plugin import SourcePlugin
from cal_tool.plugin.base.controller.registration_input_parser import BaseRegistrationInputParser


