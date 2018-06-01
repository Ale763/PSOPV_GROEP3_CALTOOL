from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Users)
admin.site.register(PasswordTokens)
admin.site.register(Calendars)
admin.site.register(CalendarSources)
admin.site.register(SharedCalendars)
admin.site.register(Filters)
admin.site.register(FilterAttributes)
