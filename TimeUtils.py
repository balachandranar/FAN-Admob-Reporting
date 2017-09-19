import time
import dateutil.parser

OUR_DATE_FORMAT = '%Y-%m-%d'


def epoch_to_date(epoch_secs):
    return time.strftime(OUR_DATE_FORMAT, time.gmtime(epoch_secs))


def date_string_to_epoch_int(date_string):
    return int(time.mktime(time.strptime(date_string, OUR_DATE_FORMAT)))


def fb_report_date_to_datetime(fan_report_date):
    date = dateutil.parser.parse(fan_report_date)
    return date
