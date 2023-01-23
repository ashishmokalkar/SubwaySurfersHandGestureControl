from cvzone.HandTrackingModule import HandDetector
import cv2
import numpy as np
import pyautogui

cap = cv2.VideoCapture(0)
cap_gif = cv2.VideoCapture("./Resources/egif_start_1.gif")

cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)

points_left = np.array([[0, 0], [450, 220], [450, 500], [0, 720]])
points_top = np.array([[0, 0], [450, 220], [830, 220], [1280, 0]])
points_right = np.array([[1280, 0], [830, 220], [830, 500], [1280, 720]])
points_down = np.array([[1280, 720], [830, 500], [450, 500], [0, 720]])


count = 1
frame_counter = 0
frame_counter_clicked = 0
flag = False

curr = "NULL"

while True:
    # Get image frame

    left_flag = False
    right_flag = False
    top_flag = False
    down_flag = False

    success, img = cap.read()
    img = cv2.flip(img, 1)
    copiedImage = img.copy()
    another_copiedImage = copiedImage.copy()
    copiedImage = cv2.rectangle(copiedImage, (450, 220), (830, 500), (102, 0, 204), 3)
    copiedImage = cv2.line(copiedImage, (0, 0), (450, 220), (102, 0, 204), 3)
    copiedImage = cv2.line(copiedImage, (830, 220), (1280, 0), (102, 0, 204), 3)
    copiedImage = cv2.line(copiedImage, (0, 720), (450, 500), (102, 0, 204), 3)
    copiedImage = cv2.line(copiedImage, (830, 500), (1280, 720), (102, 0, 204), 3)
    img = cv2.putText(img, 'Subway surfers using Hand Gesture Control ', (180, 70), cv2.FONT_HERSHEY_TRIPLEX ,
                        1.3, (102, 0, 204), 3, cv2.LINE_AA)

    ret, gif_image = cap_gif.read()
    frame_counter += 1
    frame_counter_clicked += 1

    if frame_counter == cap_gif.get(cv2.CAP_PROP_FRAME_COUNT):
        frame_counter = 0  # Or whatever as long as it is the same as next line
        cap_gif.set(cv2.CAP_PROP_POS_FRAMES, 0)

    gif_image = cv2.resize(gif_image, (400, 150), interpolation=cv2.INTER_AREA)

    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    hands2, copiedImage = detector.findHands(copiedImage)  # with draw

    if hands and hands2:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        fingers1 = detector.fingersUp(hand1)
        if fingers1 == [1, 1, 1, 0, 0]:
            if lmList1[12][0] > 800 and lmList1[12][0] < 1200 and lmList1[12][1] > 150 and lmList1[12][1] < 300 and not flag:
                flag = True
                pyautogui.press('space')
        if fingers1 == [1, 1, 1, 1, 1]:
            if lmList1[9][0] < 450 and lmList1[9][1] > 220 and lmList1[9][1] < 500:
                left_flag = True
            elif lmList1[9][0] > 450 and lmList1[9][1] < 220 and lmList1[9][1] > 00 and lmList1[9][0] < 830:
                top_flag = True
            elif lmList1[9][0] > 830 and lmList1[9][1] < 500 and lmList1[9][1] > 200 and lmList1[9][0] < 1280:
                right_flag = True
            elif lmList1[9][0] > 450 and lmList1[9][1] > 500 and lmList1[9][1] < 720 and lmList1[9][0] < 830:
                down_flag = True
    # # Display
    if not flag:
        img[150:300, 200:600] = gif_image
        cv2.imshow("Image", img)
    else:
        if left_flag:
            cv2.fillPoly(copiedImage, pts=[points_left], color=(23, 192, 243))
            copiedImage = cv2.addWeighted(copiedImage, 0.7, another_copiedImage, 0.3, 0)
            if curr != "left":
                pyautogui.press("left")
                curr = "left"
                print("Left clicked")

        elif right_flag:
            cv2.fillPoly(copiedImage, pts=[points_right], color=(23, 192, 243))
            copiedImage = cv2.addWeighted(copiedImage, 0.7, another_copiedImage, 0.3, 0)
            if curr != "right":
                pyautogui.press("right")
                curr = "right"
                print("Right clicked")
            # pyautogui.press("right")
        elif top_flag:
            cv2.fillPoly(copiedImage, pts=[points_top], color=(23, 192, 243))
            copiedImage = cv2.addWeighted(copiedImage, 0.7, another_copiedImage, 0.3, 0)
            if curr != "top":
                pyautogui.press("up")
                curr = "top"
                print("Up clicked")
            # pyautogui.press("up")
        elif down_flag:

            cv2.fillPoly(copiedImage, pts=[points_down], color=(23, 192, 243))
            copiedImage = cv2.addWeighted(copiedImage, 0.7, another_copiedImage, 0.3, 0)
            if curr != "down":
                pyautogui.press("down")
                curr = "down"
                print("Down clicked")
        else:
            curr = "NULL"
        image = cv2.putText(copiedImage, 'Up', (630, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (102, 0, 204), 2, cv2.LINE_AA)
        image = cv2.putText(copiedImage, 'Left', (10, 350), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (102, 0, 204), 2, cv2.LINE_AA)
        image = cv2.putText(copiedImage, 'Right', (1190, 330), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (102, 0, 204), 2, cv2.LINE_AA)
        image = cv2.putText(copiedImage, 'Down', (630, 700), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (102, 0, 204), 2, cv2.LINE_AA)
        cv2.imshow("Image", copiedImage)
    cv2.waitKey(1)
cap.release()
cap_gif.release()
cv2.destroyAllWindows()
