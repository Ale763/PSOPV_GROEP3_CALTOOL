from django.urls import path,include
from cal_tool.plugin.uhasselt import views

views = views.UHasseltViewPlugin()

urlpatterns = [
    path("newcalendar/", views.newcalendar, name="newcalendar"),
    path("mycalendars/", views.mycalendars, name="mycalendars"),
    path("profile/", views.settings, name="profile"),

]
