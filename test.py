import cv2
from physics import *



display = cv2.rectangle(frame, p1, p2, (255, 0, 0), 5)
black = cv2.bitwise_xor(display, display)
bg = cv2.rectangle(black, (x1, y1), (x2, y2), (255, 255, 255), -1)

cv2.imshow('test', bg)