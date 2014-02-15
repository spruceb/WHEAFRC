import cv2
import numpy as np
import time
def nothing(x):pass
cv2.namedWindow('image')
cv2.createTrackbar('Hue_upper','image',0,180,nothing)
cv2.createTrackbar('Saturation_upper','image',0,255,nothing)
cv2.createTrackbar('Value_upper','image',0,255,nothing)
cv2.createTrackbar('Hue_lower','image',0,180,nothing)
cv2.createTrackbar('Saturation_lower','image',0,255,nothing)
cv2.createTrackbar('Value_lower','image',0,255,nothing)


cap = cv2.VideoCapture(0)

while True:
	ret, frame = cap.read()
	HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	Hue_upper = cv2.getTrackbarPos('Hue_upper','image')
	Saturation_upper = cv2.getTrackbarPos('Saturation_upper','image')
	Value_upper = cv2.getTrackbarPos('Value_upper','image')
	Hue_lower = cv2.getTrackbarPos('Hue_lower','image')
	Saturation_lower = cv2.getTrackbarPos('Saturation_lower','image')
	Value_lower = cv2.getTrackbarPos('Value_lower','image')
	lower_HSV_Bound = np.array([Hue_lower,Saturation_lower,Value_lower])
	upper_HSV_Bound = np.array([Hue_upper,Saturation_upper,Value_upper])
	mask = cv2.inRange(HSV, lower_HSV_Bound, upper_HSV_Bound)
	res = cv2.bitwise_and(frame,frame, mask= mask)
	edges = cv2.Canny(res, 50, 300, apertureSize = 3)
	cv2.imshow('mask',mask)
	cv2.imshow('frame',frame)
	cv2.imshow('res',res)
	cv2.imshow('edges',edges)
	if cv2.waitKey(1) == 27:
		break
	time.sleep(0.01)



cap.release()
cv2.destroyAllWindows()