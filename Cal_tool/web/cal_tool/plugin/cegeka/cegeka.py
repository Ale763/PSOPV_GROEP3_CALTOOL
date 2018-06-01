from cal_tool.plugin.base.plugin import *
# from cal_tool.plugin.base.filter_plugin import *
# from cal_tool.filter.FilterAttribute import *
from cal_tool.plugin.cegeka.views import  *
from cal_tool.plugin.cegeka.controller.registration_input_parser import CegekaRegistrationInputParser


class CegekaPlugin(Plugin):
    def __init__(self):
        super(CegekaPlugin,self).__init__(p_name="Cegeka",p_view_plugin=CegekaViewPlugin("cal_tool/plugin_data/cegeka/logo.png"))

    def getFolder(self):
        return "cegeka"

    def getName(self):
        return "Cegeka"

    @staticmethod
    def getRegistrationParser():
        return CegekaRegistrationInputParser()

