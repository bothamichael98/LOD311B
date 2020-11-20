import cv2
import matplotlib.pyplot as plt
import os


#cap = cv2.VideoCapture(0)
#ret, frame = cap.read()

#img1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#plt.imshow(img1)
#plt.title("ABCD")
#plt.xticks([])
#plt.yticks([])
#plt.show()

#cv2.imwrite('Michael.png',img1)
#os.remove("Michael.png")

#f = open("Database","a")
#f.write("Circle\n")
#f.close()

#f = open("Database","r")
#print(f.readline())
#os.remove('Database')

#cap.release()

cap = cv2.VideoCapture(0)
ret, img = cap.read()
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#img = cv2.imread('Circle.png')
imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thrash = cv2.threshold(imgGrey, 240, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
    cv2.drawContours(img, [approx], 0, (255,0,0), 5,)
    x = approx.ravel()[0]
    y = approx.ravel()[1]
    if len(approx) == 3:
        cv2.putText(img, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0))
    elif len(approx) == 4:
        x,y,w,h = cv2.boundingRect(approx)
        aspectRation = float(w)/h
        print(aspectRation)
        if aspectRation >= 0.92 and aspectRation <= 1.08:
            cv2.putText(img, "Square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
        else:
            cv2.putText(img, "Rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0))
    elif len(approx) == 5:
        cv2.putText(img, "Pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0))
    elif len(approx) == 8:
        cv2.putText(img, "Hexagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
    else:
        cv2.putText(img, "Circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
cv2.imshow("Shape", img)
cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
