import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionConfid=0.5, trackConfid=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConfid = detectionConfid
        self.trackConfid = trackConfid

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands, min_detection_confidence=self.detectionConfid, min_tracking_confidence=self.trackConfid)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLandmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLandmarks, self.mpHands.HAND_CONNECTIONS)
        return img

    def detect_hand_closed(self, img):
        if self.detect_pinkie_closed(img) and self.detect_index_closed(img) and \
                self.detect_middle_closed(img) and self.detect_pointer_closed(img) and self.detect_thumb_closed(img):
            # print("Hand is closed")
            return True
        else:
            return False

    def detect_closed_fingers(self, img):
        # finger indices from 0 to 4: pinkie, index, middle, pointer, thumb
        return [self.detect_pinkie_closed(img), self.detect_index_closed(img), self.detect_middle_closed(img),
                self.detect_pointer_closed(img), self.detect_thumb_closed(img)]

    def detect_finger_closed(self, img, outer_index, inner_index, check_y=True):
        """detect if finger is closed given the outer and inner index of landmark. If check_y is true, we
        evaluate using y position of the landmarks. Otherwise, we use x position """

        ind = 2 if check_y else 1
        landmarkList = self.findPosition(img)
        if len(landmarkList) != 0:
            if landmarkList[outer_index][ind] > landmarkList[inner_index][ind]:
                return True

    def detect_pinkie_closed(self, img):
        return self.detect_finger_closed(img, 20, 17, True)

    def detect_index_closed(self, img):
        return self.detect_finger_closed(img, 16, 13, True)

    def detect_middle_closed(self, img):
        return self.detect_finger_closed(img, 12, 9, True)

    def detect_pointer_closed(self, img):
        return self.detect_finger_closed(img, 8, 5, True)

    def detect_thumb_closed(self, img):
        # detect which hand and then assess if tip of thumb is past x coord of pointer
        # current method works when hand is both facing camera and not facing camera
        if self.detect_finger_closed(img, 5, 17, False):
            return self.detect_finger_closed(img, 5, 4, False)
        else:
            return self.detect_finger_closed(img, 4, 5, False)

    def findPosition(self, img, handNum=0, draw=True):
        landmarkList = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNum]
            for id, landmark in enumerate(hand.landmark):
                # print(id, landmark)
                height, width, channels = img.shape
                cx, cy = int(landmark.x * width), int(landmark.y * height)
                # print(id, cx, cy)
                landmarkList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        return landmarkList

def main():
    previousTime = 0
    currentTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        landmarkList = detector.findPosition(img)
        if len(landmarkList) != 0:
            print(landmarkList[4])
        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        #THUMB DETECTION
        if detector.detect_thumb_closed(img):
            cv2.putText(img, "thumb closed", (10, 120), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        else:
            cv2.putText(img, "", (10, 120), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        #POINTER DETECTION
        if detector.detect_pointer_closed(img):
            cv2.putText(img, "pointer closed", (10, 170), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        else:
            cv2.putText(img, "", (10, 170), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        #MIDDLE DETECTION
        if detector.detect_middle_closed(img):
            cv2.putText(img, "middle closed", (10, 220), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        else:
            cv2.putText(img, "", (10, 2200), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        #INDEX DETECTION
        if detector.detect_index_closed(img):
            cv2.putText(img, "index closed", (10, 270), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        else:
            cv2.putText(img, "", (10, 270), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        #PINKIE DETECTION
        if detector.detect_pinkie_closed(img):
            cv2.putText(img, "pinkie closed", (10, 320), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        else:
            cv2.putText(img, "", (10, 320), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()