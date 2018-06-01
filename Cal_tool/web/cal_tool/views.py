from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import JsonResponse
from cal_tool.models import Calendars
from cal_tool.plugin.uhasselt.uhasselt import *


#TODO fix this function
def handler404(request, param):
    if not param:
        return HttpResponseNotFound('<h1>No Page Here</h1>')

    return render(request, 'my_calendars/mycalendars.html')

def save_to_database(request):
    return HttpResponse("Save to database")

def getfilterhtml(request):
    return request.session['plugin'].getViewPlugin().getfilterhtml(request)

def add_source(request):
    return request.session['plugin'].getViewPlugin().add_source(request)

def save_filter(request):
    return request.session['plugin'].getViewPlugin().save_filter(request)

def share_calendar(request):
    return request.session['plugin'].getViewPlugin().share_calendar(request)

def check_houres_filter(request):
    return request.session['plugin'].getViewPlugin().check_houres_filter(request)

def share_emails(request):
    return request.session['plugin'].getViewPlugin().share_emails(request)

def delete_calendar(request):
    return request.session['plugin'].getViewPlugin().delete_calendar(request)

def add_shared_email(request):
    return request.session['plugin'].getViewPlugin().add_shared_email(request)

def delete_shared_email(request):
    return request.session['plugin'].getViewPlugin().delete_shared_email(request)


def load_eventchange(request):
    return request.session['plugin'].getViewPlugin().load_eventchange(request)

def submit_profile(request):
    password_changed = request.session['plugin'].getViewPlugin().submit_profile(request)

    if password_changed:
        auth.logout(request)
        uname = request.POST.get('uname', '')
        password = request.POST.get('password1', '')
        user = auth.authenticate(username=uname, password=password)

        if user is not None:
            auth.login(request, user)
            request.session['user_id'] = user.get_unique_id
            registration_handler.set_user_plugin(request, user)


    return request.session['plugin'].getViewPlugin().user_settings(request)

def delete_profile(request):
    return request.session['plugin'].getViewPlugin().delete_profile(request)

def check_strings(request):
    return request.session['plugin'].getViewPlugin().check_strings(request)


def get_notifications(request):
    return request.session['plugin'].getViewPlugin().get_notifications(request)

# ------------------------------------------------------------------------------------------------
# Login & Registration

def load_events(request):
    return request.session['plugin'].getViewPlugin().load_events(request)

def user_settings(request):
    return request.session['plugin'].getViewPlugin().user_settings(request)
#LOGGIN FUNCTIONS: THEY DONT NEED A PLUGIN HENCE THEY ARENT LOGGED IN


#TODO don't go to login when allready logged in!!


def registration(request):
    user_logged_in = BaseRegistrationInputParser.check_login_status(request)
    if user_logged_in:
        return redirect("/mycalendars")

    context = {}
    context["domains"] = {}
    plugins = registration_handler.get_installed_plugins()
    for i in range(len(plugins)):
        context["domains"][str(i)] = plugins[i].getName()

    mex = messages.get_messages(request)

    for message in mex:
        context[message.extra_tags] = message.message

    return render(request, 'registration/registration.html', context)


def submit_registration(request):
    # from cal_tool.singletons.settings_manager_starter import settings_manager
    # If all is ok, to login

    user_logged_in = BaseRegistrationInputParser.check_login_status(request)
    if user_logged_in:
        return redirect("/mycalendars")

    domain = request.POST.get("domain")

    if domain is None or not registration_handler.is_number(domain):
        redirect("/registration")

    # Retrieve plugin based on user choice
    plugin_number = int(domain)
    plugins = registration_handler.get_plugins()
    plugin = plugins[plugin_number]
    parser = plugin.getRegistrationParser()
    success, parsed_input = parser.parse_input(request)

    if success:
        # Log user in and redirect to newcalendar page
        username = parsed_input["uname"]["value"]
        password = parsed_input["password1"]["value"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user_id'] = user.get_unique_id

            registration_handler.set_user_plugin(request, user)
            return HttpResponseRedirect('/newcalendar')
        return HttpResponseRedirect("/registration")
    else:
        # Use of django message system to send messages across redirect routes
        mex = messages.get_messages(request)
        # Empty messages
        for message in mex:
            a = message.message
        # Actually fill messages with needed info
        for key, value in parsed_input.items():
            messages.add_message(request, messages.INFO, value["value"], key)
        messages.add_message(request, messages.INFO, parsed_input)
        return redirect("/registration")


def uname_checker(request):
    uname = request.GET.get("uname", None)
    data = { "available": Users.objects.filter(username=uname).count() == 0 }
    return JsonResponse(data)


def email_checker(request):
    email = request.GET.get("email", None)
    matching_mails = Users.objects.filter(mail=email).exclude(mail__isnull=True).exclude(mail__exact='')
    data = { "available": matching_mails.count() == 0 }
    return JsonResponse(data)


def login(request):
    user_logged_in = BaseRegistrationInputParser.check_login_status(request)
    if user_logged_in:
        return redirect("/mycalendars")

    return render(request, 'login/login.html')


# TODO:: move to settings
    #TODO Choose logical plugin

# authenticating user when logging in
def authenticate(request):
    user_logged_in = BaseRegistrationInputParser.check_login_status(request)
    if user_logged_in:
        return redirect("/mycalendars")

    uname = request.POST.get('uname', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=uname, password=password)


    if user is not None:
        auth.login(request, user)
        request.session['user_id'] = user.get_unique_id

        registration_handler.set_user_plugin(request, user)
        return HttpResponseRedirect('/mycalendars')
    else:
        return HttpResponseRedirect('/invalidloggin')

def loginrequired(request):
    return render(request,'login/login_required.html')


def invalidlogin(request):
    user_logged_in = BaseRegistrationInputParser.check_login_status(request)
    if user_logged_in:
        return redirect("/mycalendars")
    return render(request, 'login/invalid_login.html')


def logout(request):
    auth.logout(request)
    return login(request)

def test(request):
    from cal_tool.cron import full_check_updates, short_term_check_updates
    short_term_check_updates()
    full_check_updates()
    return HttpResponse("OK")

# ------------------------------------------------------------------------------------------------
# Plugin functionality

@login_required
def newcalendar(request):
    return request.session['plugin'].getViewPlugin().newcalendar(request)


@login_required
def mycalendars(request):
    return request.session['plugin'].getViewPlugin().mycalendars(request)


@login_required
def make_calendar(request):
    viewplugin =request.session['plugin'].getViewPlugin()
    return viewplugin.make_calendar(request)


@login_required
def export(request):
    return request.session['plugin'].getViewPlugin().export(request)


@login_required
def settings(request):
    user = Users.objects.get(unique_id=request.session["user_id"])
    if user.is_admin:
        return request.session['plugin'].getViewPlugin().settings(request)
    return redirect("mycalendars")

@login_required
def save_settings(request):
    return request.session['plugin'].getViewPlugin().save_settings(request)
    # user = Users.objects.get(unique_id=request.session["user_id"])
    # if user.is_admin:
    #     return request.session['plugin'].getViewPlugin().save_settings(request)
    # return redirect("mycalendars")



from django.shortcuts import HttpResponseRedirect, redirect, render
# from cal_tool.plugin.cegeka.cegeka import CegekaPlugin
from django.http import HttpResponseNotFound, HttpResponse
# from django.urls import reverse

from django.contrib import messages
from cal_tool.models import Users
from cal_tool.plugin.base.controller.registration_input_parser import BaseRegistrationInputParser
from cal_tool.singletons.registration_starter import registration_handler


