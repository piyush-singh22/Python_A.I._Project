import cv2
import time
import numpy as np
import handtrackingmodule as htm
# to calculate the length
import math
# todirect change the volume of system this are from library pycaw
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
##################################
wCam, hCam = 640, 480
##################################



cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.9)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist)!=0:
        # to get a value particular handmark
        # print(lmlist[4], lmlist[8])
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2


        # this is to color the choosd landmark circle
        cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (255, 0, 255), cv2.FILLED)
        # to draw a linre between the landmark 4 and 8
        cv2.line(img, (x1, y1), (x2, y2), (255,0,0), 3)
        # now to add the circle between the given line:
        cv2.circle(img, (cx, cy), 8, (255,0,255), cv2.FILLED)
        # to calculate the distance between the two fingers and adjust volume on it
        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)




        # we have the hand range 25 - 145 and volume range is -65 - 0
        # now to change the hand range into volume we will use numpy
        vol = np.interp(length,[20,110],[minVol, maxVol])
        volBar = np.interp(length, [20,110], [400, 110])
        volPer = np.interp(length, [20, 110], [0, 100])
        print(int(length), " ||||| ", vol)
        # below is the methods of pycaw to set the volume
        volume.SetMasterVolumeLevel(vol, None)

        if length < 15:
            cv2.circle(img, (cx, cy), 8, (0,255,0), cv2.FILLED)

    # the range or representation in rectangle format
    cv2.rectangle(img,(20,110), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (20, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    # to put text below the volume bar
    cv2.putText(img, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX
                , 1, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    # cv2.putText(img, f'FPS:{int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX
    #             , 1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break