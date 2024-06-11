import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import subprocess
import os
import json
import queue
import threading
import csv

GESTURES = {'zero': [True, None, None, None, None],
            'one': [None, True, None, None, None],
            'two': [None, None, True, None, None],
            'three': [None, None, None, True, None],
            'four': [None, None, None, None, True],
            'fight_on': [True, True, None, None, True],
            'flip_the_bird': [True, True, None, True, True],
            'shaka': [None, True, True, True, None],
            'wooo': [None, True, True, None, None],
            'fist': [True, True, True, True, True]}
"""
ELECTRICAL TEAM PLZ READ:

how to start this:
    x = threading.Thread(target=GestureTracking.GestureTrack)
    x.start()

how to join thread:
    GestureTracking.stopThreads()
    x.join()

ehh just work off of sample_main.py but if you don't see that first here's 
"""

DATAPOINTS_PER_SECOND = 10
DEBUG_MODE = False

previousTime = 0
currentTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()
# finger indices from 0 to 4: pinkie, index, middle, pointer, thumb
isClosed = [False, False, False, False, False]
isFist = False
file_name = os.path.abspath("camera_data.csv")
events = []

keepGoing = True
keepWritingFiles = True

# create threadsafe queue with maxsize of 10 seconds worth of data
toWriteQueue = queue.Queue(maxsize=DATAPOINTS_PER_SECOND * 10)
fields = ["time", "gesture"]


def GestureTrack():
    global keepGoing, keepWritingFiles, toWriteQueue
    x = threading.Thread(target=fileWriteLoop)
    x.start()

    pastTime = time.time()
    while keepGoing:
        fastEnough = False
        currTime = time.time()

        while (currTime - pastTime) < (1/DATAPOINTS_PER_SECOND):
            currTime = time.time()
            fastEnough = True

        if not fastEnough:
            print(f"Need to reduce frames per second: time = {currTime}")

        pastTime = currTime

        success, img = cap.read()
        img = detector.findHands(img)
        landmarkList = detector.findPosition(img)

        gesture = "undetermined"
        # detect which fingers are closed
        closed = detector.detect_closed_fingers(img)
        print(closed)

        for gesture_lib, closed_lib in GESTURES.items():
            if closed == closed_lib:
                gesture = gesture_lib

        dict = {
            "time": currTime,
            "gesture": gesture
        }
        print(dict)

        # TODO: fill in thumb/index/middle/ring/pinky angles here
        toWriteQueue.put(dict)
        if DEBUG_MODE:
            fps = 1 / (currTime - pastTime)

            cv2.putText(img, str(int(fps)), (10, 70),
                        cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

            cv2.imshow("Image", img)
            if cv2.waitKey(1) == 32:
                break

    keepWritingFiles = False
    x.join()


def bool_to_int(b):
    if b:
        return 1
    else:
        return 0


def fileWriteLoop():
    global keepGoing, keepWritingFiles, toWriteQueue
    print("starting file write loop")
    if os.path.exists(file_name):
        os.remove(file_name)
    else:
        print("GestureTracking.fileWriteLoop: file doesn't exist")
    # https://stackoverflow.com/questions/2363731/append-new-row-to-old-csv-file-python

    with open(file_name, "a", newline='') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=fields)
        while keepWritingFiles or (not toWriteQueue.empty()):
            m = toWriteQueue.get(block=True, timeout=10)
            writer.writerow(m)

    print("ending file write loop")


def stopThreads():
    global keepGoing
    keepGoing = False


# Legacy Code Block: archived 2/25/2022
"""
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    landmarkList = detector.findPosition(img)

    # fist = detector.detect_hand_closed(img)
    # if isFist != fist:
    #     if fist:
    #         print("Closed Hand")
    #         # write line to file with bash command
    #         subprocess.run("echo 'time: {0}, hand closed' >> {1}".format(currentTime, file_name), shell=True)
    #     else:
    #         print("Opened Hand")
    #         # write line to file with bash command
    #         print("write to file: echo 'time: {0}, hand opened' >> {1}".format(currentTime, file_name))
    #
    # isFist = fist

    # detect which fingers are closed
    closed = detector.detect_closed_fingers(img)

    # detect which fingers have changed from previous logged value
    changed_fingers = []
    for i in range(5):
        if isClosed[i] == closed[i]:
            changed_fingers.append(False)
        else:
            changed_fingers.append(True)

    # for each finger that is changed
    for i in range(len(changed_fingers)):
        if changed_fingers[i]:

            # store change as dictionary (current time, finger that changed, whether open or closed)
            p = {"time": currentTime, "finger": i,
                 "change": bool_to_int(closed[i])}
            # add dictionary to overall list of events
            events.append(p)

            # update isCLosed variable
            isClosed[i] = closed[i]
"""

# Legacy Code Block: archived 3/25/2022
"""
dict = {
            "time": currTime,
            "thumbAng": -361,
            "indexAng": -361,
            "middleAng": -361,
            "ringAng": -361,
            "pinkyAng": -361       
        }
"""
