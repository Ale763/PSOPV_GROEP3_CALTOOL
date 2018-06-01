from enum import Enum
import json
from cal_tool.calendar.calendar_io import default_calendar_io
#from cal_tool.calendar.calendar_source import SourceType
from cal_tool.calendar.calendar import *
from cal_tool.models import *
from Project.settings import ICS_TMP_STORE, ICS_SAVED_STORE






class SourcePlugin:
    #this is a subplugin class that defines gives the posibilitie to predefine informations that can be used while making calendars

    def __init__(self,p_sources = [],p_filter_aliases =[] ):
        self.__m_sources = p_sources #Predefined sources or sources that are downloaded an filled in this list, thi is the list that is going to get displayed
        self.__m_filter_aliases = p_filter_aliases  #list of filter aliases that are displayed and can be querried on

    def setSources(self,p_sources):
        self.__m_sources = p_sources


    def getSources(self):
        return self.__m_sources

    def addSource(self,p_source):
        self.__m_sources.append(p_source)

    def setFilterAliases(self,p_filter_aliases):
        self.__m_filter_aliases = p_filter_aliases

    def addFilterAliases(self, p_filter_alias):
        self.__m_filter_aliases.append(p_filter_alias)

    def setFilterAliasses(self,p_filter_alias):
        self.__m_filter_aliases = p_filter_alias

    def getFilterAliasses(self):
        return self.__m_filter_aliases

    def getAllFilterAliasAtributes(self):
        filter_alias_attributes = []
        for filter_alias in self.__m_filter_aliases:
            filter_alias_attributes.append(filter_alias.getAttributes())
        return filter_alias_attributes

    

    def parse_sources_from_json(self,p_file= None):
        try:
            with p_file as json_file:
                data = json.load(json_file)
                for source in data['sources']:
                    source = Source(p_name=source['name'],p_path=source['path'],p_type=source['type'])
                    self.addSource(p_source= source)

        except Exception as e:
            print(e)


class Source():
    # this is how a source in SourcePlugin is represented
    def __init__(self,p_name=None,p_path=None,p_type=CalendarSources.URL):
        self.__m_name = p_name #name that is going to be displayed at frontend
        self.__m_path = p_path #place that it is stored or url link
        self.__m_type = p_type

    def getName(self):
        return self.__m_name

    def getPath(self):
        return self.__m_path

    def getType(self):
        return self.__m_type



