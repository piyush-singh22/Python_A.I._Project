import cv2
import numpy as np
import time
import posestimationmodule as pm
cap = cv2.VideoCapture(0)

detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0

while True:
    success, img = cap.read()
    # img = cv2.imread("workout.mp4")
    # for resize the img
    img = cv2.resize(img, (1280, 720))
    img = detector.findPose(img)
    lmList = detector.findPosition(img, False)
    # print(lmList)

    if len(lmList) != 0:
        # #right arm
        # detector.findAngle(img, 12, 14, 16)
        # left arm
        angle = detector.findAngle(img, 11, 13, 15)
        per = np.interp(angle,(220, 330), (0,110))
        bar = np.interp(angle,(220,310),(400, 110))
        # print(angle,per)

        # check for the dumbell curls
        color = (255, 0 ,255)
        if per == 110:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0

        print(int(count))
        # for bar
        cv2.rectangle(img, (20,110), (85, 400), color, 3)
        cv2.rectangle(img, (20,int(bar)), (85, 400),color, cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (150,270), cv2.FONT_HERSHEY_PLAIN,6
                    ,color, 2)


        # show the count
        cv2.rectangle(img, (0,450), (250, 720), (0,255,0), cv2.FILLED)
        cv2.putText(img, f'{int(count)}', (45,670), cv2.FONT_HERSHEY_PLAIN,15
                    ,(255, 0, 0), 5)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break