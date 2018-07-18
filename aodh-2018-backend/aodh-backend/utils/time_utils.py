import datetime
import time
from dateutil import tz

def str_2_datetime(str_in, input_format='%Y-%m-%d', timezone='JST'):
    #separator = find_sep(input_format)
    #struct_time = str_2_struct_time(str_in, input_format=input_format)
    response = datetime.datetime.strptime(str_in, input_format)
    # # todo
    # if timezone == 'JST':
    #     response_with_timezone = response.replace(tzinfo=pytz.timezone('Japan'))
    # else:
    #     # todo not implemented
    #     response_with_timezone = response.replace(tzinfo=pytz.timezone('Japan'))

    return response


def datetime_2_str(datetime_in, output_format='%Y-%m-%d'):
    return time.strftime(output_format, datetime_in.timetuple())


def normalize_time(t, format='%a %b %d %H:%M:%S %z %Y'):
    #twitter_time_format = '%a %b %d %H:%M:%S %z %Y'

    t_now = datetime.datetime.now(tz=tz.tzutc())
    #t = 'Sat Jul 15 06:41:28 +0000 2018'  # input time
    t_tw = datetime.datetime.strptime(t, format)

    t_diff = t_now - t_tw
    t_diff_hr = t_diff.seconds / 60 / 60

    if t_diff_hr <= 24.0:
        output = t_diff_hr / 24
    else:
        output = 0

    return output
