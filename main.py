import sys
import tkinter

import time

import FANHelper
import GoogleApiHelper
import GraphUtils
import TimeUtils
from TKinterDatePicker import Datepicker


def get_and_plot_ads_revenue_data(fan_app_id, fan_access_token, from_time, to_time):
    # Getting the FAN revenue data
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


def get_data_button_click(root_window, start_picker, end_picker):
    # get_and_plot_ads_revenue_data(fan_app_id, fan_access_token, 1496477331, int(time.time()))
    if start_picker.current_date is not None and end_picker.current_date is not None:
        start_epoch = TimeUtils.date_string_to_epoch_int(start_picker.current_text)
        print("Start Date is", start_epoch)
        end_epoch = TimeUtils.date_string_to_epoch_int(end_picker.current_text)
        print("End Date is", end_epoch)
        get_and_plot_ads_revenue_data(fan_app_id, fan_access_token, start_epoch, end_epoch)
        root_window.destroy()


def close_button_click(root_window):
    root_window.destroy()


# This code is used to get the FAN APP ID and FAN ACCESS TOKEN from the command line arguments
if len(sys.argv) == 3:

    fan_app_id = sys.argv[1]
    fan_access_token = sys.argv[2]

    root = tkinter.Tk()

    root.geometry("600x300")

    main = tkinter.Frame(root, pady=15, padx=15)
    main.place(anchor="c", relx=.5, rely=.2)

    tkinter.Label(main, text="Start Date").grid(row=0, column=0, pady=(5, 5))
    tkinter.Label(main, text="End Date").grid(row=0, column=1, pady=(5, 5))

    start_date_picker = Datepicker(main)
    start_date_picker.grid(row=1, column=0, pady=(5, 5))
    end_date_picker = Datepicker(main)
    end_date_picker.grid(row=1, column=1, pady=(5, 5))

    tkinter.Button(main, text="GET DATA",
                   command=lambda: get_data_button_click(root, start_date_picker, end_date_picker)).grid(row=2,
                                                                                                         column=0,
                                                                                                         pady=(5, 5))
    tkinter.Button(main, text="CLOSE", command=lambda: close_button_click(root)).grid(row=2, column=1, pady=(5, 5))

    root.mainloop()

    # get_and_plot_ads_revenue_data(fan_app_id, fan_access_token, 1496477331, int(time.time()))
else:
    print("Invalid Command Line Arguments.\nThe arguments should be : <FAN_APP_ID> <FAN_ACCESS_TOKEN>")
