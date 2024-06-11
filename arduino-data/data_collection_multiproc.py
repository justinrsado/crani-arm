from multiprocessing import Process, Pipe
from tokenize import Double
from serial import Serial
from itertools import count
import time
import csv
import json
import keyboard
import subprocess

def proc1(conn):
    end = 0
    py_start_time = time.time()
    arduino = Serial(port='/dev/tty.usbmodem14101', baudrate=28800, timeout=.1)
    while True:
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
        if len(voltage1_data) >= 1024:
            data = {
                "basetime": base_time,
                "voltage1": voltage1_data,
                "voltage2": voltage2_data,
                "voltage3": voltage3_data
            }
            conn.send(data)
            base_time, voltage1_data, voltage2_data, voltage3_data = [], [], [], []


if __name__ == '__main__':
    cmd = [
        "python ../hand-tracking-data/HandTrackingStart.py " + str(TIMER)
    ]
    subprocess.Popen(cmd, shell=True,
                     stdin=None, stdout=None, stderr=None)
    fields = ["time", "voltage1", "voltage2", "voltage3"]
    parent_conn, child_conn = Pipe()
    p = Process(target=proc1, args=(child_conn,))
    p.start()
    while True:
        data = parent_conn.recv()
        with open('json_data.json', 'w') as outfile:
            json.dump(data, outfile)
