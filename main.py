import cv2
import numpy as np

IMAGE_NAME = '3.jpg'
WINDOW_NAME = 'window'

BRIGHTNESS_LABEL = 'brightness'
CONTRAST_LABEL = 'contrast'
THRESHOLD_LABEL = 'threshold'
thr_param1_LABEL = 'thr param1'
thr_param2_LABEL = 'thr param2'

LINE_LENGTH_LABEL = 'line length'


def nothing(x):
    pass


def image_processing(image, _brightness, _thr_param1, _thr_param2, _threshold, _line_length):
    _image = image.copy()

    gray = cv2.cvtColor(_image, cv2.COLOR_BGR2GRAY)
    # thresh = gray

    thresh = cv2.adaptiveThreshold(gray, _brightness, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, thr_param1, thr_param2)

    edges = cv2.Canny(thresh, 100, 200, apertureSize=3)

    # lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    #
    # for rho, theta in lines[0]:
    #     a = np.cos(theta)
    #     b = np.sin(theta)
    #     x0 = a * rho
    #     y0 = b * rho
    #     x1 = int(x0 + 1000 * (-b))
    #     y1 = int(y0 + 1000 * a)
    #     x2 = int(x0 - 1000 * (-b))
    #     y2 = int(y0 - 1000 * a)
    #
    #     cv2.line(_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    min_line_length=100
    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi/180, threshold=_threshold,
                            lines=np.array([]), minLineLength=min_line_length, maxLineGap=80)

    try:
        a, b, c = lines.shape
        for i in range(a):

            x1 = lines[i][0][0]
            y1 = lines[i][0][1]
            x2 = lines[i][0][2]
            y2 = lines[i][0][3]

            x = x1 - _line_length
            y = int(((x - x1) * (y2 - y1)) / (x2 - x1) + y1)

            cv2.line(_image,
                     (x, y),
                     (x2, y2), (0, 255, 0), 3, cv2.LINE_AA)

        # cv2.imshow('thresh', gray)
    except:
        print('error')
        pass
    return _image

cv2.namedWindow(WINDOW_NAME)

# create track bars for relevant params
# track bar name, window name, diapason, function
cv2.createTrackbar(BRIGHTNESS_LABEL, WINDOW_NAME, 255, 255, nothing)
cv2.createTrackbar(LINE_LENGTH_LABEL, WINDOW_NAME, 0, 255, nothing)
cv2.createTrackbar(THRESHOLD_LABEL, WINDOW_NAME, 236, 255 * 3, nothing)

cv2.createTrackbar(thr_param1_LABEL, WINDOW_NAME, 255, 255, nothing)
cv2.createTrackbar(thr_param2_LABEL, WINDOW_NAME, 33, 50, nothing)

# open source image
image = cv2.imread(IMAGE_NAME)

while True:
    # close by ESC
    k = cv2.waitKey(1)
    if k == 27:
        break

    # get current positions of four track bars
    brightness = cv2.getTrackbarPos(BRIGHTNESS_LABEL, WINDOW_NAME)
    contrast = cv2.getTrackbarPos(CONTRAST_LABEL, WINDOW_NAME)
    thr_param1 = cv2.getTrackbarPos(thr_param1_LABEL, WINDOW_NAME)
    thr_param2 = cv2.getTrackbarPos(thr_param2_LABEL, WINDOW_NAME)
    threshold = cv2.getTrackbarPos(THRESHOLD_LABEL, WINDOW_NAME)

    if thr_param1 % 2 == 0:
        thr_param1 += 1

    if thr_param1 <= 2:
        thr_param1 = 3

    line_length = cv2.getTrackbarPos(LINE_LENGTH_LABEL, WINDOW_NAME) * 2

    # processed image
    image_to_show = image_processing(image, brightness, thr_param1, thr_param2, threshold, line_length)
    image_to_show = cv2.resize(image_to_show, (640, 480))
    cv2.imshow(WINDOW_NAME, image_to_show)

cv2.destroyAllWindows()

