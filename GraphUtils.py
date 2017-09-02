import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker


def plot_time_series(x_date_obj_array, y_values, y_label, y_values_prefix, date_format='%d %b %Y'):
    for i,_ in enumerate(x_date_obj_array):
        x_date_obj_array[i] = mdates.date2num(x_date_obj_array[i])

    fig, ax = plt.subplots()
    ax = sns.tsplot(data=y_values, time=x_date_obj_array, value=y_label, ax=ax)
    # assign locator and formatter for the xaxis ticks.
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))

    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter(y_values_prefix+'%d'))

    # put the labels at 45deg since they tend to be too long
    fig.autofmt_xdate()
    fig.canvas.set_window_title('Pi-FAN-Report')
    plt.show()
