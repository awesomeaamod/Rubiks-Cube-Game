import cv2
import numpy as np

cam = cv2.VideoCapture(2)
cv2.namedWindow('Tuner')

def nothing(para):
    pass

cv2.createTrackbar('H Min', 'Tuner', 0, 255, nothing)
cv2.createTrackbar('S Min', 'Tuner', 0, 255, nothing)
cv2.createTrackbar('V Min', 'Tuner', 0, 255, nothing)
cv2.createTrackbar('H Max', 'Tuner', 255, 255, nothing)
cv2.createTrackbar('S Max', 'Tuner', 255, 255, nothing)
cv2.createTrackbar('V Max', 'Tuner', 255, 255, nothing)
cv2.createTrackbar('Kill', 'Tuner', 0, 1, nothing)

while cv2.getTrackbarPos('Kill', 'Tuner') == 0:
    img = cam.read()[1]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    filtered = cv2.inRange(hsv, (cv2.getTrackbarPos('H Min', 'Tuner'), cv2.getTrackbarPos('S Min', 'Tuner'), cv2.getTrackbarPos('V Min', 'Tuner')),
                           (cv2.getTrackbarPos('H Max', 'Tuner'), cv2.getTrackbarPos('S Max', 'Tuner'), cv2.getTrackbarPos('V Max', 'Tuner')))
    filtered = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    filtered = cv2.morphologyEx(filtered, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    cv2.imshow('Camera Feed', img)
    cv2.imshow('Filtered', filtered)
    cv2.imshow('Mask', cv2.bitwise_and(img, cv2.cvtColor(filtered, cv2.COLOR_GRAY2BGR)))
    cv2.waitKey(1)

print(cv2.getTrackbarPos('H Min', 'Tuner'), cv2.getTrackbarPos('S Min', 'Tuner'), cv2.getTrackbarPos('V Min', 'Tuner'), cv2.getTrackbarPos('H Max', 'Tuner'), cv2.getTrackbarPos('S Max', 'Tuner'), cv2.getTrackbarPos('V Max', 'Tuner'))

cam.release()
cv2.destroyAllWindows()

# Green: 61 83 92 102 255 212
# Blue: 88 109 92 114 255 255
# Red: 0 212 116 19 253 239
# Orange: 0 135 175 16 255 255
# Yellow: 26 78 78 36 255 255


# Green: 75 75 109 92 255 255
# Blue: 92 158 83 108 255 255
# Red: 0 113 144 204 241 221
# Orange: 2 57 106 12 255 255
# Yellow: 26 29 111 59 231 255
# White: 97 28 108 139 180 255