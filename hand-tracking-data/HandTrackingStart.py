import GestureTracking
import threading
import time
import sys

# TODO priority low: pass in stuff as constants from here

timer = int(sys.argv[1])

time_start = time.time()

# start GestureTrack thread
x = threading.Thread(target=GestureTracking.GestureTrack)
x.start()

count = 0

while time.time()-time_start < timer:
    count += 1
    # print("delay loop count: ", count)
    time.sleep(1)

# print("exited delay loop")

# stop thread
GestureTracking.stopThreads()
x.join()
