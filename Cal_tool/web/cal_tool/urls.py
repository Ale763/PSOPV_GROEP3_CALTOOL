from django.urls import path
from cal_tool import views

handler404 = views.handler404

#TODO:: Remove test paths

urlpatterns = [
    path("", views.mycalendars, name="index"),
    path("newcalendar/filter.html", views.getfilterhtml, name="filterhtml"),
    path("submit_registration/", views.submit_registration, name="submit_registration"),
    path("ajax/uname_checker/", views.uname_checker, name="uname_checker"),
    path("ajax/email_checker/", views.email_checker, name="email_checker"),
    path("login/", views.login, name="login"),
    path("authenticate/", views.authenticate, name="authenticate"),
    path("invalidloggin/", views.invalidlogin, name="invalidlogin"),
    path("loginrequired/", views.loginrequired, name="loginrequired"),
    path("logout/", views.logout, name="logout"),
    path("eventchange/", views.load_eventchange, name='eventchange'),
    path("ajax/check_notifications/", views.get_notifications, name='check_notifications'),
    path("ajax/share_url/", views.share_calendar, name='share_calendar'),
    path("ajax/share_emails/", views.share_emails, name='share_emails'),
    path("ajax/add_shared_emails/", views.add_shared_email, name='add_shared_emails'),
    path("ajax/delete_shared_email/", views.delete_shared_email, name='delete_shared_emails'),
    path("ajax/delete_calendar/", views.delete_calendar, name='delete_calendar'),
    path("ajax/check_houres_filter/", views.check_houres_filter, name="check_houres_filter"),
    path("ajax/save_filter/", views.save_filter, name="save_filter"),
    path("ajax/add_source/", views.add_source, name="add_source"),
    path("ajax/check_strings/", views.check_strings, name="check_strings"),
    path("ajax/load_events/", views.load_events, name="load_events"),
    path("submit_profile", views.submit_profile, name="submit_profile"),
    path("user_settings/", views.user_settings, name="user_settings"),
    path("ajax/delete_profile/", views.delete_profile, name="delete_profile"),
    path("newcalendar/", views.newcalendar, name="newcalendar"),
    path("mycalendars/", views.mycalendars, name="mycalendars"),
    path("make_calendar/", views.make_calendar, name="make_calendar"),
    path("export/", views.export, name="export"),
    path("settings/", views.settings, name="settings"),
    path("save_settings/", views.save_settings, name="save_settings"),
    path("profile/", views.settings, name="profile"),
    path("test/", views.test, name="test"),
    path("registration/", views.registration, name="registration"),
]