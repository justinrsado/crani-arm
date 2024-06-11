from tokenize import Double
from serial import Serial
from itertools import count
import time
import csv
import json
import keyboard
import subprocess


TIMER = 260
cmd = [
    "python ../hand-tracking-data/HandTrackingStart.py " + str(TIMER)
]
subprocess.Popen(cmd, shell=True,
                 stdin=None, stdout=None, stderr=None)

arduino = Serial(port='/dev/tty.usbmodem14101', baudrate=28800, timeout=.1)
fields = ["time", "voltage1", "voltage2", "voltage3"]

# f = open('dataset1.csv', 'w', newline='')
# writer = csv.writer(f)

end = 0
base_time, voltage1_data, voltage2_data, voltage3_data = [], [], [], []
data = {
    "basetime": base_time,
    "voltage1": voltage1_data,
    "voltage2": voltage2_data,
    "voltage3": voltage3_data
}

with open('json_data.json', 'w') as outfile:
    json.dump(data, outfile)
py_start_time = time.time()
while time.time() - py_start_time < TIMER:
    line = arduino.readline().decode("utf-8")[:-2].split()
    if line:
        t = line[0]
        voltage1 = line[1]
        voltage2 = line[2]
        voltage3 = line[3]
        # print(t, voltage1, voltage2)

        base_time.append(py_start_time + float(t))
        voltage1_data.append(voltage1)
        voltage2_data.append(voltage2)
        voltage3_data.append(voltage3)

        # writer.writerow([str(timer), str(voltage1), str(voltage2)])

data = {
    "basetime": base_time,
    "voltage1": voltage1_data,
    "voltage2": voltage2_data,
    "voltage3": voltage3_data
}

with open('json_data.json', 'w') as outfile:
    json.dump(data, outfile)
