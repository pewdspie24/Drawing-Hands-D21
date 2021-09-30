# import cv2
# import numpy as np
# import module as htm
# import streamlit as st
# from streamlit_webrtc import VideoTransformerBase, webrtc_streamer


# st.title("Hehe")
# run = st.checkbox('Run')
# #######################
# FRAME_WINDOW = st.image([])
# brushThickness = 10
# eraserThickness = 100
# drawColor = (255, 0, 255)
# ########################
 
# drawColor = (255, 0, 255)

# detector = htm.handDetector(detectionCon=0.65,maxHands=1)
# xp, yp = 0, 0
# imgCanvas = np.zeros((480, 640, 3), np.uint8)
# class VideoTransformer(VideoTransformerBase):
#     def transform(self, frame):
#         img = frame.to_ndarray(format="bgr24")

#         try:
#             img = cv2.flip(img, 1)
        
#             # 2. Find Hand Landmarks
#             img = detector.findHands(img)
            
#             lmList = detector.findPosition(img, draw=False)
#             # print(len(lmList[0]))
#             if len(lmList) != 0:
#                 # print(lmList[0])
        
#                 # tip of index and middle fingers
#                 x1, y1 = lmList[0][8][1:]
#                 x2, y2 = lmList[0][12][1:]
#                 # print("cc")
#                 # 3. Check which fingers are up
#                 fingers = detector.fingersUp()
#                 checkDraw = detector.checkDraw()
        
#                 # 4. If Selection Mode - Two finger are up
#                 if fingers[1] and fingers[2] and fingers[3] and fingers[4]:
#                     # xp, yp = 0, 0
#                     imgCanvas = np.zeros((480, 640, 3), np.uint8)
#                 # 5. If Drawing Mode - Index finger is up

#                 if fingers[1]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:
#                     xp, yp = 0, 0
                
#                 if checkDraw:
#                     cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
#                     print("Drawing Mode")
#                     if xp == 0 and yp == 0:
#                         xp, yp = x1, y1
#                     # print(xp,yp,x1,y1)
#                     cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
        
#                     # if drawColor == (0, 0, 0):
#                     #     cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
#                     #     cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
#                     #
#                     # else:
#                     #     cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
#                     #     cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
        
#                     xp, yp = x1, y1
        
        
#                 # # Clear Canvas when all fingers are up
#                 # if all (x >= 1 for x in fingers):
#                 #     imgCanvas = np.zeros((720, 1280, 3), np.uint8)
        
#             # imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
#             # _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
#             # imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
#             # img = cv2.bitwise_and(img,imgInv)
#             # img = cv2.bitwise_or(img,imgCanvas)

#             img = cv2.add(img,imgCanvas)
            
#             # Optionally stack both frames and show it.
#             # stacked = np.hstack((imgCanvas,img))
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             # FRAME_WINDOW.image(img)
#             # cv2.imshow('Trackbars',cv2.resize(stacked,None,fx=0.6,fy=0.6))
#             # cv2.imshow("Image", img)
#         except:
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             # FRAME_WINDOW.image(img)

#         return img
 
# webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)

import cv2
from streamlit_webrtc import VideoProcessorBase, webrtc_streamer, RTCConfiguration, WebRtcMode
import av

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class OpenCVVideoProcessor(VideoProcessorBase):
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_ctx = webrtc_streamer(
        key="opencv-filter",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        video_processor_factory=OpenCVVideoProcessor,
        async_processing=True,
    )

if webrtc_ctx.video_processor:
        webrtc_ctx.video_processor.type = st.radio(
            "Select transform type", ("noop", "cartoon", "edges", "rotate")
        )