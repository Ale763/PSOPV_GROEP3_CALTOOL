from cal_tool.models import Users, Calendars, CalendarSources

class UpdateManager:
    def __init__(self):
        self.__last_completed_update = datetime.now()
        self.__force_refilter = True
        pass

    # ------------------------------------------------------------------------------------------------------------------
    # Setters & Getters

    def set_force_refilter(self, p_force_refilter):
        self.__force_refilter = p_force_refilter

    def get_force_refilter(self):
        return self.__force_refilter

    def set_last_completed_update(self, p_datetime):
        self.__force_refilter = p_datetime

    def get_last_completed_update(self):
        return self.set_last_completed_update

    # ------------------------------------------------------------------------------------------------------------------

    def update_calendars(self, p_short_term=False):
        """
        Starts checking all calendars for changes and notifies users if there are changes
        """
        # Update calendars per user
        for user in Users.objects.all():
            # Retrieve all calenders from given user and check for updates
            calendars = Calendars.get_calenders_from_user(user.unique_id)
            for calendar in calendars:
                self.__check_calendar_updates(calendar, p_short_term)

        # When finished checking all calenders from all users,
        # update the self.__last_completed_update to finish-time
        self.__last_completed_update = datetime.now()

    # ------------------------------------------------------------------------------------------------------------------
    # Helper functions

    def __check_calendar_updates(self, p_cal, p_short_term):
        """
        Iterates over all the sources of a calendar
        :param p_cal:
        """
        cal = calendar()
        cal.load_from_database(p_cal.cal_id, self.__last_completed_update)
        result = cal.check_for_updates(p_short_term=p_short_term)

        if result is not None:
            # Separate results
            deleted_events, changed_events, added_events = result[0], result[1], result[2]

            # Notify user
            # TODO:: TESTEN
            event_changes_notifcation = event_changes()
            event_changes_notifcation.send_event_changed_notification(added_events, changed_events, deleted_events, cal)

    def __check_calendar_source_updates(self, p_cal_src):
        """

        :param p_cal_src:
        """
        db_cal_sources = CalendarSources.objects.filter(cal_id=p_cal_src.cal_source_id)
        cal_src = CalendarSources()

    def __get_filtered_source(self, p_cal_src_id):
        if Filters.check_filters_changed(self.__last_completed_update):
            filtered_source_path = CalendarSources.objects.filter(cal_source_id=p_cal_src_id)


from datetime import datetime
from cal_tool.models import Filters
from cal_tool.calendar.calendar import calendar, calendar_source
from cal_tool.event_updates.event_changes import event_changes
from cal_tool.singletons.notifications_starter import NOTIFICATION_APP