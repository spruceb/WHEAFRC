"""
Vision Processing using the Robot Feed
The idea for this program is to be able to edit the masking values on the fly
Hopefully there will be HSV value sliders on the screen so that there is no need for
changing the values in the code each time. 

ToDo - Get the Camera Feed from the Robot Working - √
ToDo - Add Sliders to edit the HSV Values - √
ToDo - Find Corners of the Target
ToDo - Get the LED Light Ring Working
"""

import urllib, urllib2
import numpy as np
import cv2

stream = urllib.urlopen('http://10.38.81.11/mjpg/video.mjpg')
def nothing():pass
bytes=''
cv2.namedWindow('masked Tracking')

cv2.createTrackbar('Hue_upper','masked Tracking',0,180,nothing)
cv2.createTrackbar('Saturation_upper','masked Tracking',0,255,nothing)
cv2.createTrackbar('Value_upper','masked Tracking',0,255,nothing)
cv2.createTrackbar('Hue_lower','masked Tracking',0,180,nothing)
cv2.createTrackbar('Saturation_lower','masked Tracking',0,255,nothing)
cv2.createTrackbar('Value_lower','masked Tracking',0,255,nothing)
while True:
	bytes+=stream.read(16384)
	a = bytes.find('\xff\xd8')
	b = bytes.find('\xff\xd9')
	if a != -1 and b != -1:
		jpg = bytes[a:b+2]
		bytes = bytes[b+2:]
		i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
		HSV = cv2.cvtColor(i, cv2.COLOR_BGR2HSV)
		Hue_upper = cv2.getTrackbarPos('Hue_upper','masked Tracking')
		Saturation_upper = cv2.getTrackbarPos('Saturation_upper','masked Tracking')
		Value_upper = cv2.getTrackbarPos('Value_upper','masked Tracking')
		Hue_lower = cv2.getTrackbarPos('Hue_lower','masked Tracking')
		Saturation_lower = cv2.getTrackbarPos('Saturation_lower','masked Tracking')
		Value_lower = cv2.getTrackbarPos('Value_lower','masked Tracking')
		for value in (Hue_upper, Hue_lower, Saturation_upper, Saturation_lower, Value_upper, Value_lower):
			print 'HSV Values'
			print value
		lower_HSV_Bound = np.array([Hue_lower,Saturation_lower,Value_lower])
		upper_HSV_Bound = np.array([Hue_upper,Saturation_upper,Value_upper])
		mask = cv2.inRange(HSV, lower_HSV_Bound, upper_HSV_Bound)
		res = cv2.bitwise_and(i,i, mask=mask)
		edges = cv2.Canny(res, 50, 150, apertureSize = 3)
		minLineLength = 100
		maxLineGap = 20
		contours, hierarchy = cv2.findContours(edges,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		max_area = 0
		best_contour = 1
		for cnt in contours:
			area = cv2.contourArea(cnt)
			if area > max_area:
				max_area = area
				best_contour = cnt
		M = cv2.moments(best_contour)
		cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
		cv2.circle(edges,(cx,cy),5,255,-1)
		cv2.circle(res,(cx,cy),5,255,-1)
		cv2.imshow('masked Tracking',mask)
		print cx,cy
		cv2.imshow('i',i)
		if cv2.waitKey(1) == ord('1'):
			exit(0)