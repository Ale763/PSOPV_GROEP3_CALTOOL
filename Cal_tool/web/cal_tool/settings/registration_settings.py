class RegistrationSettings():
    def __init__(self, p_plugins=None):
        if p_plugins is None:
            # ALL PLUGINS GO HERE
            p_plugins = INSTALLED_PLUGINS
        self.__plugins = p_plugins

    def get_plugins(self):
        return self.__plugins

    def set_plugins(self, p_plugins):
        self.__plugins = p_plugins

    @staticmethod
    def is_number(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def set_user_plugin(request, user):
        if user.domain == Users.BASE:
            request.session['plugin'] = Plugin()
        elif user.domain == Users.UHASSELT:
            request.session['plugin'] = UhasseltPlugin()
        elif user.domain == Users.CEGEKA:
            request.session['plugin'] = CegekaPlugin()

    @staticmethod
    def get_installed_plugins():
        return INSTALLED_PLUGINS


from cal_tool.models import Users
from cal_tool.plugin.base.plugin import Plugin
from cal_tool.plugin.uhasselt.uhasselt import UhasseltPlugin
from cal_tool.plugin.cegeka.cegeka import CegekaPlugin

INSTALLED_PLUGINS = [
    Plugin(),
    UhasseltPlugin(),
    CegekaPlugin()
]