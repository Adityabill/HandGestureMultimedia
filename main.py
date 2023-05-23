import cv2
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import time
import numpy as np
import screen_brightness_control as sbc
from math import hypot
import alsaaudio

pyautogui.FAILSAFE = False

setVolume = alsaaudio.Mixer()


#variables
buttonPressed = False
buttonDelay = 10
buttonCount = 0
gestureThreshold = 500
width, height = 1200, 720 
brightness = 50
volume_level = 50


cap = cv2.VideoCapture(0)

#Hand Detection
detector = HandDetector(detectionCon=0.8, maxHands=1)
hand_detector = mp.solutions.hands.Hands()

#Mediapipe hands
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

#Drawing Utils
drawing_utils = mp.solutions.drawing_utils

screenHeight, screenWidth = pyautogui.size()
index_y = 0

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgbFrame)

    #imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    hands, frame = detector.findHands(frame)
    cv2.line(frame, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    windowHeight, windowWidth, _ = frame.shape

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']

        if cy <= gestureThreshold: #Multimedia and Presentation Control(next and previous)
           if fingers == [1, 0, 0, 0, 0]: #Gesture - left
               pyautogui.press("left")
               buttonPressed = True

           elif fingers == [0, 0, 0, 0, 1]: #Gesture - right
               pyautogui.press("right")
               buttonPressed = True

        if fingers == [1, 1, 1, 1, 1]: #Stop and Play
            pyautogui.press("space")
            buttonPressed = True

        if fingers == [0, 1, 0, 0, 1]: #Brightness Increase
            brightness = brightness+5
            sbc.set_brightness(brightness)

        if fingers == [1, 0, 0, 0, 1]: #Brightness Decrease
            brightness = brightness-5
            sbc.set_brightness(brightness)
        
        if fingers == [0, 1, 1, 1, 0]: #Volume Increase    
            volume_level = volume_level+5
            if(volume_level<=100 and volume_level>=0):
               setVolume.setvolume(volume_level)
            else:
                volume_level = 100

        if fingers == [0, 1, 1, 1, 1]: #Volume Decrease
            volume_level = volume_level-5
            if(volume_level>=0 and volume_level<=100):
               setVolume.setvolume(volume_level)
            else: 
                volume_level = 0

        if fingers == [0, 1, 1, 0, 0]: #AI Virtual Mouse
            hands = output.multi_hand_landmarks
            for hand in hands:
                drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x * windowWidth)
                    y = int(landmark.y * windowHeight)
                    if id == 8:
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                        index_x = screenWidth / windowWidth * x
                        index_y = screenHeight / windowHeight * y
                        pyautogui.moveTo(index_x, index_y)
                    if id == 12:
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                        thumb_x = screenWidth / windowWidth * x
                        thumb_y = screenHeight / windowHeight * y
                        if (abs(thumb_x - index_x) < 70):
                            pyautogui.click()





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
