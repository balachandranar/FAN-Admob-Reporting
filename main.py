import sys

import time

import FANHelper
import GraphUtils
import TimeUtils
import GoogleApiHelper


def get_and_plot_ads_revenue_data(fan_app_id, fan_access_token, from_time, to_time):
    #Getting the FAN revenue data
    fan_res = FANHelper.fan_api_request(fan_app_id, fan_access_token, from_time, to_time)

    if fan_res.status_code == 200:
        data = fan_res.json()['data']
        fan_y_values = []
        x_time_array = []
        for datum in data:
            x_time_array.append(TimeUtils.fb_report_date_to_datetime(datum['time']))
            fan_y_values.append(float(datum['value']))

        # Getting the Google Admob revenue data
        admob_service = GoogleApiHelper.init_auth()
        value_tuple = GoogleApiHelper.get_earnings(admob_service, TimeUtils.epoch_to_date(from_time),
                                                   TimeUtils.epoch_to_date(to_time))

        admob_values = []
        for i in value_tuple:
            admob_values.append(float(i[1]))

        total_y_values = []
        for i, _ in enumerate(x_time_array):
            total_y_values.append(fan_y_values[i] + admob_values[i])

        y_values = [fan_y_values, admob_values, total_y_values]

        # we got all the necessary data. We will plot the data into a time series graph now.
        GraphUtils.plot_time_series(x_time_array, y_values, "Date", "Revenue", ["FAN", "Admob", "Total"], "$",
                                    "Network", "Pi Music Player Ads Revenue")
    else:
        print("Bad Response. Code :" + str(fan_res.status_code))

# This code is used to get the FAN APP ID and FAN ACCESS TOKEN from the command line arguments
if len(sys.argv) == 3:

    fan_app_id = sys.argv[1]
    fan_access_token = sys.argv[2]

    get_and_plot_ads_revenue_data(fan_app_id, fan_access_token, 1496477331, int(time.time()))
else:
    print("Invalid Command Line Arguments.\nThe arguments should be : <FAN_APP_ID> <FAN_ACCESS_TOKEN>")
