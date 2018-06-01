import datetime

now = datetime.datetime.now()
print(now)

future = now + datetime.timedelta(weeks=1)
print(future)