# for image processing
import time
import mediapipe as mp
import cv2

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
# for pose estimation
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("E:\Internship Project\She was shocked!.mp4")
pTime = 0
while (True):
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS) # here the POSE_CONNECTIONS is for darwing the connection line between all the landmarks
        for id, lm in enumerate(results.pose_landmarks.landmark ):
            h , w, c = img.shape
            print(id, lm)
            cx, cy = int(lm.x * w), int( lm.y*h)
            cv2.circle(img, (cx, cy), 10, (255,0,0), cv2.FILLED)
    # Frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 8 , 9), 3)
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break