import cv2
import mediapipe as mp
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
wCam, hCam = 1840, 1680
# width of cam
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=1
) as hands:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                thumb = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

                thumb_x, thumb_y = int(thumb.x * frame.shape[1]), int(thumb.y * frame.shape[0])
                index_x, index_y = int(index.x * frame.shape[1]), int(index.y * frame.shape[0])
                middle_x, middle_y = int(middle.x * frame.shape[1]), int(middle.y * frame.shape[0])

                if index_y < middle_y:  # Two fingers
                    pyautogui.moveTo(thumb_x, thumb_y)
                else:  # One finger
                    pyautogui.click()

                mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Mouse Control", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
