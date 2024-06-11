# Get file paths
import csv
import os
import json

import numpy as np
import matplotlib.pyplot as plt

cwd = os.getcwd()
data_directory = "data"

camera_data_filename = "camera_data.csv"
arduino_data_filename = "extracted_features.json"

print(cwd)
print(os.path.join(cwd, data_directory, camera_data_filename))

camera_data_path = os.path.join(cwd, data_directory, camera_data_filename)
arduino_data_path = os.path.join(cwd, data_directory, arduino_data_filename)

# Load camera data into memory

camera_data = []
camera_time_data = []
with open(camera_data_path) as camera_file:
    reader = csv.reader(camera_file)
    for row in reader:
        time = float(row[0])
        camera_data.append([time, row[1]])
        camera_time_data.append(time)

# Load arduino data into memory
arduino_file = open(arduino_data_path)
arduino_data = json.load(arduino_file)
print("\nARDUINO DATA CONSISTENCY:")
for label in arduino_data.keys():
    print("\tlength of " + label + ":",  len(arduino_data[label]))

# Add camera data to arduino data
time_label = "timestamp"
camera_index = 0
arduino_index = 0
arduino_time_list = arduino_data[time_label]
hand_labels = []

hit_end = False
incremented = False
print("\nDATASET ALIGNMENT:")
while arduino_index < len(arduino_time_list):
    while (camera_index < len(camera_data)-1) and (camera_data[camera_index][0] < arduino_time_list[arduino_index]):
        camera_index += 1
    if arduino_index == 0:
        print("\tfirst arduino datapoint aligns with camera index", camera_index)
    if camera_index == 1 and not incremented:
        print("\tfirst camera index increased at arduino index", arduino_index)
        incremented = True
    if (camera_index == len(camera_data) - 1) and (not hit_end):
        hit_end = True
        print("\tlast camera index came at arduino index", arduino_index)

    hand_labels.append(camera_data[camera_index][1])
    arduino_index += 1
print("\tlast arduino datapoint aligns with camera index", camera_index)

print("\nDATASET LENGTH:")
print("\tlength of arduino data:", len(arduino_time_list))
print("\tlength of camera data:", len(camera_data))

# Ouput data
arduino_data["label"] = hand_labels
output_path = "output"
output_file = "dataset.json"

with open(os.path.join(cwd, output_path, output_file), 'w') as outfile:
    json.dump(arduino_data, outfile)

# Data validation
print("\nCAMERA DATAPOINT TIME DIFFERENCE CONSISTENCY")
camera_time_arr = np.array(camera_time_data)
camera_time_diff = np.diff(camera_time_arr)
max = np.amax(camera_time_diff)
min = np.amin(camera_time_diff)
avg = np.average(camera_time_diff)
std = np.std(camera_time_diff)
print("max:", round(max, 4))
print("min:", round(min, 4))
print("avg:", round(avg, 4))
print("std:", round(std, 4))

plt.hist(camera_time_diff)
plt.title("Histogram of sampling frequency for camera")
plt.xlabel("Time between datapoints (ms)")
plt.ylabel("Frequency")

