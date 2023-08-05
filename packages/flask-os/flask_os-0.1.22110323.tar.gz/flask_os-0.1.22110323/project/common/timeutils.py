import os
import pytz
import time
from datetime import datetime


def set_init_pytz(tz):
    os.environ["TZ"] = tz
    time.tzset()


def time2str(src_time, dst_tz, date_format="%Y-%m-%d %H:%M:%S"):
    date = datetime.utcfromtimestamp(src_time)
    return date.astimezone(tz=dst_tz).strftime(date_format)


def date2time(src_date, src_tz, date_format="%Y-%m-%d %H:%M:%S"):
    date = datetime.strptime(src_date, date_format)
    date = date.replace(tzinfo=pytz.timezone(src_tz))
    return date.timestamp()
