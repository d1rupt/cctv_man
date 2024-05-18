import cv2


def detect_mov(background, cv_img):
    movement = False
    orig_frame = cv_img.copy()
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    frame_diff = cv2.absdiff(gray, background)
    ret, thres = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)
    dilate_frame = cv2.dilate(thres, None, iterations=2)
    contours, hierarchy = cv2.findContours(dilate_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 500:
            continue
        (x,y,w,h) = cv2.boundingRect(contour)
        movement = True

        cv2.rectangle(orig_frame, (x,y), (x+w, y+h), (0,255,0), 2)

    return orig_frame, movement