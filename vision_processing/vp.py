import cv2
import numpy as np
import time
#
#class Vision:
#    def __init__(self):
cv2.namedWindow('image')
cv2.createTrackbar('Hue Min', 'image', 0, 180, int)
cv2.createTrackbar('Hue Max', 'image', 0, 180, int)
cv2.createTrackbar('Saturation Min', 'image', 0, 255, int)
cv2.createTrackbar('Saturation Max', 'image', 0, 255, int)
cv2.createTrackbar('Value Min', 'image', 0, 255, int)
cv2.createTrackbar('Value Max', 'image', 0, 255, int)





cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    Hue_upper = cv2.getTrackbarPos('Hue Max', 'image')
    Saturation_upper = cv2.getTrackbarPos('Saturation Max', 'image')
    Value_upper = cv2.getTrackbarPos('Value Max', 'image')
    Hue_lower = cv2.getTrackbarPos('Hue Min', 'image')
    Saturation_lower = cv2.getTrackbarPos('Saturation Min', 'image')
    Value_lower = cv2.getTrackbarPos('Value Min', 'image')
    lower_HSV_Bound = np.array([Hue_lower, Saturation_lower, Value_lower])
    upper_HSV_Bound = np.array([Hue_upper, Saturation_upper, Value_upper])
    mask = cv2.inRange(HSV, lower_HSV_Bound, upper_HSV_Bound)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    edges = cv2.Canny(res, 50, 300, apertureSize = 3)
    cv2.imshow('mask', mask)
    cv2.imshow('frame',frame)
    cv2.imshow('res', res)
    cv2.imshow('edges',edges)
    if cv2.waitKey(1) == 27:
        break
    if cv2.waitKey(1) == 119:
        with open("log.txt", "a") as f:
          f.write("{}\nHue: {}-{}\nSaturation: {}-{}\nValue: {}-{}\n".format(time.asctime(), Hue_lower, Hue_upper,
                                                                           Saturation_lower, Saturation_upper,
                                                                           Value_lower, Value_upper))
    time.sleep(0.01)

cap.release()
cv2.destroyAllWindows()