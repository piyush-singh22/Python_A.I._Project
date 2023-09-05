import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
# to detect all the point drawn on the hand throw mediapipe like it has 21 point
mpDraw = mp.solutions.drawing_utils


# it is for frame rate
pTime = 0
cTime = 0
while True:
    Success, img = cap.read()

    # it is us to convert the image into rgb image as this library
    # can only understand rgb image.
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # process hands for us as it has the method process in it
    results = hands.process(imgRGB)

    # multi_hand_landmark thus methd is used to see that weather the hand is detected
    # or not.
    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:

            for id, ln in enumerate(handLms.landmark):
                # print(id, ln)
                h, w, c = img.shape
                # it is used for landmarkes on the hand
                cx, cy = int(ln.x*w), int(ln.y*h)
                print(id, cx, cy)
                # now it will only go for 5 to 20 landmarkes on the hand
                if id <= 20 and id >= 5 :
                    cv2.circle(img, (cx, cy), 10, (255, 15, 255), cv2.FILLED)



            # mpHands.HAND_CONNECTIONS IT IS USED TO SHOW THE CONNECTION BETWEEN ALL
            # HAND LANDMARKS
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)







    cTime = time.time()
    fps = 1/(cTime-pTime)
    # pTime = cTime

    # cv2.putText(img, f'str(int(fps))', (18,70), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 255), 3 )
    cv2.imshow("Image", img)
     if cv2.waitKey(1) & 0xFF == ord("q"):
            break



