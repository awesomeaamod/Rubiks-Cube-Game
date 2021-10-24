import cv2
import numpy as np
import colors

cam = cv2.VideoCapture(2) # 2 for webcam
cv2.namedWindow('Game')

def nothing(para):
    pass

z = 60
y = z-30

# coords =
coords = ((270+y, 175+y), (270+y, 205+2*y), (270+y, 235+3*y), (300+2*y, 175+y), (300+2*y, 205+2*y), (300+2*y, 235+3*y), (330+3*y, 175+y), (330+3*y, 205+2*y), (330+3*y, 235+3*y))
# coords = [(275, 195), (275, 225), (275, 255), (305, 195), (305, 225), (305, 255), (335, 195), (335, 225), (335, 255)]
first_character = {'green': 'G',
                   'blue': 'B',
                   'red': 'R',
                   'orange': 'O',
                   'yellow': 'Y',
                   'white': 'W'}

cv2.createTrackbar('Kill', 'Game', 0, 1, nothing)

while cv2.getTrackbarPos('Kill', 'Game') == 0:
    img = cv2.resize(cam.read()[1], (640, 480))
    cube = ['', '', '', '', '', '', '', '', '']

    for colorName in colors.colors:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        color = colors.colors[colorName]

        filtered = cv2.inRange(hsv, (color[0], color[1], color[2]), (color[3], color[4], color[5]))
        filtered = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        filtered = cv2.morphologyEx(filtered, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

        for i in range(9):
            square = img[coords[i][0]:coords[i][0] + z, coords[i][1]:coords[i][1] + z]
            # print(i, colorName, cv2.countNonZero(square))

            if colorName == 'green':
                cv2.imshow('square ' + str(i), square)

            # if cv2.countNonZero(square) > 1800:
            #     cube[i] = first_character[colorName]
        print(cube)
        cv2.imshow(colorName, filtered)

    for coord in coords:
        cv2.rectangle(img, (coord[0] - z, coord[1] + z), (coord[0] - 2*z, coord[1] + 2*z), (0, 0, 0), 4)

    print("final:", cube)

    # for coord in coords:
    #     cv2.rectangle(img, coord, (coord[0] + z, coord[1] + z), (0, 0, 0), 4)
    cv2.imshow('Camera Feed', img)
    # cv2.imshow('Mask', cv2.bitwise_and(img, cv2.cvtColor(filtered, cv2.COLOR_GRAY2BGR)))
    cv2.waitKey(1)

cam.release()
cv2.destroyAllWindows()
