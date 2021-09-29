import cv2
import numpy as np
import time
import os
import module as htm
 
#######################
brushThickness = 10
eraserThickness = 100
drawColor = (255, 0, 255)
########################
 
drawColor = (255, 0, 255)
 
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
 
detector = htm.handDetector(detectionCon=0.65,maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros((480, 640, 3), np.uint8)
 
while True:
 
    # 1. Import image
    success, img = cap.read()
    if success:
        try:
            img = cv2.flip(img, 1)
        
            # 2. Find Hand Landmarks
            img = detector.findHands(img)
            
            lmList = detector.findPosition(img, draw=False)
            # print(len(lmList[0]))
            if len(lmList) != 0:
                # print(lmList[0])
        
                # tip of index and middle fingers
                x1, y1 = lmList[0][8][1:]
                x2, y2 = lmList[0][12][1:]
                # print("cc")
                # 3. Check which fingers are up
                fingers = detector.fingersUp()
                checkDraw = detector.checkDraw()
        
                # 4. If Selection Mode - Two finger are up
                if fingers[1] and fingers[2] and fingers[3] and fingers[4]:
                    # xp, yp = 0, 0
                    imgCanvas = np.zeros((480, 640, 3), np.uint8)
                # 5. If Drawing Mode - Index finger is up

                if fingers[1]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:
                    xp, yp = 0, 0
                
                if checkDraw:
                    cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                    print("Drawing Mode")
                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1
                    # print(xp,yp,x1,y1)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
        
                    # if drawColor == (0, 0, 0):
                    #     cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                    #     cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
                    #
                    # else:
                    #     cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                    #     cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
        
                    xp, yp = x1, y1
        
        
                # # Clear Canvas when all fingers are up
                # if all (x >= 1 for x in fingers):
                #     imgCanvas = np.zeros((720, 1280, 3), np.uint8)
        
            # imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
            # _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
            # imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
            # img = cv2.bitwise_and(img,imgInv)
            # img = cv2.bitwise_or(img,imgCanvas)

            img = cv2.add(img,imgCanvas)
    
            # Optionally stack both frames and show it.
            stacked = np.hstack((imgCanvas,img))
            cv2.imshow('Trackbars',cv2.resize(stacked,None,fx=0.6,fy=0.6))
            cv2.imshow("Image", img)
            # Setting the header image
            # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
            # cv2.imshow("Image", img)
            # cv2.imshow("Canvas", imgCanvas)
        except:
            print("",end="")
            cv2.imshow("Image", img)
    if cv2.waitKey(1)&0xFF == 27:
        break