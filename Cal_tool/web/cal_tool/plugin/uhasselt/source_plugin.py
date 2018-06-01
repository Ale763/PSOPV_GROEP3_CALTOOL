from cal_tool.plugin.base.plugin import SourcePlugin


class UhasseltSourcePlugin(SourcePlugin):
    def __init__(self):
        super(UhasseltSourcePlugin,self).__init__()
        self.makeFilterAliasses()
        self.parse_sources()



    def makeFilterAliasses(self):
        self.addFilterAliases(p_filter_alias=FilterAlias(p_attribute=AttributeType.DESCRIPTION,p_alias="Lokaal"))
        self.addFilterAliases(p_filter_alias=FilterAlias(p_attribute=AttributeType.DESCRIPTION,p_alias="Professor"))


    def parse_sources(self):
        """
        Get all UHasselt ics url sources from file
        :param
        :return:
        """
        file = open("/data/web/cal_tool/plugin/uhasselt/sources/sources.json")
        self.parse_sources_from_json(p_file=file)



if __name__ == '__main__':
    new = UhasseltSourcePlugin()

from cal_tool.plugin.base.filter_plugin import *
from cal_tool.filter.FilterAttribute import *