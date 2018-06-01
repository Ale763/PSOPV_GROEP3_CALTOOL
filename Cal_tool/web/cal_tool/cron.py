import datetime
import pytz


# def fromutc(dt):
#     # raise ValueError error if dt.tzinfo is not self
#     dtoff = dt.utcoffset()
#     dtdst = dt.dst()
#     # raise ValueError if dtoff is None or dtdst is None
#     delta = dtoff - dtdst  # this is self's standard offset
#     if delta:
#         dt += delta   # convert to standard local time
#         dtdst = dt.dst()
#         # raise ValueError if dtdst is None
#     if dtdst:
#         return dt + dtdst
#     else:
#         return dt

def full_check_updates():
    print("{0}: Started full check...".format(now))
    update_manager.update_calendars()
    print("{0}: Full check done".format(now))

def short_term_check_updates():
    print("{0}: Started short check...".format(now))
    update_manager.update_calendars(p_short_term=True)
    print("{0}: Short check done".format(now))

now = datetime.datetime.now()
#now = fromutc(now)

from cal_tool.singletons.update_manager_starter import update_manager
