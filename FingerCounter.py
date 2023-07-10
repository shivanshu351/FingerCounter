import time
import os
import mediapipe as mp
import cv2 as cv

frame_capture=cv.VideoCapture(1)
ptime=0


mpHand=mp.solutions.hands
hands=mpHand.Hands()
mpDraw=mp.solutions.drawing_utils
lmList=[]
def Findposition(frame, handNo=0, draw=True):
    lmList = []
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            # print(id, lm)
            h, w, c = frame.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            # print(id, cx, cy)
            lmList.append([id, cx, cy])
    return lmList


folderpath="FingerImages"
myList=os.listdir(folderpath) #os.listdir() gets list of all files and directories astored in the specified path
overlayList=[]
for imPath in myList:#reads each image of the list ex-FingerImages/1finger.jpg
    image=cv.imread(f'{folderpath}/{imPath}')
    overlayList.append(image)

tipIds=[4,8,12,16,20]
while(True):
    isTrue,frame=frame_capture.read()
    frameRgb=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    results = hands.process(frameRgb)

    # img=detector.findHands(frame) #sending in the image
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:  # extract information for each hand

            mpDraw.draw_landmarks(frame, handLms, mpHand.HAND_CONNECTIONS)

    lmList = Findposition(frame, draw=False)
    if len(lmList)!=0:
        fingers=[]
        if lmList[tipIds[0]][1]> lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        #4fingers
        for id in range(1,5):
            if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
            # cv.putText(frame, '1', (300, 150), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        print(fingers)
        totalFingers=fingers.count(1)
        print(totalFingers)
        cv.putText(frame,str(int(totalFingers)),(300,150),cv.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
        # if (lmList[8][2]<lmList[6][2] & lmList[10][2]<lmList[12][2] & lmList[16][2]>lmList[14][2] & lmList[20][2] > lmList[18][2]):
        #         cv.putText(frame,'1',(300,150),cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0),3)
    #setting size of each image as per any image
    h,w,c=overlayList[0].shape
    frame[0:h,0:w]=overlayList[0]

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    cv.putText(frame, str(int(fps)), (300, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv.imshow('Vid', frame)


    if cv.waitKey(10)==ord('q'):
        break
frame_capture.release()
cv.destroyAllWindows