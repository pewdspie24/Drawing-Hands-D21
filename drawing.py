import cv2
import numpy as np
import time
import os
import module as htm
 
#######################
brushThickness = 10
eraserThickness = 100
drawColor = (255, 0, 255)
headerColor = [(255,0,255), (255,255,0), (0,255,255), (0,0,0)]
########################
 
drawColor = (255, 0, 255)
 
WINDOW_SIZE = (480, 640, 3)
HEADER_SIZE = (int(WINDOW_SIZE[1]), int(WINDOW_SIZE[0]/20))
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
 
detector = htm.handDetector(detectionCon=0.65,maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros(WINDOW_SIZE, np.uint8)
# print(WINDOW_SIZE[:-1]/4)
header = np.zeros(WINDOW_SIZE, np.uint8)
header[:] = headerColor[1]
print(header.shape)
header[0:WINDOW_SIZE[0], 0:(WINDOW_SIZE[1]//4)] = headerColor[0]
header[0:WINDOW_SIZE[0], (WINDOW_SIZE[1]//4):(WINDOW_SIZE[1]//2)] = headerColor[1]
header[0:WINDOW_SIZE[0], (WINDOW_SIZE[1]//2):(WINDOW_SIZE[1]//4*3)] = headerColor[2]
header[0:WINDOW_SIZE[0], (WINDOW_SIZE[1]//4*3):(WINDOW_SIZE[1])] = headerColor[3]
header = cv2.resize(header, HEADER_SIZE)
print(HEADER_SIZE)
print(WINDOW_SIZE[0]-HEADER_SIZE[1], WINDOW_SIZE[1]-HEADER_SIZE[0])
print(header.shape)
# img[(WINDOW_SIZE[1]-HEADER_SIZE[0]):HEADER_SIZE[1], (WINDOW_SIZE[1]-HEADER_SIZE[0]):WINDOW_SIZE[1]] = header
while True:
 
    # 1. Import image
    success, img = cap.read()
    if success:
        try:
            img = cv2.flip(img, 1)
            
            # header = np.zeros((480, 640, 3), np.uint8)
            # 2. Find Hand Landmarks
            img = detector.findHands(img)
            
            lmList = detector.findPosition(img, draw=False)
            # print(len(lmList[0]))

            if len(lmList) != 0:
                # print(lmList[0])
                
                # tip of index and middle fingers
                x1, y1 = lmList[0][8][1:]
                x2, y2 = lmList[0][4][1:]
                # print("cc")
                # 3. Check which fingers are up
                fingers = detector.fingersUp()
                checkDraw = detector.checkDraw()
                checkErase = detector.checkErase()
                print(fingers)
                # 4. If Selection Mode - Two finger are up
                if fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1:
                    xp, yp = 0, 0
                # 5. If Drawing Mode - Index finger is up

                elif checkErase:
                    xp, yp = 0, 0
                    # print("cc")
                    imgCanvas = np.zeros(WINDOW_SIZE, np.uint8)
                    
                elif fingers[0] == 0 and fingers[1]:
                    cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

                elif fingers[1] and fingers[2]:
                        if y1 < HEADER_SIZE[1]:
                            if 0 < x1 < WINDOW_SIZE[1]//4:
                                drawColor = headerColor[0]
                            elif WINDOW_SIZE[1]//4 < x1 < WINDOW_SIZE[1]//2:
                                drawColor = headerColor[1]
                            elif WINDOW_SIZE[1]//2 < x1 < WINDOW_SIZE[1]//4*3:
                                drawColor = headerColor[2]
                            elif WINDOW_SIZE[1]//4*3 < x1 < WINDOW_SIZE[1]:
                                drawColor = headerColor[3]
                
                elif checkDraw:
                    cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                    # print("Drawing Mode")
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
            img[(WINDOW_SIZE[1]-HEADER_SIZE[0]):HEADER_SIZE[1], (WINDOW_SIZE[1]-HEADER_SIZE[0]):WINDOW_SIZE[1]] = header
            cv2.imshow("Image", img)
            # Setting the header image
            # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
            # cv2.imshow("Image", img)
            # cv2.imshow("Canvas", imgCanvas)
        except:
            print("",end="")
            img[(WINDOW_SIZE[1]-HEADER_SIZE[0]):HEADER_SIZE[1], (WINDOW_SIZE[1]-HEADER_SIZE[0]):WINDOW_SIZE[1]] = header
            cv2.imshow("Image", img)
    if cv2.waitKey(1)&0xFF == 27:
        break