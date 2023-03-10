import cv2
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import time
import numpy as np
import screen_brightness_control as sbc
from math import hypot

#variables
buttonPressed = False
buttonDelay = 10
buttonCount = 0
gestureThreshold = 500
width, height = 1200, 720
volume = 50


cap = cv2.VideoCapture(0)

#Hand Detection
detector = HandDetector(detectionCon=0.8, maxHands=1)

#Mediapipe hands
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    success, frame = cap.read()

    #imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    hands, frame = detector.findHands(frame)
    cv2.line(frame, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']

        if cy <= gestureThreshold:
           if fingers == [1, 0, 0, 0, 0]: #Gesture - left
               pyautogui.press("left")
               buttonPressed = True

           elif fingers == [0, 0, 0, 0, 1]: #Gesture - right
               pyautogui.press("right")
               buttonPressed = True

        if fingers == [1, 1, 1, 1, 1]:
            pyautogui.press("space")
            buttonPressed = True

        if fingers == [0, 1, 0, 0, 1]:
            volume = volume+5
            sbc.set_brightness(volume)

        if fingers == [1, 0, 0, 0, 1]:
            volume = volume-5
            sbc.set_brightness(volume)





    #Button Press Iteration
    if buttonPressed:
        buttonCount += 1
        if buttonCount > buttonDelay:
            buttonCount = 0
            buttonPressed = False



    cv2.imshow("Window", frame)
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break
