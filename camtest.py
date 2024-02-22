import cv2

c = cv2.VideoCapture(0)

while True:
    ret, cv_img = c.read()
    if ret:
        cv2.imshow('image',cv_img)
        cv2.waitKey(0)