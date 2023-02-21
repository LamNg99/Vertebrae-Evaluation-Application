import cv2
import imutils
import numpy as np

def is_bad_contour(contour):
	# approximate the contour
	peri = cv2.arcLength(contour, True)
	approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
	# the contour is 'bad' if it is not a rectangle
	return not len(approx) == 4

def is_small_contour(contour, area_threshold):
	return cv2.contourArea(contour) > area_threshold

def get_segmentation(area_theshold):
	# Load original and binary images
	original = cv2.imread('original.png')
	binary = cv2.imread('binary.png')

	# Grayscale
	original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
	binary_gray = cv2.cvtColor(binary, cv2.COLOR_BGR2GRAY)

	slicedImage = binary_gray[0:400, 140:250]

	background = np.zeros(original.shape[:2], dtype='uint8') * 255
	background[0:400, 140:250] = slicedImage

	blurred = cv2.GaussianBlur(background, (3, 3), 0)
	edged = cv2.Canny(blurred, 10, 100)
	edged = cv2.dilate(edged, None, iterations=1)
	edged = cv2.erode(edged, None, iterations=1)

	# Finding Contours
	# Use a copy of the image e.g. edged.copy()
	# Since findContours alters the image
	contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	cnts = imutils.grab_contours(contours)
	mask = np.zeros(original.shape[:2], dtype='uint8') * 255
	# loop over the contours
	for c in cnts:
		# if the contour is bad, draw it on the mask
		if is_bad_contour(c) and is_small_contour(c, area_theshold):
			cv2.drawContours(mask, [c], -1, 255, -1)

	cv2.imwrite('mask.png', mask)

	# Bitwise-AND mask and original image
	segmented_image = cv2.bitwise_and(original_gray, original_gray ,mask= mask)
	cv2.imwrite('segmentedimage.png', segmented_image)


