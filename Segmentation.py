import pydicom as dicom
import numpy as np
import matplotlib.pyplot as plt
import os
import skimage.io as io
import skimage.color
import skimage.filters
import skimage.segmentation
import cv2
import PIL
import imutils

path = "./im2/100.dcm"

#Load Dicom file and save side view of scan as PNG
def initializeDicom():

    dcm = dicom.dcmread(path)    
    # Get a specific slice
    slice = dcm.pixel_array[:,:]

    # Plot the slice using matplotlib
    plt.imshow(slice, cmap='gray')

    # Save the slice as a PNG
    plt.axis('off')
    plt.savefig('scan.png',bbox_inches='tight',transparent=True, pad_inches=0)
    
def is_contour_bad(c):
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	# the contour is 'bad' if it is not a rectangle
	return not len(approx) == 4

def is_contour_small(c):
	# approximate the contour
	size = cv2.contourArea(c) > 200
	# the contour is 'bad' if it is too small
	return size

initializeDicom()


from PIL import Image, ImageFilter
img = Image.open('scan.png').convert('L')
blurred_image = img.filter(ImageFilter.MedianFilter).save('grayscale.png')
#blurred_image = img.filter(ImageFilter.MedianFilter).transpose(Image.Transpose.FLIP_LEFT_RIGHT).rotate(270).save('grayscale.png')
gray = plt.imread("grayscale.png")

threshold = 0.420
binary_mask = gray < threshold
plt.imshow(binary_mask, cmap="gray")
plt.savefig('thres.png',bbox_inches='tight',transparent=True, pad_inches=0)
image = cv2.imread("thres.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
edged = cv2.Canny(blurred, 10, 100)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# apply the dilation operation to the edged image
dilate = cv2.dilate(edged, kernel, iterations=1)

cv2.imshow("Original", image)
# find contours in the image and initialize the mask that will be
# used to remove the bad contours
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
mask = np.ones(image.shape[:2], dtype="uint8") * 255
# loop over the contours
for c in cnts:
	# if the contour is bad, draw it on the mask
	if is_contour_bad(c) and is_contour_small(c):
		cv2.drawContours(mask, [c], -1, 0, -1)
# remove the contours from the image and show the resulting images
#image = cv2.bitwise_and(image, image, mask=mask)

cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
cnts = cnts[:4]

img_gray = cv2.imread("grayscale.png", cv2.IMREAD_GRAYSCALE)

img_contour = cv2.addWeighted(img_gray, 0.7, mask, 0.3, 0)
result = cv2.bitwise_and(img_contour, img_contour, mask=mask)
# create a blank image to store all the contoured sections
all_contoured_sections = np.zeros_like(img_gray)
for i in range(len(cnts)):
    contoured_section = img_gray[cnts[i][:,0][:,1].min():cnts[i][:,0][:,1].max(), cnts[i][:,0][:,0].min():cnts[i][:,0][:,0].max()]
    cv2.drawContours(all_contoured_sections, [cnts[i]], 0, contoured_section.mean(), -1)
    print("Mean intensity: ", contoured_section.mean())
    
cv2.imshow("All contoured sections", all_contoured_sections)
sorted_cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
largest_cnts = sorted_cnts[:]

for cnt in largest_cnts:
    area = cv2.contourArea(cnt)
    print("Contour Area:", area)
cv2.imshow("Mask", mask)
cv2.imshow("After", result)
cv2.imwrite("result.png", result)
cv2.waitKey(0)
