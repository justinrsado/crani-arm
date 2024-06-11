from itertools import count
import wave
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import pandas as pd
import numpy as np
import json
from math import sqrt
import os


def str_to_float(val):
    return float(val)


arr_to_doubles = np.vectorize(str_to_float)

NUM_VOLTAGES = 3

voltages = []

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'data/middle_fo_fist/json_data.json')
print(filename)

with open(filename, 'r') as json_file:
    data = json.load(json_file)
    basetime = arr_to_doubles(np.asarray(data["basetime"]))
    for x in range(NUM_VOLTAGES):
        voltages.append(arr_to_doubles(np.asarray(data["voltage" + str(x+1)])))

# bandpass filter parameters

# polling every 32 ms (fs = 1/32 ms) - NEED TO INCREASE THIS TO AT LEAST 700HZ
fs = 1000
low = 10
high = 350


def butter_bandpass(lowcut, highcut, fs, order=8):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=8):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


# extract windows
n = 128         # window size
s = 32          # shift length

windows_arr = []
for voltage in voltages:
    windows_arr.append([voltage[i:i+n] for i in range(0, len(voltage), s)])
start_time = [basetime[i] for i in range(0, len(basetime), s)]


def normalize(min, max, val):
    return (val - min)/(max - min)


## EXTRACT FEATURES ##
output = {}

windows_index = 0
for voltage in voltages:
    waveform_length = []
    integrated_emg = []
    mean_abs_val = []
    mean_abs_val_slope = []
    simple_square_integral = []
    variance = []
    root_mean_sq = []
    timestamp = []

    windows = windows_arr[windows_index]
    for i in range(0, len(windows_arr[windows_index])):
        # Bandpass filter each segment - uncomment after increasing sampling rate
        window = butter_bandpass_filter(windows[i], low, high, fs)
        # window = windows[i]

        # Do not extract for last few windows with not enough data
        if (len(window) == n):
            timestamp.append(start_time[i])

            wl = 0
            iemg = 0
            ssi = 0

            for j in range(0, len(window)-1):
                wl += abs(window[j+1] - window[j])

                iemg += abs(window[j])

                ssi += abs(window[j])*abs(window[j])

            # Waveform Length
            waveform_length.append(wl)

            # Integrated EMG
            integrated_emg.append(iemg)

            # Mean Absolute Value
            mean_abs_val.append(iemg/len(window))

            # Simple Square Integral
            simple_square_integral.append(ssi)

            # Variance
            variance.append(ssi/(len(window) - 1))

            # Root Mean Square
            root_mean_sq.append(sqrt(ssi/len(window)))

    # Mean Absolute Value Slope
    for j in range(0, len(mean_abs_val)-1):
        mean_abs_val_slope.append(mean_abs_val[j+1] - mean_abs_val[j])

    # Normalize features

    normalize_arr = np.vectorize(normalize)

    min_wl = min(waveform_length)
    max_wl = max(waveform_length)
    waveform_length = normalize_arr(
        min_wl, max_wl, np.asarray(waveform_length))

    min_iemg = min(integrated_emg)
    max_iemg = max(integrated_emg)
    integrated_emg = normalize_arr(
        min_iemg, max_iemg, np.asarray(integrated_emg))

    min_mav = min(mean_abs_val)
    max_mav = max(mean_abs_val)
    mean_abs_val = normalize_arr(
        min_mav, max_mav, np.asarray(mean_abs_val))

    min_mavslope = min(mean_abs_val_slope)
    max_mavslope = max(mean_abs_val_slope)
    mean_abs_val_slope = normalize_arr(
        min_mavslope, max_mavslope, np.asarray(mean_abs_val_slope))

    min_ssi = min(simple_square_integral)
    max_ssi = max(simple_square_integral)
    simple_square_integral = normalize_arr(
        min_ssi, max_ssi, np.asarray(simple_square_integral))

    min_var = min(variance)
    max_var = max(variance)
    variance = normalize_arr(min_var, max_var, np.asarray(variance))

    min_rms = min(root_mean_sq)
    max_rms = max(root_mean_sq)
    root_mean_sq = normalize_arr(
        min_rms, max_rms, np.asarray(root_mean_sq))

    # Plot raw data and extracted features
    fig, axs = plt.subplots(4, 2)
    fig.tight_layout()
    axs[0][0].plot(range(0, len(voltage)), voltage)
    axs[0][0].set_title("Voltage Raw Data")

    axs[0][1].plot(range(0, len(waveform_length)), waveform_length)
    axs[0][1].set_title("Voltage Waveform Length")

    axs[1][0].plot(range(0, len(integrated_emg)), integrated_emg)
    axs[1][0].set_title("Voltage Integrated EMG")

    axs[1][1].plot(range(0, len(mean_abs_val)), mean_abs_val)
    axs[1][1].set_title("Voltage Mean Absolute Value")

    axs[2][0].plot(range(0, len(mean_abs_val_slope)), mean_abs_val_slope)
    axs[2][0].set_title("Voltage Mean Absolute Value Slope")

    axs[2][1].plot(range(0, len(simple_square_integral)),
                   simple_square_integral)
    axs[2][1].set_title("Voltage Simple Square Integral")

    axs[3][0].plot(range(0, len(variance)), variance)
    axs[3][0].set_title("Voltage Variance")

    axs[3][1].plot(range(0, len(root_mean_sq)), root_mean_sq)
    axs[3][1].set_title("Voltage Root Mean Square")

    output["waveform_length" + str(windows_index)] = waveform_length.tolist()
    output["integrated_emg" + str(windows_index)] = integrated_emg.tolist()
    output["mean_abs_val" + str(windows_index)] = mean_abs_val.tolist()
    output["mean_abs_val_slope" +
           str(windows_index)] = mean_abs_val_slope.tolist()
    output["simple_square_integral" +
           str(windows_index)] = simple_square_integral.tolist()
    output["variance" + str(windows_index)] = variance.tolist()
    output["root_mean_sq" + str(windows_index)] = root_mean_sq.tolist()
    output["timestamp"] = timestamp

    output['mean_abs_val_slope' + str(windows_index)].append(0)

    print("waveform_length" + str(windows_index),
          len(output["waveform_length" + str(windows_index)]))
    print("integrated_emg" + str(windows_index),
          len(output["integrated_emg" + str(windows_index)]))
    print("mean_abs_val" + str(windows_index),
          len(output["mean_abs_val" + str(windows_index)]))
    print("mean_abs_val_slope" + str(windows_index),
          len(output["mean_abs_val_slope" + str(windows_index)]))
    print("simple_square_integral" + str(windows_index),
          len(output["simple_square_integral" + str(windows_index)]))
    print("variance" + str(windows_index),
          len(output["variance" + str(windows_index)]))
    print("root_mean_sq" + str(windows_index),
          len(output["root_mean_sq" + str(windows_index)]))
    print("timestamp:", len(output["timestamp"]))

    windows_index += 1


with open("../dataset-creation/data/extracted_features.json", 'w') as jsonfile:
    json.dump(output, jsonfile)

plt.show()