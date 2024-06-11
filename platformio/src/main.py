from multiprocessing import Process
from serial import Serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy import signal
from scipy.signal import filtfilt
import numpy as np

arduino = Serial(port='COM5', baudrate=9600, timeout=.1)

def read():
    time.sleep(0.001)
    data = arduino.readline()
    return data

sensor_data = []
i = 1
j = 0

# bandpass filter parameters
freq = 1000     # polling every 1 ms
nyq = freq/2
low = 10/nyq
high = 350/nyq

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

def animate(i, xs, ys):
    xs.append(i)
    ys.append(sensor_data[i])

    xs = xs[-20:]
    ys = ys[-20:]

    ax.clear()
    ax.plot(xs, ys)

    plt.subplots_adjust(bottom=0.30)
    plt.title('penis')
    plt.ylabel('sex')

def ani_init():
    ani = FuncAnimation(fig, animate, fargs=(xs, ys), interval=32)
    plt.show()
    plt.hold(True)

def read_serial():
    while True:
        value = read().decode('utf-8')
        if value:
            sensor_data.append(value)
        # if (i < 32):
        #     sensor_data.append(value)
        #     i += 1
        # else:
        #     sensor_data.append(value)
            # ani = FuncAnimation(fig, animate, fargs=(xs, ys), interval=32)
            # plt.show()
            # plt.hold(True)
        #     fig.canvas.draw()
        #     ani.event_source.stop()

        #     print(*sensor_data)

        #     sensor_data = []
        #     i = 1
            # bandpass filter
            # b, a = signal.butter(2, [low, high], 'bandpass', analog='True')
            # filtered_signal = filtfilt(b, a, sensor_data, axis=0)
Process(target=read_serial).start()
Process(target=ani_init).start()