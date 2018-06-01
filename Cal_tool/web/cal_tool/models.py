from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from cal_tool.random_generator.random_generator import RandomGenerator
from django.db.models import Q

TIMEZONE = 'Europe/Brussels'
import datetime
import pytz

def fromutc(dt):
    # raise ValueError error if dt.tzinfo is not self
    dtoff = dt.utcoffset()
    dtdst = dt.dst()
    # raise ValueError if dtoff is None or dtdst is None
    delta = dtoff - dtdst  # this is self's standard offset
    if delta:
        dt += delta   # convert to standard local time
        dtdst = dt.dst()
        # raise ValueError if dtdst is None
    if dtdst:
        return dt + dtdst
    else:
        return dt

def utcnowfunc():
    brussels_tz = pytz.timezone(TIMEZONE)
    utc_tz = pytz.utc
    now = brussels_tz.localize(datetime.datetime.now())
    now = fromutc(now)
    return now


# Create your models here.

class UserManager(BaseUserManager):
    def __create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('Please give a valid username!')
        user = self.model(username=username, **extra_fields)
        user.set_unique_id(RandomGenerator.random_int())
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role', Users.USER)
        return self.__create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('role', Users.ADMIN)

        return self.__create_user(username, password, **extra_fields)

class Users(AbstractBaseUser):
    class Meta:
        verbose_name = ('User')
        verbose_name_plural = ('Users')
    USER = 0
    ADMIN = 1
    ROLES = (
        (USER, 'USER'),
        (ADMIN, 'ADMIN')
    )

    BASE = 0
    UHASSELT = 1
    CEGEKA = 2
    DOMAINS = (
        (BASE, 'BASE'),
        (UHASSELT, 'UHASSELT'),
        (CEGEKA, 'CEGEKA')
    )
    unique_id = models.BigIntegerField(primary_key=True, blank=False, null=False)
    username = models.CharField(max_length=30, null=False, default="User", unique=True)
    #password = models.CharField(max_length=200, blank=False, null=False)
    mail = models.EmailField(blank=False, null=True, unique=True)
    slacktoken = models.CharField(max_length=100, blank=False, null=True)
    slackchannel = models.CharField(max_length=50, blank=False, null=True)
    role = models.IntegerField(choices=ROLES, default=USER)
    last_login = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    domain = models.IntegerField(choices=DOMAINS, default=BASE)

    STAFF = [ADMIN]
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()

    @staticmethod
    def generate_new_id():
        new_id = RandomGenerator.random_int()
        while Users.objects.filter(unique_id=new_id).count() > 0:
            new_id = RandomGenerator.random_int()
        return new_id

    @staticmethod
    def test_empty():
        a = Users.objects.filter(username="admin")
        if a.exists():
            print("not empty")
        else:
            print("empty")

    @staticmethod
    def get_domain(p_uid):
        return Users.objects.filter(unique_id=p_uid).domain

    def __str__(self):  # __unicode__ on Python 2
        if self.username is not None and self.username != "":
            return self.username
        else:
            return self.mail

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def set_mail(self, p_mail):
        self.mail = p_mail

    def set_role(self, p_role):
        self.role = p_role

    def set_unique_id(self, p_unique_id):
        self.unique_id = p_unique_id

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def get_unique_id(self):
        return self.unique_id

    @property
    def is_staff(self):
        for role in self.STAFF:
            if self.role == role:
                return True
        return False

    @property
    def is_active(self):
        return True

# TODO:: Refine user profile approach
# class user_settings(models.Model):


class PasswordTokens(models.Model):
    class Meta:
        verbose_name_plural = "PasswordTokens"
    unique_id = models.OneToOneField(Users, primary_key=True, blank=False, null=False, on_delete=models.CASCADE)
    password_token = models.CharField(max_length=200, blank=False, null=False)
    timestamp = models.DateTimeField(blank=False, null=False, auto_now_add=True)


class Calendars(models.Model):
    class Meta:
        verbose_name_plural = "Calendars"
    # TODO:: Add available colors to CAL_COLORS
    BLUE = 0
    RED = 1
    CAL_COLORS = (
        (BLUE, "Blue"),
        (RED, "Red")
    )
    cal_id = models.BigIntegerField(primary_key=True, blank=False, null=False)
    unique_id = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE)
    cal_alias = models.CharField(max_length=30, blank=True, null=True)
    cal_color = models.CharField(max_length=20, choices=CAL_COLORS, default="Blue", blank=False, null=False)
    last_checked = models.DateTimeField(blank=False, null=False, auto_now_add=True)

    @staticmethod
    def generate_new_id():
        new_id = RandomGenerator.random_int()
        while Calendars.objects.filter(cal_id=new_id).count() >0:
            new_id = RandomGenerator.random_int()
        return new_id

    @staticmethod
    def get_calenders_from_user(user_id):
        return Calendars.objects.filter(unique_id=user_id)





class SharedCalendars(models.Model):
    class Meta:
        verbose_name_plural = "SharedCalendars"
    cal_id = models.ForeignKey(Calendars, blank=False, null=False, on_delete=models.CASCADE)
    mail = models.CharField(max_length=50, blank=False, null=True, unique=True)
    url = models.URLField(unique=True)
    password = models.CharField(max_length=200, blank=False, null=False)


class CalendarSources(models.Model):
    class Meta:
        verbose_name_plural = "CalendarSources"
    FILE = 0
    URL = 1
    CAL_SOURCE_TYPES = (
        (FILE, "File"),
        (URL, "URL")
    )
    cal_source_id = models.BigIntegerField(primary_key=True, blank=False, null=False)
    cal_id = models.ForeignKey(Calendars, blank=False, null=False, on_delete=models.CASCADE)
    cal_source_alias = models.CharField(max_length=30, blank=False, null=False, default="Source")
    source_location = models.FilePathField(blank=False, null=False)
    filtered_source_location = models.FilePathField(blank=False, null=False)
    url = models.URLField(null=True, blank=True)
    type = models.CharField(max_length=200, choices=CAL_SOURCE_TYPES, default="File",blank=False, null=False)

    @staticmethod
    def generate_new_id():
        new_id = RandomGenerator.random_int()
        a = CalendarSources.objects.filter(cal_source_id=new_id)
        while CalendarSources.objects.filter(cal_source_id=new_id).count() > 0:
            new_id = RandomGenerator.random_int()
        return new_id

    @staticmethod
    def generate_new_file_name(base):
        location = RandomGenerator.random_string()
        path = base + location
        while "/" in location or CalendarSources.objects.filter(source_location=path).count() > 0:
            location = RandomGenerator.random_string()
            path = base + location
        return path

    @staticmethod
    def get_source(p_last_updated):
        if not Filters.check_filters_changed(p_last_updated):
            return


class Filters(models.Model):
    class Meta:
        verbose_name_plural = "Filters"
    filter_id = models.BigIntegerField(primary_key=True, blank=False, null=False)
    cal_source_id = models.ForeignKey(CalendarSources, blank=False, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False, null=False)
    last_modified = models.DateTimeField(blank=False, null=False, auto_now_add=True)

    @staticmethod
    def check_filters_changed(p_cal_source_id, p_time):
        filters = Filters.objects.filter(cal_source_id=p_cal_source_id).filter(last_modified__gte=p_time)
        if not filters:
            return False
        else:
            return True

    @staticmethod
    def get_filters(p_cal_src):
        return Filters.objects.filter(cal_source_id=p_cal_src)


    @staticmethod
    def generate_new_id():
        new_id = RandomGenerator.random_int()
        while CalendarSources.objects.filter(cal_source_id=new_id).count() > 0:
            new_id = RandomGenerator.random_int()
        return new_id

class FilterAttributes(models.Model):
    class Meta:
        verbose_name_plural = "FilterAttributes"

    # TODO:: Add available colors to CAL_COLORS
    LOCATION = 0
    SUMMARY = 1
    DESCRIPTION = 2
    DTSTART = 3
    DTEND = 4
    STATUS = 5
    CLASS = 6
    PRIORITY = 7
    ORGANIZER = 8
    PROF = 9
    COURSE = 10
    COURSENUMBER = 11
    ROOM = 12
    TYPE = 13
    GROUP = 14
    CONTAINS = 15
    EQUAL = 16
    ATTRIBUTES = (
        (LOCATION, "Location"),
        (SUMMARY, "Summary"),
        (DESCRIPTION, "Description"),
        (DTSTART, "Start"),
        (DTEND, "End"),
        (STATUS, "Status"),
        (CLASS, "Class"),
        (PRIORITY, "Priority"),
        (ORGANIZER, "Organizer"),
        (PROF, "Prof"),
        (COURSE, "Course"),
        (COURSENUMBER, "CourseNumber"),
        (ROOM, "Room"),
        (TYPE, "Type"),
        (GROUP, "Group")
    )
    MODE = (
        (CONTAINS, "Contains"),
        (EQUAL, "Equal")
    )
    filter_id = models.ForeignKey(Filters, blank=False, null=False, on_delete=models.CASCADE)
    type = models.CharField(max_length=200, choices=ATTRIBUTES, default="Description",blank=False, null=False)
    mode = models.CharField(max_length=200, choices=MODE, default="Contains", blank=False, null=False)
    value = models.CharField(max_length=200, blank=True, null=False)
    not_value = models.BooleanField(null=False, default=False)





