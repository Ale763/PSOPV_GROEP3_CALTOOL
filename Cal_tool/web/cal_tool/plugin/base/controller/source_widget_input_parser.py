class UnknownSourceType(Exception):
    def __init__(self, p_value):
        self.__value = p_value

    def __str__(self):
        return repr(self.__value)

class EmptyAttributeError(Exception):
    def __init__(self, p_value):
        self.__value = p_value

    def __str__(self):
        return repr(self.__value)

class DuplicateNameError(Exception):
    def __init__(self, p_value):
        self.__value = p_value

    def __str__(self):
        return repr(self.__value)

class SourceWidgetInputParser:
    def __init__(self):
        self.__sources_count = 0
        self.__save_location = ICS_SAVED_STORE
        self.__tmp_save_location = ICS_TMP_STORE
        self.__io = default_calendar_io()
        self.__request = None

    def get_sources(self, request):
        """
        Parses sources and returns a fully parsed calendar object
        :param request:
        """
        self.__request = request

        new_calendar = calendar()
        new_calendar_name = self.__check_and_get_post("newCalendarName")
        new_calendar.set_calendar_name(new_calendar_name)
        new_calendar_color = self.__check_and_get_post("newCalendarColor")
        new_calendar.set_calendar_color(new_calendar_color)
        widget_count = self.get_widget_count(request)

        if Calendars.objects.filter(cal_alias=new_calendar_name, unique_id=request.session['user_id']).exists():
            raise DuplicateNameError("The name for your calendar already exists, please enter another name.")

        all_source_names = []

        for i in range(widget_count):
            current_id = str(i)
            source_type = self.__check_and_get_post("sourceType"+current_id)

            if source_type == 'file':
                file = self.__check_and_get_files("fileInput"+current_id)
                src = self.__handle_file_upload(file)
            elif source_type == 'url':
                url = self.__check_and_get_post("urlInput"+current_id)
                src = self.__handle_url_upload(url)
            elif source_type == 'source':
                info = self.__check_and_get_post("sourceInput" + current_id)
                src = self.__handle_source_upload(info)
            else:
                raise UnknownSourceType("The specified sourcetype is unknown. Only url and file sourcetypes are supported.")

            source_name = self.__check_and_get_post("calendarName" + current_id)

            if source_name in all_source_names:
                raise DuplicateNameError("The name for your calendar already exists, please enter another name.")

            all_source_names.append(source_name)
            src.set_source_name(source_name)

            if "filter"+current_id in request.session:
                src.add_multiple_filters(request.session["filter"+current_id])

            new_calendar.add_source(src)

        self.__empty_session(request, widget_count)

        return new_calendar

# TODO:: Add filtering with input parsing

    def __handle_source_upload(self,info):
        info = info.split(";/")
        if info[1] == "URL":
            return self.__handle_url_upload(info[0])
        else:
            return self.__handle_file_upload(info[0])

    def __empty_session(self, request, p_count):
        for i in range(p_count):
            request.session["filter"+str(i)] = None
            request.session["filteredsource" + str(i)] = None
            request.session["source" + str(i)] = None


    def __handle_file_upload(self, file):
        if file is not None and file != "":
            location = CalendarSources.generate_new_file_name(self.__tmp_save_location)
            self.__save_file(file, location)
            cal_source = self.__io.parse_file(location)
            # cal_source.apply_filters()
            cal_source.set_source_type(CalendarSources.FILE)
            return cal_source
        raise EmptyAttributeError("The fileupload was empty")

    def __handle_url_upload(self, url):
        if url is not None and url != "":
            cal_source = self.__io.parse_file(url)
            file = self.__io.open_source(url, "rb")
            location = CalendarSources.generate_new_file_name(self.__tmp_save_location)
            self.__save_file(file, location)
            cal_source.set_source_location(location)
            cal_source.set_source_url(url)
            cal_source.set_source_type(CalendarSources.URL)
            # cal_source.apply_filters()
            return cal_source
        raise EmptyAttributeError("The fileupload was empty")

    def __check_and_get_post(self, attribute):
        requested = self.__request.POST.get(attribute)
        if requested is not None and requested != "":
            return requested
        raise AttributeError("Requested attribute does not exist or is empty!")

    def __check_and_get_files(self, attribute):
        requested = self.__request.FILES.get(attribute)
        if requested is not None and requested != "":
            return requested
        raise AttributeError("Requested attribute does not exist or is empty!")

    @staticmethod
    def __save_file(file, location):
        """
        Saves given file to given location
        :param file:    Accepts a request.FILES[key] argument
        :type location: Location to which to save file to

        """
        with open(location, 'wb') as destination:
            destination.write(file.read())
            # for chunk in file.read(1024):
            #     destination.write(chunk)

    def get_widget_count(self, request):
        post = request.POST
        i = 0
        a = post.get("calendarName" + str(i))
        while a is not None:
            i += 1
            a = post.get("calendarName" + str(i))
        self.__sources_count = i
        return i


from cal_tool.calendar.calendar_io import default_calendar_io
#from cal_tool.calendar.calendar_source import SourceType
from cal_tool.calendar.calendar import *
from cal_tool.models import *
from Project.settings import ICS_TMP_STORE, ICS_SAVED_STORE