class ShareCalendar:
    def __init__(self):
        try:
            self.__server = smtplib.SMTP('smtp.gmail.com', 587)
            self.__server.ehlo()
            self.__server.starttls()
            self.__server.ehlo()

            # Next, log in to the server
            self.__server.login("noreplycaltool@gmail.com", "alessioaytugjef")

        except SMTPAuthenticationError:
            print("Could not connect to mailserver")

    def share_calendar(self, p_cal_id, p_email=None, p_password=""):
        # share calendar by email
        if p_email is not None:
            new_url = self.__save_shared_calendar(p_cal_id, p_email, p_password)
            self.__share_url_by_mail(p_email, new_url)
            return None

        # share calendar by public url
        else:
            calendar = Calendars.objects.filter(cal_id=p_cal_id)[0]
            shared_cal_url = SharedCalendars.objects.filter(cal_id=calendar, mail__isnull=True)

            # if public url doesn't exist
            if shared_cal_url.count() == 0:
                return self.__save_shared_calendar(p_cal_id, p_email, p_password)
            else:
                return shared_cal_url.values()[0]["url"]+".ics"

    def share_emails(self, p_cal_id):
        email_list = []

        calendar = Calendars.objects.filter(cal_id=p_cal_id)[0]
        shared_cal_url = SharedCalendars.objects.filter(cal_id=calendar, mail__isnull=False)

        for i in range(0, shared_cal_url.count()):
            email_list.append(shared_cal_url.values()[i]["mail"])

        return email_list


    def __save_shared_calendar(self, p_cal_id, p_email, p_password):
        cal = calendar()
        cal.load_from_database(int(p_cal_id))
        new_url = cal.export()

        # Save shared calendar to saved storage
        ICS_TMP_STORE_len = len(ICS_TMP_STORE)
        path = new_url[ICS_TMP_STORE_len:]
        saved_url = ICS_SAVED_STORE + path

        cal = open(new_url, "rb").read()
        new_cal = open(saved_url+".ics", "wb")
        new_cal.write(cal)
        new_cal.close()

        calendar_db = Calendars.objects.filter(cal_id=p_cal_id)[0]
        if SharedCalendars.objects.filter(cal_id=calendar_db, mail=p_email).exists():
            return SharedCalendars.objects.filter(cal_id=calendar_db, mail=p_email)[0].url + ".ics"
        else:
            db_shared_cal = SharedCalendars(cal_id=calendar_db, mail=p_email, url=saved_url, password=p_password)
            db_shared_cal.save()
            return saved_url+".ics"

    def delete_shared_email(self, p_cal_id, p_email):
        calendar = Calendars.objects.filter(cal_id=p_cal_id)[0]
        entry_to_delete = SharedCalendars.objects.filter(cal_id=calendar, mail=p_email)[0]
        entry_to_delete.delete()


    def __share_url_by_mail(self, p_adress, p_url):
        # Send the mail
        message = "There is a calendar shared with you, here is the link:\n\n" + p_url
        mail = 'Subject: {}\n\n{}'.format("There is a calendar shared with you...", message)
        self.__server.sendmail("noreplycaltool@gmail.com", p_adress, mail)


import smtplib
from cal_tool.models import SharedCalendars, Calendars
from cal_tool.calendar.calendar import calendar
from Project.settings import ICS_SAVED_STORE, ICS_TMP_STORE
from smtplib import SMTPAuthenticationError