import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import subprocess
import os
import json

previousTime = 0
currentTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()
# finger indices from 0 to 4: pinkie, index, middle, pointer, thumb
isClosed = [False, False, False, False, False]
isFist = False
file_name = os.path.abspath("hand_open_closed.json")
events = []

def bool_to_int(b):
    if b:
        return 1
    else:
        return 0

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
            p = {"time": currentTime, "finger": i, "change": bool_to_int(closed[i])}
            # add dictionary to overall list of events
            events.append(p)

            # update isCLosed variable
            isClosed[i] = closed[i]

    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) == 32:
        break

#
# # printing dictionaries to json file
# dict_json = {"events": events}
# with open(file_name, "w") as out_file:
#     json.dump(dict_json, out_file, indent=4)