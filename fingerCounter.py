import cv2
import os
import time
import handtrackingmodule as htm
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
# width of cam
cap.set(3, wCam)
cap.set(4, hCam)

# to store the finger through os library
folderPath = "E:\Internship Project\FingerCount"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(f'{folderPath}/{imPath}')
    overlayList.append(image)


print(len(overlayList))

pTime = 0

detector = htm.handDetector(detectionCon=0.85)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)

    if len(lmList) != 0:
        fingers = []
            # it is for thumb
        if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # it is for 4 finger
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        # it shows that how many numbers are 1 in the given list fingers
        totalFingers = fingers.count(1)
        print(totalFingers)
                # print("index finger open")
        # image itself is an matrix
        # to target a specific image is known as slicing
        # 0:200 is height and width
        # img[221:105, 221:105] = overlayList[0]

        # if the size is unknown and all the images size are different then shape
        # method is used which return the value of the height , width and channel
        h, w, c = overlayList[totalFingers-1].shape
        img[0:h, 0:w] = overlayList[totalFingers-1]

        cv2.rectangle(img, (20, 225), (170, 425), (0,255,0))
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN
                    , 10, (255,0 ,0 ), 25)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime


    cv2.putText(img, f'FPS:{int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255,0, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break