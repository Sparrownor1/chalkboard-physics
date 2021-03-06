import numpy as np
import cv2

cap = cv2.VideoCapture(1)
while True:
    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)

    HEIGHT, WIDTH, _ = frame.shape

    x1 = int(2*WIDTH/8)
    y1 = int(HEIGHT/8)
    x2 = int(6*WIDTH/8)
    y2 = int(7*HEIGHT/8)

    p1 = (x1, y1)
    p2 = (x2, y2)

    display = cv2.rectangle(frame, p1, p2, (255, 0, 0), 5)

    black = cv2.bitwise_xor(display, display)
    mask = cv2.rectangle(black, (x1, y1), (x2, y2), (255, 255, 255), -1)

    frame = cv2.bitwise_and(frame, mask)

    cv2.imshow('display', display)

    if cv2.waitKey(1) == ord('e'):
        drawing = frame
        break
    if cv2.waitKey(1) == ord('q'):
        exit()

#now drawing is the img with the data for the physics
# cv2.imshow('frame', frame)
canny = cv2.Canny(drawing, 100, 200)
# cv2.imshow('edge', canny)

# CIRCLES
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100, 
                           maxRadius = 100, param1 = 100, param2 = 60)

gray = cv2.blur(gray, (3,3))

shapeDisplay = frame

if circles is not None:
    
    circles = np.round(circles[0, :]).astype("int")

    for (x, y, r) in circles:
        shapeDisplay = cv2.circle(shapeDisplay, (x, y), r, (0, 255, 0), 5)
        cv2.rectangle(shapeDisplay, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

cv2.imshow('gray', gray)
cv2.imshow('shapes', shapeDisplay)

cv2.waitKey(0)

cap.release() 
cv2.destroyAllWindows()