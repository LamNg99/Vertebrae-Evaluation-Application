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

path = "./im2"

#Load Dicom file and save side view of scan as PNG
def initializeDicom():
    slices = [dicom.read_file(path+'/'+s) for s in os.listdir(path)]
    slices.sort(key=lambda x: int(x.SliceLocation))
    ps = slices[0].PixelSpacing
    ss = slices[0].SliceThickness
    sag_aspect = ps[1]/ss
    img_shape = list(slices[0].pixel_array.shape)
    img_shape.append(len(slices))
    img3d = np.zeros(img_shape)    
    for i, s in enumerate(slices):
        img2d = s.pixel_array
        img3d[:, :, i] = img2d
    a2 = plt.subplot()
    plt.imshow(img3d[:, img_shape[1]//2, :])
    a2.set_aspect(sag_aspect)
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
	size = cv2.contourArea(c) > 100
	# the contour is 'bad' if it is too small
	return size

initializeDicom()

scan = plt.imread("scan.png")
spine = np.rot90(scan)
plt.imshow(spine)

from PIL import Image, ImageFilter
img = Image.open('scan.png').convert('L')
blurred_image = img.filter(ImageFilter.MedianFilter).transpose(Image.Transpose.FLIP_LEFT_RIGHT).rotate(270).save('grayscale.png')
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
image = cv2.bitwise_and(image, image, mask=mask)
cv2.imshow("Mask", mask)
cv2.imshow("After", image)
cv2.imwrite("result.png", image)
cv2.waitKey(0)

im2 = cv2.imread("result.png")
