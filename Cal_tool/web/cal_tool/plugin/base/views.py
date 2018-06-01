from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from cal_tool.filter.filter import Filter, FilterAttribute

import json
from cal_tool.utilities.fuzzy_string_matching import modified_damerau_levenshtein_strategy
from django.contrib.auth.hashers import BCryptSHA256PasswordHasher, make_password


class ViewPlugin:
    # this class redirects the pages towards the correct pages
    # inheriting this class as a plugin allows users to customize redirections into their own choice
    def __init__(self, p_template_path= "global/base.html", p_logo=""):
        self.__m_template_path = p_template_path
        self.__m_filter_attributes = filter_attributes

    def getTemplatePath(self):
        return self.__m_template_path


    def setTemplatePath(self,p_template_path):
        self.__m_template_path = p_template_path

    def setFilterAttributes(self, p_filter_attributes):
        self.__m_filter_attributes = p_filter_attributes

    def getFilterAttributes(self):
        return self.__m_filter_attributes

    #--------------------------------------------------------------------------------------------------------------------
    # Views
    @method_decorator(login_required)
    def newcalendar(self,request, context=None):
        if context is None:
            context = {}
        context["filter_attributes"] = self.getFilterAttributes()

        return render(request, 'new_calendar/newcalendar.html', context)

    @method_decorator(login_required(login_url='login'))
    def mycalendars(self, request, context={}):
        user_id = request.session['user_id']
        db_calendars = Calendars.objects.filter(unique_id=user_id)
        mycalendars = []

        for db_calendar in db_calendars:
            cal = calendar()
            cal.load_from_database(db_calendar.cal_id)
            mycalendars.append(cal)

        context = {}
        context['mycalendars'] = mycalendars

        id = request.GET.get('id')
        try:
            context['id'] = int(id)
        except:
            context['id'] = 0

        return self.redirect_mycalendars(request,context)

    def redirect_mycalendars(self, request,context = None):
        return render(request, 'my_calendars/mycalendars.html', {'context': context})


    @method_decorator(login_required)
    def make_calendar(self, request):

        #parser = request.session['plugin'].getSourcePlugin().getSourceWidgetInputParser()
        parser = SourceWidgetInputParser()
        context = {}
        # TODO:: Define filter_attributes in plugins
        filter_attributes = {}
        context["filter_attributes"] = filter_attributes
        # context["filter_attributes"] = self.getFilterAttributes()
        try:
            new_calendar = parser.get_sources(request)
        except EmptyAttributeError:
            context["error"] = "One of the fields was empty. Please fill in all required fields"
            return request.session.get("plugin").getViewPlugin().newcalendar(request, context)
        except CalendarOpeningException or ValueError:
            context["error"] = "The given calendar could not be opened. Verify that the calendar is not corrupt or that the url is correct."
            return request.session.get("plugin").getViewPlugin().newcalendar(request, context)
        except FileNotFoundError:
            context["error"] = "One of the requested files could not be opened or was not found."
            return request.session.get("plugin").getViewPlugin().newcalendar(request, context)
        except DuplicateNameError:
            context["error"] = "The name for your calendar already exists, please enter another name."
            return request.session.get("plugin").getViewPlugin().newcalendar(request, context)
        except Exception as e:
            context["error"] = "There was a problem processing the request."
            print(e)
            return request.session.get("plugin").getViewPlugin().newcalendar(request, context)

        # new_calendar = parser.get_sources(request)
        new_calendar_name = new_calendar.get_calendar_name()

        user_id = request.session.get("user_id")
        user = Users.objects.filter(unique_id=user_id)
        if user.count() == 0:
            context["error"] = "De gebruiker bestaat niet."
            return render(request, 'new_calendar/newcalendar.html', context)
        username = user[0].username

        new_calendar.save_to_database(username)

        id = new_calendar.get_id()
        #request.session[new_calendar_name] = new_calendar

        return HttpResponseRedirect("/mycalendars/?id="+str(id))


    @method_decorator(login_required)
    def export(self, request):
        cal_id = request.POST.get("cal_id")
        cal = calendar()
        cal.load_from_database(cal_id)

        local_path = cal.export()

        # File download
        file = open(local_path, "rb").read()
        response = HttpResponse(file, content_type="text/ics")
        response["Content-Disposition"] = 'attachment; filename="icaller_merged_cal.ics"'
        return response

    @method_decorator(login_required)
    def settings(self, request):
        user_id = request.session["user_id"]
        # user = Users.objects.filter(unique_id=user_id)
        context = settings_manager.to_dict()
        return render(request, "settings/settings.html", context)


    def load_events(self, request, id):
        event_list = []
        if "filteredsource" + str(id) in request.session and request.session["filteredsource" + str(id)] is not None :
            event_list.extend(request.session["filteredsource" + str(id)].event_list_to_string())
        else:
            if "source" + str(id) in request.session and request.session["source" + str(id)] is not None:
                event_list.extend(request.session["source" + str(id)].event_list_to_string())

        return JsonResponse(event_list, safe=False)

    @method_decorator(login_required)
    def user_settings(self,request):
        user_id = request.session['user_id']
        user = Users.objects.filter(unique_id=user_id)[0]
        context = {}
        context["email"]=user.mail
        context["username"]=user.username
        context["slacktoken"]=user.slacktoken
        context["slackchannel"]=user.slackchannel
        context["admin"]=user.is_admin
        return render(request, 'profile/settings.html', context)

    @method_decorator(login_required)
    def submit_profile(self, request):
        user_id = request.session['user_id']
        user = Users.objects.filter(unique_id=user_id)[0]
        slacktoken = self.__check_empty(request.POST.get("slacktoken"))
        slackchannel = self.__check_empty(request.POST.get("slackchannel"))
        username = self.__check_empty(request.POST.get("uname"))
        password1 = self.__check_empty(request.POST.get("password1"))
        password2 = self.__check_empty(request.POST.get("password2"))
        email = self.__check_empty(request.POST.get("email"))

        data_valid = True
        if username is None or (user.username != username and Users.objects.filter(username=username).exists()):
            data_valid = False
        if password1 is not None and password2 is not None and (
                password1 != password2 or len(password1) < 8 or len(password2) < 8):
            data_valid = False
        if email is not None and (user.mail != email and Users.objects.filter(mail=email).exists()):
            return False

        if data_valid:
            if password1 is not None:
                user.password = make_password(password1)
                user.username = username
                user.mail = email
                user.slackchannel = slackchannel
                user.slacktoken = slacktoken
                user.save()
                return True
            else:
                user.username = username
                user.mail = email
                user.slackchannel = slackchannel
                user.slacktoken = slacktoken
                user.save()
                return False
        return False

    @method_decorator(login_required)
    def save_settings(self, request):
        admin_input = {
            "event_change_strategy": request.POST.get("event_change_strategy"),
            "event_matching_strategy": request.POST.get("event_matching_strategy"),
            "merge_strategy": request.POST.get("merge_strategy"),
            "string_matching_strategy": request.POST.get("string_matching_strategy"),
            "fuzzy_string_word_treshold": request.POST.get("fuzzy_string_word_treshold"),
            "fuzzy_string_string_treshold": request.POST.get("fuzzy_string_string_treshold"),
            "sort_strategy": request.POST.get("sort_strategy"),
            "short_term_update_frequency": request.POST.get("short_term_update_frequency"),
            "long_interval": request.POST.get("long_interval"),
        }
        context = settings_manager.to_dict()
        for entry_key, entry_value in admin_input.items():
            if entry_value is None:
                context["basic_error"] = "Er was een probleem met de opgegeven waardes. Vul deze opnieuw correct in."
                return render(request, 'settings/settings.html', context)

        time = admin_input["long_interval"].split(":")
        admin_input["long_term_update_hour"] = time[0]
        admin_input["long_term_update_minutes"] = time[1]

        if settings_manager.set_settings(admin_input):
            context = settings_manager.to_dict()
            context["success"] = "De instellingen werden succesvol aangepast"
            return render(request, 'settings/settings.html', context)
        else:
            context["basic_error"] = "Er was een probleem met de opgegeven waardes. Vul deze opnieuw correct in."
            return render(request, 'settings/settings.html', context)

        data_valid = True
        if username is None or (user.username != username and Users.objects.filter(username=username).exists()):
            data_valid = False
        if password1 is not None and password2 is not None and (password1 != password2 or len(password1) < 8 or len(password2) < 8):
            data_valid = False
        if email is not None and (user.mail != email and Users.objects.filter(mail=email).exists()):
            return False

        if data_valid:
            if password1 is not None:
                updated_user = Users(unique_id=user_id, username=username, mail=email, slackchannel=slackchannel,
                    slacktoken=slacktoken, password=make_password( password1 ))
            else:
                updated_user = Users(unique_id=user_id, username=username, mail=email, slackchannel=slackchannel,
                    slacktoken=slacktoken)
            updated_user.save()

        return self.user_settings(request)

    def delete_profile(self, request):
        user_id = request.session['user_id']

        try:
            cal_list = Calendars.objects.filter(unique_id=user_id)
            for cal in cal_list:
                shared_list = SharedCalendars.objects.filter(cal_id=cal.cal_id)
                cal_source_list = CalendarSources.objects.filter(cal_id=cal.cal_id)
                for cal_source in cal_source_list:
                    if cal_source.source_location is not None:
                        os.remove(cal_source.source_location)
                    if cal_source.filtered_source_location is not None:
                        os.remove(cal_source.filtered_source_location)

                for shared_cal in shared_list:
                    if shared_cal.url is not None:
                        os.remove(shared_cal.url+".ics")
        except Exception:
            print("Something went wrong deleting all the calendars")

        user = Users.objects.filter(unique_id=user_id)[0]
        user.delete()

        return JsonResponse("", safe=False)

    def __check_empty(self, string):
        if string is not None and string == "":
            return None
        else:
            return string

    def save_filter(self, request):
        data = json.loads(request.POST.get('data', None))
        id = request.POST.get('id', None)

        request.session["filter" + str(id)] = None
        request.session["filteredsource" + str(id)] = None

        filter_list = []

        for filter in data:
            new_id = Filters.generate_new_id()
            new_filter = Filter(new_id, filter[0])
            for filterAttribute in filter[1]:
                value = new_filter.string_to_datetime(filterAttribute["TYPE"], filterAttribute["VALUE"])
                new_filter.add_attribute(filterAttribute["TYPE"], filterAttribute["MODE"], filterAttribute["NOT"], value)
            filter_list.append(new_filter)

        request.session["filter"+str(id)] = filter_list

        if "source"+str(id) in request.session and request.session.get("source"+str(id), None) is not None:
            self.filter_source(request)

        return self.load_events(request, int(id))


    # TODO:: JEF SUFFELEERS VRAGEN OM TE VERPLAATSEN
    def filter_source(self, request):
        id = request.POST.get('id', None)
        calendar = request.session.get("source"+str(id), None)
        filters = request.session.get("filter"+str(id), None)
        if calendar != None and filters != None:
            new_cal = calendar_source()
            new_cal.copy_calendar_source(calendar)
            new_cal.add_multiple_filters(filters)
            new_cal.apply_filters()
            request.session["filteredsource" + str(id)] = new_cal
            pass

        elif calendar != None:
            request.session["filteredsource" + str(id)] = calendar

    def add_source(self, request):
        id = request.POST.get('id', None)
        source = request.POST.get('source', None)
        try:
            if source is None:
                raise CalendarOpeningException("Geen bron gevonden")

            cal_io = default_calendar_io()
            calendarsource = cal_io.parse_file(source)
            request.session["source" + str(id)] = calendarsource
            self.filter_source(request)
            return HttpResponse("Ok")

        except CalendarOpeningException:
            request.session["source" + str(id)] = None
            return HttpResponse("Ok")


    def share_calendar(self, request):
        email = request.POST.get('email', None)
        if email == "":
            email = None
        cal_id = request.POST.get('id', None)
        password = request.POST.get('password', None)
        share = ShareCalendar()
        url = share.share_calendar(int(cal_id), email, password)

        if url is None:
            return HttpResponse("Ok")
        else:
            return JsonResponse(url, safe=False)

    def check_houres_filter(self, request):
        cal_id = request.POST.get('id', None)
        filter_value = request.POST.get('filter_value', None)
        cal = calendar()
        cal.load_from_database(int(cal_id))
        calendar_sources = cal.get_sources()

        time = 0

        for source in calendar_sources:
            temp_time = 0
            filter = Filter(-1, "check_houres_filter")
            filter.add_attribute("DESCRIPTION", "CONTAINS", False, filter_value)
            temp_time += source.apply_time_filter(filter)

            if temp_time == 0:
                filter2 = Filter(-2, "check_houres_filter2")
                filter2.add_attribute("SUMMARY", "EQUAL", False, filter_value)
                temp_time += source.apply_time_filter(filter2)

            time += temp_time

        return JsonResponse(time, safe=False)

    def share_emails(self, request):
        cal_id = request.POST.get('id', None)
        share = ShareCalendar()
        emails = share.share_emails(int(cal_id))
        return JsonResponse(emails, safe=False)

    def delete_calendar(self, request):
        cal_id = request.POST.get('id', None)
        calendar = Calendars.objects.filter(cal_id=int(cal_id))[0]
        calendar.delete()
        return HttpResponse("Ok")

    def add_shared_email(self, request):
        cal_id = request.POST.get("id")
        email = request.POST.get("shareEmail")

        share = ShareCalendar()
        share.share_calendar(int(cal_id), email)

        return HttpResponse("Ok")

    def check_strings(self, request):
        stra = request.POST.get("string1", None)
        strb = request.POST.get("string2", None)

        word_treshold = request.POST.get("word_treshold", None)
        string_treshold = request.POST.get("string_treshold", None)

        str_check_failed, word_treshold_faulty, string_treshold_faulty = self.test_check_string_input(request)

        if str_check_failed or word_treshold_faulty or string_treshold_faulty:
            data = {
                "match_failed": str_check_failed,
                "word_treshold_faulty": word_treshold_faulty,
                "string_treshold_faulty": string_treshold_faulty
            }
            return JsonResponse(data, safe=False)
        else:
            word_treshold = int(word_treshold)
            string_treshold = int(string_treshold)

        settings_manager.set_word_treshold(word_treshold)
        settings_manager.set_string_treshold(string_treshold)

        damerau_levenshtein = modified_damerau_levenshtein_strategy()
        match = damerau_levenshtein.match(stra, strb)
        data = {
            "match_failed": not match,
            "word_treshold_faulty": word_treshold_faulty,
            "string_treshold_faulty": string_treshold_faulty
        }
        return JsonResponse(data, safe=False)

    @staticmethod
    def test_check_string_input(request):
        stra = request.POST.get("string1", None)
        strb = request.POST.get("string2", None)
        word_treshold = request.POST.get("word_treshold", None)
        string_treshold = request.POST.get("string_treshold", None)

        str_check_failed = word_treshold_faulty = string_treshold_faulty = False

        if stra is None or strb is None:
            str_check_failed = True

        try:
            word_treshold = int(word_treshold)
        except Exception:
            word_treshold = None

        try:
            string_treshold = int(string_treshold)
        except Exception:
            string_treshold = None

        if word_treshold is None:
            word_treshold_faulty = True
        elif word_treshold <= 0 or word_treshold >100:
            word_treshold_faulty = True

        if string_treshold is None:
            string_treshold_faulty = True
        elif string_treshold <= 0 or string_treshold >100:
            string_treshold_faulty = True

        return str_check_failed, word_treshold_faulty, string_treshold_faulty






    def delete_shared_email(self, request):
        cal_id = request.POST.get("id")
        email = request.POST.get("shareEmail")

        share = ShareCalendar()
        share.delete_shared_email(int(cal_id), email)

        return HttpResponse("Ok")


    def load_eventchange(self, request):
        return render(request, "global/eventchange.html")


    def get_notifications(self, request):
        email = request.GET.get('email', None)
        notifications = NOTIFICATION_APP
        return JsonResponse(notifications.get_personal_browser_notifications(email), safe=False)

    def getfilterhtml(self, request):
        return render(request, 'new_calendar/filter/filter.html')


from cal_tool.calendar.calendar_source import calendar_source
from cal_tool.calendar.calendar_io import default_calendar_io
from cal_tool.plugin.base.controller.source_widget_input_parser import DuplicateNameError
from cal_tool.calendar.calendar_io import CalendarOpeningException
from cal_tool.plugin.base.controller.source_widget_input_parser import SourceWidgetInputParser, EmptyAttributeError
from cal_tool.plugin.base.filter_attributes import filter_attributes

from django.contrib import auth
from cal_tool.models import *

from Project.settings import ICS_TMP_STORE
from django.http import JsonResponse
from cal_tool.singletons.notifications_starter import NOTIFICATION_APP
from cal_tool.event_updates.event_changes import event_changes
from cal_tool.calendar.calendar import calendar
from cal_tool.calendar.share_calendar import ShareCalendar
# from cal_tool.plugin.uhasselt.uhasselt import UhasseltPlugin
from cal_tool.singletons.settings_manager_starter import settings_manager
SETTINGS_MANAGER = settings_manager
import os