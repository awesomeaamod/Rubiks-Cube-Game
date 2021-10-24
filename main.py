import cv2
import numpy as np

kernel = np.ones((5, 5), np.uint8)

def process(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    filtered = cv2.inRange(hsv, (105, 120, 120), (118, 255, 255))
    filtered = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    filtered = cv2.morphologyEx(filtered, cv2.MORPH_CLOSE, kernel)
    return img, filtered

cam = cv2.VideoCapture(0)

for i in range(2000):
    img, filtered = process(cam.read()[1])
    contours = cv2.findContours(filtered, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
    largestArea = 2000
    largestAreaIndex = None

    if len(contours) > 0:
        j = 0
        for j in range(len(contours)):
            contourArea = cv2.contourArea(contours[j])
            if largestArea < contourArea:
                largestArea = contourArea
                largestAreaIndex = j

        if not largestAreaIndex == None:
            x, y, w, h = cv2.boundingRect(contours[largestAreaIndex])
            cv2.drawContours(img, contours, largestAreaIndex, (0, 0, 0), 6)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 6)

            ratio = h/w
            if 0.8 <= ratio <= 1.2:
                print('3 layers', ratio, cv2.contourArea(contours[largestAreaIndex]))
            elif 0.5 <= ratio < 0.8:
                print('2 layers', ratio, cv2.contourArea(contours[largestAreaIndex]))
            elif 0.25 <= ratio < 0.5:
                print('1 layer', ratio, cv2.contourArea(contours[largestAreaIndex]))
            elif 1.2 < ratio <= 1.5:
                print('2 vertical layers', ratio, cv2.contourArea(contours[largestAreaIndex]))
            elif 1.5 < ratio <= 4:
                print('1 vertical layer', ratio, cv2.contourArea(contours[largestAreaIndex]))
            else:
                print('0 layers', ratio, cv2.contourArea(contours[largestAreaIndex]))

    cv2.imshow('Camera Feed', img)
    cv2.imshow('Filtered', filtered)
    cv2.waitKey(1)
    if i % 100 == 0:
        print(i)

cam.release()
cv2.destroyAllWindows()
