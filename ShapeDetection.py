#Add opencv-python and matlotlib to python interpretor

import cv2
import matplotlib.pyplot as plt
import os
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(17, GPIO.IN)
GPIO.setup(14, GPIO.IN)

f = open("Database","a")
SevSeg_count = 0
PowerSupp_count = 0
Motor_count =0
IC_count=0
UltrSon_count = 0
LED_count =0
loopACT=1
while loopACT ==1:
    if (GPIO.input(17)):
        cap = cv2.VideoCapture(0)
        ret, img = cap.read()
        imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thrash = cv2.threshold(imgGrey, 240, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
        cv2.drawContours(img, [approx], 0, (255,0,0), 5,)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        if len(approx) == 3:
            cv2.putText(img, "Seven Segment", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0))
            f.write("Seven Segment\n")
            print("adding Seven Segment to database")
            SevSeg_count=SevSeg_count+1
        elif len(approx) == 4:
            x,y,w,h = cv2.boundingRect(approx)
            aspectRation = float(w)/h
            print(aspectRation)
            if aspectRation >= 0.92 and aspectRation <= 1.08:
                cv2.putText(img, "Power Supply", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
                f.write("Power Supply\n")
                print("adding Power Supply to database")
                PowerSupp_count=PowerSupp_count+1
            else:
                cv2.putText(img, "I.C.", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0))
                f.write("I.C.\n")
                print("adding I.C. to database")
                IC_count=IC_count+1

        elif len(approx) == 5:
            cv2.putText(img, "Motor", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0))
            f.write("Motor\n")
            print("adding Motor to database")
            Motor_count=Motor_count+1
        elif len(approx) == 8:
            cv2.putText(img, "Ultrasonic Sensor", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
            f.write("Ultrasonic Sensor\n")
            print("adding Ultrasonic sensor to database")
            UltrSon_count=UltrSon_count+1
        else:
            cv2.putText(img, "LED", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
            f.write("LED\n")
            print("adding LED to database")
            LED_count=LED_count+1
    cv2.imshow("Shape", img)
    cap.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if(GPIO.input(14)):

        cap = cv2.VideoCapture(0)
        ret, img = cap.read()
        imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thrash = cv2.threshold(imgGrey, 240, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
        cv2.drawContours(img, [approx], 0, (255,0,0), 5,)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        entity1 = f.readline()
        if len(approx) == 3 and SevSeg_count != 0:
            cv2.putText(img, "Seven Segment", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0))
            del f[0]
            print("Deleting Seven Segment to database")
            SevSeg_count=SevSeg_count-1

        elif len(approx) == 4 :
            x,y,w,h = cv2.boundingRect(approx)
            aspectRation = float(w)/h
            print(aspectRation)
            if aspectRation >= 0.92 and aspectRation <= 1.08 and entity1 == "Power Supply":
                cv2.putText(img, "Power Supply", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
                f.write("Power Supply\n")
                print("Deleting Power Supply to database")
                PowerSupp_count=PowerSupp_count-1
            elif aspectRation < 0.92 and aspectRation > 1.08 and entity1 == "I.C.":
                cv2.putText(img, "I.C.", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0))
                f.write("I.C.\n")
                print("Deleting I.C. to database")
                IC_count=IC_count-1
        elif len(approx) == 5:
            cv2.putText(img, "Motor", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0))
            f.write("Motor\n")
            print("Deleting Motor to database")
            Motor_count=Motor_count-1
        elif len(approx) == 8:
            cv2.putText(img, "Ultrasonic Sensor", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
            f.write("Ultrasonic Sensor\n")
            print("Deleting Ultrasonic sensor to database")
            UltrSon_count=UltrSon_count-1
        else:
            cv2.putText(img, "LED", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
            f.write("LED\n")
            print("Deleting LED to database")
            LED_count=LED_count-1
    cv2.imshow("Shape", img)
    cap.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()


cap.release()
if(SevSeg_count+PowerSupp_count+IC_count+Motor_count+UltrSon_count+LED_count)!=0:
    print("Something is missing in the process")
