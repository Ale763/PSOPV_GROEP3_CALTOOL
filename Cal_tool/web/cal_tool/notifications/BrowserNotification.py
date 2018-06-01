from .Observer import Observer

class BrowserNotification(Observer):
    __messages = []
    __SECONDS = 3600 #3600 seconds in 1 hour, messages older then an hour will be removed

    def update(self, observable, arg):
        if 'message' in arg and 'email' in arg:
            self.__add_message_to_queue(arg)

    def __add_message_to_queue(self, p_message):
        message = {
            "message":p_message['message'],
            "time" : time.time(),
            "email" : p_message['email']
        }

        self.__delete_old_messages()
        self.__messages.append(message)


    def __delete_old_messages(self):
        for message in self.__messages:
            if not self.__time_in_range(message['time'], time.time(), self.__SECONDS):
                self.__messages.remove(message)


    def __time_in_range(self, start, end, x):
        """Return true if x is in the range [start, end]"""
        if start <= end:
            return start+x > end
        else:
            return False

    def get_personal_messages(self, p_email):
        self.__delete_old_messages()

        personal_messages = []
        for m in self.__messages:
            if m['email'] == p_email:
                personal_messages.append(m)
                self.__messages.remove(m)

        return personal_messages

    def get_amount_of_personal_messages(self, p_email):
        amount_of_messages = 0
        personal_messages = self.get_personal_messages(p_email)
        for _ in personal_messages:
            amount_of_messages+=1

        return amount_of_messages

import time