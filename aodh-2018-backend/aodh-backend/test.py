import datetime
from dateutil import tz


def normalize_time(t):
    twitter_time_format = '%a %b %d %H:%M:%S %z %Y'

    t_now = datetime.datetime.now(tz=tz.tzutc())
    #t = 'Sat Jul 15 06:41:28 +0000 2018'  # input time
    t_tw = datetime.datetime.strptime(t, twitter_time_format)

    t_diff = t_now - t_tw
    t_diff_hr = t_diff.seconds / 60 / 60

    if t_diff_hr <= 24.0:
        output = 2 / 24
    else:
        output = 0

    return output

t = 'Sat Jul 15 06:41:28 +0000 2018'  # input time
r = normalize_time(t)
print(r)