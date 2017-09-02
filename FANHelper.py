
import requests
import time

import GraphUtils
import TimeUtils


def get_and_plot_fan_data(fan_app_id, fan_access_token):

    fan_res = fan_api_request(fan_app_id, fan_access_token, 1496793600, int(time.time()))

    if fan_res.status_code == 200:
        data = fan_res.json()['data']
        y_values = []
        x_time_array = []
        for datum in data:
            x_time_array.append(TimeUtils.fb_report_date_to_datetime(datum['time']))
            y_values.append(float(datum['value']))
        GraphUtils.plot_time_series(x_time_array, y_values, "Revenue", "$")
    else:
        print("Bad Response. Code :" + str(fan_res.status_code))


def fan_api_request(app_id, access_token, from_epoch_secs, to_epoch_secs, event_name ="fb_ad_network_revenue", agg_by ="SUM"):

    url = "https://graph.facebook.com/v2.10/" + app_id + "/app_insights/app_event/?"\
    "since="+str(from_epoch_secs)+"&"\
    "until="+str(to_epoch_secs)+"&"\
    "summary=true&"\
    "event_name=" + event_name + "&"\
    "aggregateBy=" + agg_by + "&"\
    "access_token=" + access_token

    res = requests.get(url)

    return res