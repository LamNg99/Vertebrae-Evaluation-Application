import cv2

def is_bad_contour(contour):
	# approximate the contour
	peri = cv2.arcLength(contour, True)
	approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
	# the contour is 'bad' if it is not a rectangle
	return not len(approx) == 4

def is_small_contour(contour):
	# approximate the contour
	size = cv2.contourArea(contour) > 200
	# the contour is 'bad' if it is too small
	return size