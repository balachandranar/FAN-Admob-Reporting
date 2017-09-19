import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import pandas as pd


def plot_time_series(x_date_obj_array, y_values, x_label, y_label, y_value_categories, y_values_prefix="",
                     y_values_category="", window_title="", date_format='%d %b %Y'):
    for i, _ in enumerate(x_date_obj_array):
        x_date_obj_array[i] = mdates.date2num(x_date_obj_array[i])

    fig, ax = plt.subplots()

    dfs = []

    for index, value in enumerate(y_values):
        df = pd.DataFrame({
            x_label: x_date_obj_array,
            y_values_category: y_value_categories[index],
            y_label: value})
        dfs.append(df)

    final_df = pd.concat(dfs, axis=0)

    final_df['unit'] = 'subject'

    ax = sns.tsplot(data=final_df, time=x_label, value=y_label, unit="unit", condition=y_values_category)
    # assign locator and formatter for the xaxis ticks.
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))

    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter(y_values_prefix + '%d'))

    # put the labels at 45deg since they tend to be too long
    fig.autofmt_xdate()
    fig.canvas.set_window_title(window_title)
    plt.show()
