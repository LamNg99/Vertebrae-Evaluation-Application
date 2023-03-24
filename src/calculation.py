import cv2
import numpy as np

def contour_area(image): 
    # convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find the contours using binary image
    contours, _ = cv2.findContours(gray, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # print("Number of contours in image:",len(contours))

    pixel_area = 0 
    for cnt in contours:
        pixel_area += cv2.contourArea(cnt)

    return pixel_area

def get_area(pixel_area, img_shape, dicom_shape, pixel_spacing):
    ratio = (dicom_shape[0] * dicom_shape[1]) / (img_shape[0] * img_shape[1])
    area = pixel_area * ratio * (pixel_spacing[0] * pixel_spacing[1])
    return area / 100

def get_height(num_slices, slice_thickness):
    height = num_slices * slice_thickness
    return height / 10 

def get_volume(area, height):
    return area * height

def get_bmc(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bmc = np.array(gray, dtype='float')
    bmc[(bmc > 0) & (bmc <= 50)] = 0.0026
    bmc[(bmc > 50) & (bmc <= 100)] = 0.0048
    bmc[(bmc > 100) & (bmc <= 150)] = 0.0061
    bmc[(bmc > 150) & (bmc <= 200)] = 0.0076
    bmc[(bmc > 200) & (bmc <= 255)] = 0.0093
    return np.sum(bmc)

def get_aBMD(bmc, area):
    return bmc / area

def get_vBMD(bmc, volume):
    return bmc / volume

def get_elastic_modulus(vBMD):
    return 757 * (vBMD ** 1.94) 