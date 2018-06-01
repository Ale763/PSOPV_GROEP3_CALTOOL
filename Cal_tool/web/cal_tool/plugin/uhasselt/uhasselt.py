from cal_tool.filter.FilterAttribute import *
from cal_tool.plugin.base.plugin import Plugin
from cal_tool.plugin.uhasselt.filter_attributes import filter_attributes_uhasselt


class UhasseltPlugin(Plugin):
    def __init__(self):
        super(UhasseltPlugin,self).__init__(p_name="UHasselt",p_source_plugin=UhasseltSourcePlugin(), p_view_plugin=UHasseltViewPlugin("cal_tool/plugin_data/uhasselt/logo.jpg"))
        self.setFilterAttributes(filter_attributes_uhasselt)

    def getFolder(self):
        return "uhasselt"

    def getName(self):
        return "UHasselt"

    @staticmethod
    def getRegistrationParser():
        return UHasseltRegistrationInputParser()

from cal_tool.plugin.uhasselt.views import *
from cal_tool.plugin.uhasselt.controller.registration_input_parser import UHasseltRegistrationInputParser


from cal_tool.plugin.base.filter_plugin import *
from cal_tool.filter.FilterAttribute import *
from cal_tool.plugin.uhasselt.source_plugin import UhasseltSourcePlugin