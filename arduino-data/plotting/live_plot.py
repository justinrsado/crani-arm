from serial import Serial
from itertools import count
import time
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from matplotlib.animation import FuncAnimation
import pandas as pd

data = pd.read_csv('thumb_motion_1channel.csv', header=None)[0]
window = []
index = count()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

arduino = Serial(port='COM5', baudrate=9600, timeout=.1)

def read():
    data = arduino.readline().decode("utf-8")
    if (data):
        i = next(index)
        return (i, data)
    else:
        return None
    i = next(index)
    return i, data[i]

# bandpass filter parameters
fs = 1000     # polling every 1 ms
low = 10
high = 350

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def animate(i, xs, ys):
    # Read EMG sensor data
    time, emg_voltage = read()
    if (emg_voltage):

        # Add to current window
        xs.append(time)
        window.append(emg_voltage)

        # If window size is reached do preprocessing and add to plot
        if (len(window) == 1024):
            #filtered_window = butter_bandpass_filter(window, low, high, fs)

            # add window to ys list
            for v in window:
                ys.append(v)

            # Limit x and y lists to 2048 items
            xs = xs[-2048:]
            ys = ys[-2048:]

            # Draw x and y lists
            ax.clear()
            ax.plot(xs, ys)

            # Format
            plt.title("EMG Voltage Over Time")
            plt.ylabel("Voltage (mV)")
            plt.xlabel("Time (ms)")

            # Clear window
            window.clear()


ani = FuncAnimation(fig, animate, fargs=(xs, ys), interval=1)
plt.show()