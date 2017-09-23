import time

import dateutil.parser

OUR_DATE_FORMAT = '%Y-%m-%d'


def epoch_to_date(epoch_secs):
    return time.strftime(OUR_DATE_FORMAT, time.gmtime(epoch_secs))


def date_string_to_epoch_int(date_string):
    # Since IST is 12 hours 30 minutes ahead of PST (which is FAN's time zone) we need to add 45000 seconds
    return int(time.mktime(time.strptime(date_string, OUR_DATE_FORMAT))) + 45000


def fb_report_date_to_datetime(fan_report_date):
    date = dateutil.parser.parse(fan_report_date)
    return date


def datetime_to_date_string(datetime_obj):
    date = datetime_obj.strftime(OUR_DATE_FORMAT)
    return date
