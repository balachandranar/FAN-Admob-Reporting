import FAN_Abs
import TimeUtils
import GraphUtils
import time
import sys

if len(sys.argv) == 3:

    fan_app_id = sys.argv[1]
    fan_access_token = sys.argv[2]

    fan_res = FAN_Abs.fan_api_request(fan_app_id, fan_access_token, 1496793600, int(time.time()))

    if fan_res.status_code == 200:
        data = fan_res.json()['data']
        y_values = []
        x_timeArray = []
        for datum in data:
            x_timeArray.append(TimeUtils.fb_report_date_to_datetime(datum['time']))
            y_values.append(float(datum['value']))

        GraphUtils.plot_time_series(x_timeArray, y_values, "Revenue","$")
    else:
        print("Bad Response. Code :" + str(fan_res.status_code))

else:
    print("Invalid Command Line Arguments.\nThe arguments should be : <FAN_APP_ID> <FAN_ACCESS_TOKEN>")