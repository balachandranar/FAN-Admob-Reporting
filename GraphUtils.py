import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker


def plot_time_series(x_date_obj_array, y_values, y_label):
    fig, ax = plt.subplots()
    ax = sns.tsplot(data=y_values, time=x_date_obj_array, value=y_label, ax=ax)

    # assign locator and formatter for the xaxis ticks.
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %Y'))

    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('$%d'))

    # put the labels at 45deg since they tend to be too long
    fig.autofmt_xdate()
    plt.show()
