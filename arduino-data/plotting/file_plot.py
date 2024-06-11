import matplotlib.pyplot as plt
import csv
import json


def plot_two_lines(x, y1, y2, y3, label1="line1", label2="line2", label3="line3"):
    ax = plt.axes()

    ax.plot(x, y1, 'bo', linestyle="-", label=label1, markersize=0.1, lw=0.5)
    ax.plot(x, y2, 'go', linestyle="-", label=label2,  markersize=0.1, lw=0.5)
    ax.plot(x, y3, 'ro', linestyle="-", label=label3,  markersize=0.1, lw=0.5)

    ax.yaxis.set_major_locator(plt.MaxNLocator(5))
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))

    plt.legend()
    plt.show()

# open file
with open('../json_data.json') as f:
    data = json.load(f)

# extract time data and make relative time start from 0
time = data['basetime']
time = [(float(x) - float(time[0])) for x in time]

# extract other time series data
voltage1 = data['voltage1']
voltage2 = data['voltage2']
voltage3 = data['voltage3']

plot_two_lines(time, voltage1, voltage2, voltage3, "voltage1", "voltage2", "voltage3")

