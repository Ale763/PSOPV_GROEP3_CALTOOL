from django.core.management.base import BaseCommand, CommandError
from cal_tool.cron import short_term_check_updates
import datetime

class Command(BaseCommand):
    args = ''
    help = 'Check all calendars per user for changes on the short term'

    def handle(self, *args, **options):
        # do something here
        short_term_check_updates()
        with open("/data/web/short.log", "a") as file:
            file.write("{0}: Short term checking done.\n".format(datetime.datetime.now()))
