import numpy as np
import cv2
from physics import *

cap = cv2.VideoCapture(1)
while True:
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
        displayWithText = cv2.putText(display, "position shapes inside the box", (0, HEIGHT - 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        displayWithText = cv2.putText(displayWithText, "press e once shapes are drawn", (0, HEIGHT - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.namedWindow('display')
        cv2.moveWindow('display', 100, 100)
        cv2.imshow('display', displayWithText)

        if cv2.waitKey(1) == ord('e'):
            cv2.destroyWindow('display')
            break
        if cv2.waitKey(1) == ord('q'):
            exit()

    #now drawing is the img with the data for the physics
    # cv2.imshow('frame', frame)
    canny = cv2.Canny(frame, 100, 200)
    # cv2.imshow('edge', canny)

    # CIRCLES
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100, 
                            maxRadius = 100, param1 = 100, param2 = 60)

    gray = cv2.blur(gray, (3,3))

    shapeDisplay = display

    balls = []

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            shapeDisplay = cv2.circle(shapeDisplay, (x, y), r, (0, 255, 0), 5)
            cv2.rectangle(shapeDisplay, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            balls.append(Ball(x, y, r, 0, 0))

    #LINES
    lines = cv2.HoughLinesP(
        canny,
        1.0,
        np.pi/180,
        20,
        minLineLength=40,
        maxLineGap=10 
    )

    lines = [x[0] for x in lines]

    for xy in lines:
        shapeDisplay = cv2.line(shapeDisplay, (xy[0],xy[1]), (xy[2],xy[3]), [0,0,255], thickness=3)

    texted = cv2.putText(shapeDisplay, "press r if all the shapes are not detected", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    texted = cv2.putText(texted, "press any other key to see the simulation", (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    #cv2.imshow('gray', gray)
    cv2.namedWindow('shapes')
    cv2.moveWindow('shapes', 100, 100)
    cv2.imshow('shapes', texted)

    k = cv2.waitKey(0)
    cv2.destroyWindow("shapes")

    if k != ord('r'):
        break

while True:

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    HEIGHT, WIDTH, _ = frame.shape

    for ball in balls:
        #1. draw the ball
        x, y = int(ball.position[0]), int(ball.position[1])
        cv2.circle(frame, (x, y), int(ball.radius), (255, 0, 0), 5)

        #2. move the ball
        takeStep(ball, lines)
        print(ball.position)
    #display image
    cv2.namedWindow('out')
    cv2.moveWindow('out', 100, 100)
    cv2.imshow('out', frame)
    if cv2.waitKey(5) == ord('q'):
        break

cap.release() 
cv2.destroyAllWindows()