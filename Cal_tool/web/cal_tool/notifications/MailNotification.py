from .Observer import Observer

class MailNotification(Observer):
    def __init__(self):
        try:
            self.__server = smtplib.SMTP('smtp.gmail.com', 587)
        except Exception:
            print("Could not connect to mailserver")
            return
        self.__server.ehlo()
        self.__server.starttls()
        self.__server.ehlo()

        # Next, log in to the server
        try:
            self.__server.login("noreplycaltool@gmail.com", "alessioaytugjef")
        except Exception:
            print("Could not connect to mailserver")

    def update(self, observable, arg):
        if 'email' in arg and 'message' in arg:
            self.__send_mail(arg['email'], arg['message'])

    def __send_mail(self, p_mail_address, p_messege):
        # Send the mail
        mail = 'Subject: {}\n\n{}'.format("There are some changes in your calendars...", p_messege)
        try:
            self.__server.sendmail("noreplycaltool@gmail.com", p_mail_address, mail)
        except Exception:
            print("Could not connect to mailserver")
        self.__server.sendmail("noreplycaltool@gmail.com", p_mail_address, mail)

import smtplib