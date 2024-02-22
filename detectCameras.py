import json
import cv2

def read_config():
    with open('./config/cameras.json', 'r') as f:
        js = json.load(f)
    return js
def list_cameras_ids():
    skip = []
    js = read_config()
    for i in js:
        if "idchoice" in i.keys():
            skip.append(int(i["idchoice"]))
    arr = []
    for index in range(10):
        if index not in skip:
            cap = cv2.VideoCapture(index,cv2.CAP_DSHOW)
            if not cap.read()[0]:
                break
            else:
                arr.append(index)
            cap.release()
        index += 1
    return arr