from .Observable import Observable

#expected a dictionary with "message", "token", "channel" and/or "email"
class Notification(Observable):
    def __init__(self):
        self.__browser=BrowserNotification()
        self.add_observer(SlackNotification())
        self.add_observer(self.__browser)
        self.add_observer(MailNotification())

    #p_event is a dictionary with "message", "token", "channel" and/or "email"
    def send_notification(self, p_dictionary_event):
        """

        :param p_dictionary_event:
        """
        self.set_changed()
        self.notify_observers(p_dictionary_event)

    def get_personal_browser_notifications(self, p_email):
        return self.__browser.get_personal_messages(p_email)

    def get_amount_of_browser_notifications(self, p_email):
        return self.__browser.get_amount_of_personal_messages(p_email)

from .SlackNotification import SlackNotification
from .BrowserNotification import BrowserNotification
from .MailNotification import MailNotification