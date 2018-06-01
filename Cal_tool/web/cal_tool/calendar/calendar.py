from datetime import datetime
import os, shutil, copy


class calendar:
    def __init__(self, id=None, merge_strategy=None, filter_strategy=None):
        # Settings
        self.__merge_strategy = merge_factory.get_strategy(MATCHING_STRATEGY, MERGE_STRATEGY)
        self.__filter_strategy = filter_strategy
        self.__event_change_strategy = event_change_factory.get_strategy(EVENT_CHANGE_STRATEGY)
        self.__io = io_factory.get_strategy(IO_STRATEGY)

        # Characteristics
        self.__id = id
        self.__sources = []
        self.__calendar_name = None
        self.__calendar_color = None
        #
        # # Globals
        # self.__io_strategy =

    def visit(self, settings_manager):
        pass
        # self.__io_strategy = io_factory.DEFAULT
        # EVENT_CHANGE_STRATEGY = settings_manager.get_active_event_strategy()
        # DATETIME_EVENT_COMPARE_STRATEGY = EventCompareStrategies.DATETIME_EVENT_COMPARE
        # MERGE_STRATEGY = MergeStrategies.DEFAULT_MERGE
        # SHORT_TERM_WINDOW = 14


    # ------------------------------------------------------------------------------------------------------------------
    # Getters & setters

    def get_id(self):
        return self.__id

    def get_sources(self):
        return self.__sources

    def get_calendar_color(self):
        return self.__calendar_color

    def set_calendar_color(self, p_calendar_color):
        self.__calendar_color = p_calendar_color

    def get_calendar_name(self):
        return self.__calendar_name

    def set_calendar_name(self, p_calendar_name):
        self.__calendar_name = p_calendar_name

    def __set_default_merge_strategy(self):
        if self.__merge_strategy is None:
            self.__merge_strategy = MERGE_STRATEGY

    def get_size(self):
        size = 0
        for source in self.__sources:
            size += source.get_size()
        return size

    def add_source(self, p_source):
        self.__sources.append(p_source)

    def add_sources(self, p_sources):
        self.__sources.append(p_sources)


    def get_owner(self):
        """
        Returns Users-object that is the owner of the calendar
        :return: Returns Users-object that is the owner of the calendar
        """
        calendar_object = Calendars.objects.filter(cal_id=self.__id)
        if calendar_object.count() == 0:
            raise Exception("Calendar not found in database.")
        user_id = calendar_object[0].unique_id.unique_id
        return Users.objects.get(unique_id=user_id)

    # ------------------------------------------------------------------------------------------------------------------
    # Database

    def load_from_database(self, p_cal_id, p_last_checked=datetime.now(), p_force_refilter=False):
        """
        Loads calendar from database with its sources.
        The sources will contain the filtered events if the filters where changed since last checked
        :param p_cal_id:
        :param p_last_checked:
        """
        db_cal = Calendars.objects.filter(cal_id=p_cal_id).values()[0]
        self.__id = db_cal["cal_id"]
        self.__calendar_color = db_cal["cal_color"]
        self.__calendar_name = db_cal["cal_alias"]

        sources = CalendarSources.objects.filter(cal_id=p_cal_id)
        self.__sources = []
        for source in sources.values():
            src = calendar_source()
            filters_changed =  Filters.check_filters_changed(source["cal_source_id"], p_last_checked)
            refilter = filters_changed or p_force_refilter
            src.load_from_database(source["cal_source_id"],refilter)
            self.__sources.append(src)

    def save_to_database(self, user=None):
        """
        Saving NEW object to database, ONLY FOR NEW OBJECTS
        For existing objects use .save()
        """
        if user is None:
            user = self.get_owner().username
        self.__id = Calendars.generate_new_id()
        cal_id = self.__id
        user = Users.objects.get(username=user)
        db_cal = Calendars(cal_id=cal_id,
                           unique_id=user,
                           cal_alias=self.__calendar_name,
                           cal_color=self.__calendar_color)
        db_cal.save()
        cal = Calendars.objects.get(cal_id=cal_id)
        for source in self.__sources:
            source.save_to_database(cal)

    # ------------------------------------------------------------------------------------------------------------------
    # Remove events from calendar based on filter

    def apply_filter(self):
        # filter_strategy.filter()
        pass

    def merge(self):
        merged_calendar = self.__merge_strategy.merge(self.__sources)
        return merged_calendar

    def export(self):
        location = CalendarSources.generate_new_file_name(ICS_TMP_STORE)
        merged_calendar = self.merge()
        self.__io.write_to_file(merged_calendar, location)
        return location

    # ------------------------------------------------------------------------------------------------------------------
    # Event updates handling

    def check_for_updates(self, p_short_term=False, p_skip_filetype=True):
        """
        Checks calendar for updates by comparing old and new version of all its sources
        and notifies the users if changes are detected
        :param p_short_term:    Must be set to True to enable short-term checking
        :param p_skip_filetype: Must be set to True when skipping FILE-types when checking
        :return                 Returns a list containing lists representing in order:
                                    0:  List containing deleted Event-objects
                                    1:  List containing changed changed_event-objects
                                    2:  List containing added Event-objects
        """
        for cal_src in self.__sources:
            # Skip CalendarSources.FILE calendar_sources when p_skip_filetype equals True
            if not p_skip_filetype and cal_src.get_source_type() == CalendarSources.FILE:
                continue

            # Old version
            old = cal_src

            # New version
            new = self.__handle_new_version(old)

            #Apply filters:
            old, new = self.__apply_update_filter(old, new, p_short_term)


            # Compare old and new version with event_change_strategy
            result = list(self.__event_change_strategy.check_for_events(old, new))

            # If changes detected
            if self.__changes_detected(result):


                # Update database and files
                self.__update_locations(old, new)


                return result
            return None

    def __handle_new_version(self, old):
        """
        Creates and fills new version of calendar source with the data of the up-to date calendar
        :param old:
        :return: Returns tuple of new calendar_source object and the location
        """
        # Construct new version of source
        new = copy.deepcopy(old)
        new_unfiltered_location = self.__get_new_version(old)               # Unfiltered location of new version (url or file)
        if new_unfiltered_location is None:
            raise Exception("No location found.")
        new_unfiltered = self.__io.parse_file(new_unfiltered_location)      # Parse file or url
        new.set_cal_attributes(new_unfiltered.get_cal_attribute_list())     # Set attributes of freshly parsed calendar
        new.set_event_list(new_unfiltered.get_event_list())                 # Set event list of freshly parsed calendar

        # Generate location on disk and write to temporary folder
        new_unfiltered_location_on_disk = CalendarSources.generate_new_file_name(ICS_TMP_STORE)
        new.set_source_location(new_unfiltered_location_on_disk)
        if new_unfiltered_location_on_disk is None:
            raise Exception("No location found.")
        self.__io.write_to_file(new_unfiltered, new_unfiltered_location_on_disk)
        return new

    def __update_locations(self, old, new):
        """
        Updates and moves the files from temporary location to saved location
        :param old:
        :param new:
        """
        # Update old unfiltered location
        self.__delete_file(old.get_source_location())
        shutil.move(new.get_source_location(), old.get_source_location())

        # Update old filtered location
        self.__delete_file(old.get_filtered_source_location())
        shutil.move(new.get_filtered_source_location(), old.get_filtered_source_location())
        #self.__io.write_to_file(new, new.get_filtered_source_location())

    def __apply_update_filter(self, p_old_src, p_new_src, p_short_term):
        """
        Applies all filters to calendar with short-term filtern when enabled with p_short_term=true
        :param p_old_src:       Old verion of calendar_source object
        :param p_new_src:       New verion of calendar_source object
        :param p_short_term:    If True: short term will be applied, nothing otherwise
        :return:                Returns filtered version of calendar source
        """
        # Apply short term filter
        if p_short_term:
            short_term_filter = ShortTermFilter(SHORT_TERM_WINDOW)
            p_old_src.set_event_list(short_term_filter.filter_calendar_source(p_old_src))
            short_term_filter2 = ShortTermFilter(SHORT_TERM_WINDOW)
            p_new_src.set_event_list(short_term_filter2.filter_calendar_source(p_new_src))

        # Apply regular filters
        p_new_src.apply_filters()
        new_filtered_location = CalendarSources.generate_new_file_name(ICS_TMP_STORE)
        p_new_src.set_filtered_source_location(new_filtered_location)
        self.__io.write_to_file(p_new_src, new_filtered_location)
        return p_old_src,p_new_src

    @staticmethod
    def __delete_file(filename):
        try:
            os.remove(filename)
        except OSError:
            pass

    @staticmethod
    def __changes_detected(result):
        """
        Checks the result for changes
        :param result:  3-tuple containing added, changed and removed event_lists
        :return:        If all 3 lists are empty: Return False, True otherwise
        """
        if result[0] == [] and result[1] == [] and result[2] == []:
            return False
        return True

    @staticmethod
    def __get_new_version(p_cal_src):
        if p_cal_src.get_source_type() == CalendarSources.URL:
            return p_cal_src.get_source_url()
        return None

from cal_tool.event_updates.event_changes import event_changes
from cal_tool.event_updates.event_matching import event_matching_factory, EventMatchingStrategies
from cal_tool.event_updates.merge_strategy import merge_factory, MergeStrategies
from cal_tool.event_updates.event_change_strategy import event_change_factory, EventChangeStrategies
from cal_tool.calendar.calendar_io import io_factory
from cal_tool.models import Users, Calendars, CalendarSources, Filters
from cal_tool.random_generator.random_generator import RandomGenerator
from Project.settings import ICS_TMP_STORE
from cal_tool.calendar.calendar_source import calendar_source
from cal_tool.filter.ShortTermFilter import ShortTermFilter
from cal_tool.event_updates.event_compare import *
from cal_tool.singletons.settings_manager_starter import settings_manager

IO_STRATEGY = io_factory.DEFAULT
EVENT_CHANGE_STRATEGY = settings_manager.get_active_event_change_strategy()
DATETIME_EVENT_COMPARE_STRATEGY = EventCompareStrategies.DATETIME_EVENT_COMPARE
MATCHING_STRATEGY = EventMatchingStrategies.FUZZY_EVENT_MATCHING
MERGE_STRATEGY = MergeStrategies.DEFAULT_MERGE
SHORT_TERM_WINDOW = 14