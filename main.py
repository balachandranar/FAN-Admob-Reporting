import csv
import sys
import tkinter

import FANHelper
import GoogleApiHelper
import GraphUtils
import TimeUtils
from TKinterDatePicker import Datepicker


def get_and_plot_ads_revenue_data(fan_id, fan_token, from_time, to_time):
    revenue_data = get_fan_and_admob_revenue_data(fan_id, fan_token, from_time, to_time)

    # we got all the necessary data. We will plot the data into a time series graph now.
    GraphUtils.plot_time_series(revenue_data[0], revenue_data[1:4], "Date", "Revenue", ["FAN", "Admob", "Total"], "$",
                                "Network", "Pi Music Player Ads Revenue")


def get_fan_and_admob_revenue_data(fan_id, fan_token, from_time, to_time):
    # Getting the FAN revenue data
    fan_res = FANHelper.fan_api_request(fan_id, fan_token, from_time, to_time)

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

        return [x_time_array, fan_y_values, admob_values, total_y_values]

    else:
        print("Bad Response. Code :" + str(fan_res.status_code))


def get_ads_revenue_data_and_show_table(fan_id, fan_token, from_time, to_time):
    revenue_data = get_fan_and_admob_revenue_data(fan_id, fan_token, from_time, to_time)
    to_csv_data = [["DATE", "FAN", "ADMOB", "TOTAL"]]
    fan_sum = 0
    admob_sum = 0
    total_sum = 0
    for i, _ in enumerate(revenue_data[0]):
        to_csv_data.append(
            [TimeUtils.datetime_to_date_string(revenue_data[0][i]), round(revenue_data[1][i], 2), round(revenue_data[2][i], 2),
             round(revenue_data[3][i], 2)])
        fan_sum += revenue_data[1][i]
        admob_sum += revenue_data[2][i]
        total_sum += revenue_data[3][i]
    to_csv_data.append(["SUM", round(fan_sum,2), round(admob_sum,2), round(total_sum,2)])
    with open('rev_from_'+TimeUtils.epoch_to_date(from_time)+'_to_'+TimeUtils.epoch_to_date(to_time)+'.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(to_csv_data)
        f.close()


def show_graph_button_click(start_picker, end_picker):
    # get_and_plot_ads_revenue_data(fan_app_id, fan_access_token, 1496477331, int(time.time()))
    if start_picker.current_date is not None and end_picker.current_date is not None:
        start_epoch = TimeUtils.date_string_to_epoch_int(start_picker.current_text)
        end_epoch = TimeUtils.date_string_to_epoch_int(end_picker.current_text)
        get_and_plot_ads_revenue_data(fan_app_id, fan_access_token, start_epoch, end_epoch)


def show_table_button_click(start_picker, end_picker):
    # get_and_plot_ads_revenue_data(fan_app_id, fan_access_token, 1496477331, int(time.time()))
    if start_picker.current_date is not None and end_picker.current_date is not None:
        start_epoch = TimeUtils.date_string_to_epoch_int(start_picker.current_text)
        end_epoch = TimeUtils.date_string_to_epoch_int(end_picker.current_text)
        get_ads_revenue_data_and_show_table(fan_app_id, fan_access_token, start_epoch, end_epoch)


def close_button_click(root_window):
    root_window.destroy()


# This code is used to get the FAN APP ID and FAN ACCESS TOKEN from the command line arguments
if len(sys.argv) == 3:

    fan_app_id = sys.argv[1]
    fan_access_token = sys.argv[2]

    root = tkinter.Tk()

    root.geometry("600x350")

    main = tkinter.Frame(root, pady=15, padx=15)
    main.place(anchor="c", relx=.5, rely=.2)

    tkinter.Label(main, text="Start Date").grid(row=0, column=0, pady=(5, 5))
    tkinter.Label(main, text="End Date").grid(row=0, column=1, pady=(5, 5))

    start_date_picker = Datepicker(main)
    start_date_picker.grid(row=1, column=0, pady=(5, 5))
    end_date_picker = Datepicker(main)
    end_date_picker.grid(row=1, column=1, pady=(5, 5))

    tkinter.Button(main, text="SHOW GRAPH",
                   command=lambda: show_graph_button_click(start_date_picker, end_date_picker)).grid(row=2,
                                                                                                     column=0,
                                                                                                     pady=(5, 5))

    tkinter.Button(main, text="TABLE",
                   command=lambda: show_table_button_click(start_date_picker, end_date_picker)).grid(row=2,
                                                                                                     column=1,
                                                                                                     pady=(5, 5))
    tkinter.Button(main, text="CLOSE", command=lambda: close_button_click(root)).grid(row=3, column=1, pady=(5, 5))

    root.mainloop()

    # get_and_plot_ads_revenue_data(fan_app_id, fan_access_token, 1496477331, int(time.time()))
else:
    print("Invalid Command Line Arguments.\nThe arguments should be : <FAN_APP_ID> <FAN_ACCESS_TOKEN>")
