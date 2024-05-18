import json
import cv2

def read_config():
    #reads cameras.json
    try:
        with open('./config/cameras.json', 'r') as f:
            js = json.load(f)
    except:
        js = []
    return js
def list_cameras_ids():
    #gets ids of cameras connected, except the ones already configured
    skip = []
    js = read_config()
    for i in js:
        if "idchoice" in i.keys():
            skip.append(int(i["idchoice"]))
    arr = []
    for index in range(-1, 10):
        if index not in skip:
            try:
                cap = cv2.VideoCapture(index)
                if cap.read()[0]:
                    arr.append(index)
                cap.release()
            except:
                pass

    return arr