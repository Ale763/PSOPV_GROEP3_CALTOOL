from django.core.management.base import BaseCommand, CommandError
from cal_tool.cron import full_check_updates
import datetime

class Command(BaseCommand):
    args = ''
    help = 'Check all calendars per user for changes'

    def handle(self, *args, **options):
        # do something here
        full_check_updates()
        with open("/data/web/long.log", "a") as file:
            file.write("{0}: Long term checking done.\n".format(datetime.datetime.now()))

