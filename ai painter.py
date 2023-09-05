import cv2
import numpy as np
import time
import os
import handtrackingmodule as htm

################################
brushThickness = 15
eraserThickness = 50
##########################
folderPath = "E:\Internship Project\Header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
    # image = cv2.resize(overlayList[imPath], (1280, 217))
print(len(overlayList))
header = overlayList[0]
drawColor = (49, 49, 255)




cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = htm.handDetector(detectionCon=0.5, maxHands=1)

xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
   # steps to perform the

    # find landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # print(lmList)

        #tip of index and middle finger
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # check when which fingers are up
        fingers = detector.fingersup()
        print(fingers)
        # if selection mode - two fingers are up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print("selectin mode")
            # checking for click and chaning the color
            if y1 < 125:
                if 250<x1<450:
                    header = overlayList[0]
                    drawColor = (49, 49, 255)
                elif 550<x1<750:
                    header = overlayList[1]
                    drawColor = (255, 0 ,0)
                elif 800<x1<950:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 1050<x1<1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)


            cv2.rectangle(img, (x1, y1-15),(x2, y2+15), drawColor, cv2.FILLED)



        # if drawing mode - index finger is up
        if fingers[1] and fingers[2]==False:
            cv2.circle(img, (x1, y1), 8, drawColor, cv2.FILLED)
            print("draw mode")
            # the line shouldnt start from zero index
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp),(x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp),(x1, y1), drawColor, brushThickness)
            else:
                cv2.line(img, (xp, yp),(x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp),(x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1



    # two add two img
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    #settting the header image
    img[0:130, 0:1280] = cv2.resize(header, (1280, 130))
    img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
