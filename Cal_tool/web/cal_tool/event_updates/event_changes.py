from .event_change_strategy import default_event_change_strategy
from cal_tool.calendar.calendar_io import default_calendar_io
from cal_tool.models import CalendarSources
from cal_tool.singletons.notifications_starter import NOTIFICATION_APP
from cal_tool.event_updates.changed_event import changed_event, AttributeStatus
from cal_tool.plugin.uhasselt.filter_attributes import filter_attributes_uhasselt

class event_changes:
    __event_change=default_event_change_strategy()
    __notifications=NOTIFICATION_APP
    __calendar_io = default_calendar_io()

    def send_event_changed_notification(self, p_added, p_changed, p_removed, p_calendar):
        """
        Constructs notification based on changes from lists
        :param p_added:
        :param p_changed:
        :param p_removed:
        :param p_calendar:  calendar-object
        """
        added_events= p_added
        changed_events= p_changed
        deleted_events= p_removed

        notification=self.__get_owner_info(p_calendar.get_owner())
        notification['message'] = self.__make_notifications(p_calendar, deleted_events, changed_events, added_events)

        if notification['message'] is not "":
            self.__notifications.send_notification(notification)


    def __get_sources_from_url(self, p_calendar, p_location):
        calendarID = p_calendar.get_id()
        urls=CalendarSources.objects.filter(cal_id=calendarID).values()

        calendar_sources=[]

        for url in urls:
            calendar_sources.append(self.__calendar_io.parse_file(url[p_location]))

        return calendar_sources

    def __get_owner_info(self, p_owner):
        #TODO: laad info van de eigenaar van de calendar
        info = {}
        #info['token']="xoxp-332875611927-332219201906-340940693570-adde7abc96db270e6773584933196128"
        #info['channel']="CAC1E3MKQ"
        info['token']=p_owner.slacktoken
        info['channel']=p_owner.slackchannel
        if hasattr(p_owner, 'mail') and p_owner.mail is not None:
            info['email']=p_owner.mail

        return info

    def __make_notifications(self, p_calendar, p_deleted_events, p_changed_events, p_added_events):
        if len(p_deleted_events) == 0 and len(p_changed_events) == 0 and len(p_added_events) == 0:
            return ""

        notifications_message="In calendar "+p_calendar.get_calendar_name()+", there are some new changes\n\n"
        if len(p_deleted_events) > 0:
            notifications_message+="Events that are deleted from your calendar:\n"
            notifications_message+=self.__events_to_string(p_deleted_events)
        if  len(p_changed_events) > 0:
            notifications_message += "\nEvents that are changed from your calendar:\n"
            notifications_message += self.__changed_events_to_string(p_changed_events)
        if len(p_added_events) > 0:
            notifications_message+="\nEvents that are added to your calendar:\n"
            notifications_message += self.__events_to_string(p_added_events)

        return notifications_message

    def __changed_events_to_string(self, p_changes):
        event_string = ""
        for changed_event in p_changes:
            event = changed_event.get_old()
            event_string += "\tThe event: "
            if 'SUMMARY' in event and event['SUMMARY'] is not "":
                event_string += event['SUMMARY']
            event_string += '\n'
            if 'DESCRIPTION' in event and event['DESCRIPTION'].to_ical().decode("unicode-escape") != "":
                event_string += '\twith description: '
                event_string += event['DESCRIPTION']
                event_string += '\n'
            event_string += "\thas the next attributes added, changed or deleted: \n"
            attributes = changed_event.get_attributes()
            for attribute, value in attributes.items():
                if attribute not in filter_attributes_uhasselt:
                    continue
                elif value == AttributeStatus.CHANGED:
                    event_string += "\tThe attribute "+filter_attributes_uhasselt[attribute]+" has changed it's value from: "
                    event_string += self.__value_to_string(attribute, changed_event.get_old()[str(attribute)])
                    event_string += " to: "
                    event_string += self.__value_to_string(attribute, changed_event.get_old()[str(attribute)])
                    event_string += '\n'
                elif value == AttributeStatus.ADDED:
                    event_string += "\t" + str(filter_attributes_uhasselt[str(attribute)])
                    event_string += " has been added with value: "
                    event_string += self.__value_to_string(attribute, changed_event.get_old()[str(attribute)])
                    event_string += '\n'
                else:
                    event_string += "\t" + str(filter_attributes_uhasselt[str(attribute)])
                    event_string += " has deleted"
                    event_string += '\n'

        return event_string

    def __value_to_string(self, p_attribute, p_value):
        if str(p_attribute) == "DTSTART" or str(p_attribute) == "DTEND":
            return p_value.dt.strftime("%Y-%m-%d %H:%M")
        else:
            return str(p_value.to_ical().decode("unicode-escape")).replace("\\\\", "\\").replace("\,", ", ")


    @staticmethod
    def __interpret_attribute_status(p_attribute):
        if p_attribute == AttributeStatus.ADDED:
            return "toegevoegd"
        elif p_attribute == AttributeStatus.CHANGED:
            return "veranderd"
        else:
            return "verwijderd"

    def __events_to_string(self, p_event_list):
        event_string=""
        for event in p_event_list:
            event_string+="\tThe event: "
            if 'SUMMARY' in event and event['SUMMARY'] is not "":
                event_string+=event['SUMMARY']
            event_string+='\n'
            if 'DESCRIPTION' in event and event['DESCRIPTION'] is not "":
                event_string+='\twith description: '
                event_string += event['DESCRIPTION']
                event_string += '\n'
            if 'DTSTART' in event and 'DTEND' in event:
                event_string += '\tfrom '
                event_string += event["DTSTART"].dt.strftime("%H.%M %d.%m.%y")
                event_string += ' to '
                event_string += event["DTEND"].dt.strftime("%H.%M %d.%m.%y")
            event_string += '\n\n'

        return event_string