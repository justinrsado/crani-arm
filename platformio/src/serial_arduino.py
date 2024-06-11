from serial import Serial
import time
from threading import Lock

class Serial_Arduino:
    def __init__(self):
        self.threshold = 2500
        self.on = False
        self.arduino = Serial(port='/dev/cu.usbmodem14101', baudrate=9600, timeout=.1)
        # self.arduino = Serial(port='/dev/tty.usbserial-1410', baudrate=9600, timeout=.1)
        # self.arduino = Serial(port='COM3', baudrate=9600, timeout=None)
        self.on_lock = Lock()

    def read_loop_begin(self):
        while True:
            try:
                value = self.arduino.readline().decode('utf-8')
                # print("value:" + value)
                if value:
                    float_value = float(value)
                    self.on_lock.acquire()
                    if float_value < self.threshold and self.on == True:
                        # print("changing to false")
                        self.on = False
                    elif float_value >= self.threshold and self.on == False:
                        # print("changing to true")
                        self.on = True
                    self.on_lock.release()
            except (UnicodeDecodeError, ValueError) as err:
                print(err)
            

    def get_on(self):
        return self.on

    def get_on_lock(self):
        return self.on_lock