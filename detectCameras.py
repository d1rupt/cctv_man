import json
import cv2
import pathlib
def read_config():
    #reads cameras.json
    try:
        with open('./config/cameras.json', 'r') as f:
            js = json.load(f)
    except:
        js = []
        json_object = json.dumps(js, indent=4)
        pathlib.Path('./config/').mkdir(parents=True, exist_ok=True)
        with open("./config/cameras.json", "w") as outfile:
            outfile.write(json_object)

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