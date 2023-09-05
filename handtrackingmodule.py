
import mediapipe as mp
import cv2
import time
class handDetector():
    def __init__(self, mode=False, maxHands = 2,  modelComplexity = 1, detectionCon = 0.5, trackCon = 0.5  ):
        self.mode = mode
        self.maxHands = maxHands
        self.modelcomplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        # self.cap = cv2.VideoCapture(0)
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,   self.modelcomplexity, self.detectionCon, self.trackCon)
        # print(self.hands)
        # to detect all the point drawn on the hand throw mediapipe like it has 21 point
        self.mpDraw = mp.solutions.drawing_utils

        self.tipIds = [4, 8, 12, 16, 20]
    def findHands(self, img, draw=True):
        # it is us to convert the image into rgb image as this library
        # can only understand rgb image.
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # process hands for us as it has the method process in it
        self.results = self.hands.process(imgRGB)
        # multi_hand_landmark thus methd is used to see that weather the hand is detected
        # or not.
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                # mpHands.HAND_CONNECTIONS IT IS USED TO SHOW THE CONNECTION BETWEEN ALL
                # HAND LANDMARKS
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True ):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, ln in enumerate(myHand.landmark):
                # prin t(id, ln)
                h, w, c = img.shape
                # it is used for landmarkes on the hand
                cx, cy = int(ln.x * w), int(ln.y * h)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 15, 255), cv2.FILLED)
        return self.lmList

    def fingersup(self):
        fingers = []
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)


        for id in range (1,5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers


def main():
    # it is for frame rate
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    #  object
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
        # it is for calculating the frame rate.
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'str{int(fps)}', (18, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
if __name__ == "__main__":
    # here there will be the dummy part that show what can it do
    main()
